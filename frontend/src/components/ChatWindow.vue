<template>
    <div class='chatwindow'>
        <VueChat :current-user-id="this.userid" :rooms="rooms" :messages="messages"
        :loading-rooms="false" :rooms-loaded="true" :messages-loaded="true"
        v-bind:single-room="singleRoom" :load-first-room="true" theme="dark"
        :show-add-room="false" :show-search="false" :rooms-list-opened="false"
        v-on:send-message="sendMessageHandler"
        />
    </div>
</template>

<script>
    import VueChat from 'vue-advanced-chat'
    import 'vue-advanced-chat/dist/vue-advanced-chat.css'

    import {io} from "socket.io-client";
    import axiosInstance from '../helpers/interceptor';
    import authHelper from '../helpers/auth';
    
    export default {
        props: ['selected'],
        mixins: [authHelper],
        watch: {
            selected: {
                async handler() {
                    await this.fetchData()
                    // setup a new websocket, fetch data for the new room.
                    if (this.socket) {
                        this.socket.disconnect();
                    }
                    this.setup_websocket()


                },
                deep: true
            }
        },
        components: {
            VueChat
        },
        data: function() {
            return {
                singleRoom: true,
                rooms: [],
                users: [],
                messages: [],
                userid_map: {},
                usergroup_id: null,
                socket: null,
            };
        },
        methods: {
            async fetch_room_info(selectedUser) {
                console.log(this.claims);
                let selectedUserId = selectedUser._id;
                let selectedUserName = selectedUser.name;

                // create a new room (or obtain one if already exists)
                let response = (await axiosInstance.post(process.env.VUE_APP_USERGROUPS_API_ENDPOINT + "/new", {"user_id": selectedUserId})).data;

                // map user ids to user names.
                let userid_map = {}

                // response contains a usergroup/room structure with id/name/tags and users list.
                response.users.forEach((user) => {
                    let u = {}
                    u._id = user._id
                    u.username = user.name
                    u.status = {
                        state: 'online'
                    }
                    this.users.push(u)
                    userid_map[user._id] = user.name
                });
                
                // assign new room to vue-adv-chat rooms list.
                this.usergroup_id = response._id;
                let room = {
                    roomId: this.usergroup_id,
                    roomName: selectedUserName,
                    unreadCount: 0,     // hardcoded for now
                    index: 1,           // hardcoded for now
                    lastMessage: {'content': '' },  // hardcoded for now
                    users: this.users,
                    typingUsers: []     // TODO
                }

                return [userid_map, [room]]
            },
            async fetch_historical_messages() {
                let messageApiUrl = process.env.VUE_APP_USERGROUPS_MESSAGES_API_ENDPOINT.replace('usergroup_id', this.usergroup_id)
                let response = (await axiosInstance.get(messageApiUrl)).data;
                let count = 0

                let messages = []
                response.data.forEach((message) => {
                    let m = {}
                    m._id = count
                    m.senderId = message.created_by
                    m.content = message.content?message.content:[]
                    m.username = this.userid_map[message.created_by]
                    m.date = message.creation_date.substring(5, 15)     // TODO: parse date here
                    m.timestamp = message.creation_date.substring(17, 22)     // TODO: parse date here
                    m.file = {}
                    m.reactions = {}
                    messages.push(m);

                    count += 1
                });
                return messages;
            },
            setup_websocket() {
                const socket = io("ws://localhost:5010", {transports: ["websocket"], reconnection: false});
                socket.on('connect', () => {
                    console.log("connected, socket_id:", socket.id);
                });

                console.log("listening on ", this.usergroup_id);
                // listen only to the currently open usergroup/room.  TODO: notify for other rooms this user has subscribed.
                socket.on(this.usergroup_id, (data) => {
                    let index = this.messages.length;
                    this.messages[index] = data.data;
                    this.messages = [...this.messages];
                    console.log("received", this.messages);
                });

                socket.on("disconnect", () => {
                    console.log("disconnected. socket_id:", socket.id);
                });
                this.socket = socket;
            },
            async fetchData() {
                let selectedUser = this.selected[0];
                let res = await this.fetch_room_info(selectedUser);
                this.userid_map = res[0]
                this.rooms = res[1]

                // fetch historical messages if any
                this.messages = await this.fetch_historical_messages();
            },
            sendMessageHandler(msg) {
                console.log(msg)
                let count = this.messages.length;
                if (msg.content || msg.file) {
                    msg._id = count;
                    msg.senderId = this.userid;
                    msg.username = this.username;
                    msg.date = new Date();
                    msg.timestamp = new Date().toTimeString();
                    msg.roomId = this.usergroup_id;
                    msg.reactions = {};

                    // Quick Hack:
                    // emit to default room, so the server does not have to open N number of connections,
                    // instead the server would fetch room info from the message and reply to connected clients on 
                    // "roomId". Clients listening on "roomId" (having their chat window open) shall receive the message.

                    // TODO: Implement proper authorization so only the authorized users can receive a mesaage.
                    this.socket.emit('event', {data: msg});
                }
            },
        mounted: function() {
            document.querySelector('vue-advanced-chat').currentUserId = this.userid;
            document.querySelector('vue-advanced-chat').rooms = this.rooms;
            document.querySelector('vue-advanced-chat').messages = this.messages;
        }
    }
}
</script>

<style scoped>
.chatwindow {
    padding-left: 20px;
}
</style>