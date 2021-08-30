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

    import io from "socket.io-client";
    import axiosInstance from '../helpers/interceptor';
    import authHelper from '../helpers/auth';
    
    export default {
        props: ['selected'],
        mixins: [authHelper],
        watch: {
            selected: {
                handler() {
                    this.fetchData()
                },
                deep: true
            }
        },
        components: {
            VueChat
        },
        data: function() {
            return {
                // currentUserId: this.userid,
                // currentUserName: this.username,
                singleRoom: true,
                rooms: [],
                // rooms:[
                // {
                //     roomId: 1,
                //     roomName: 'Room 1',
                //     avatar: 'assets/imgs/people.png',
                //     unreadCount: 0,
                //     index: 3,
                //     lastMessage: {
                //     content: 'Last message received',
                //     senderId: 1234,
                //     username: 'John Doe',
                //     timestamp: '10:20',
                //     saved: true,
                //     distributed: false,
                //     seen: false,
                //     new: true
                //     },
                //     users: [
                //     {
                //         _id: 1234,
                //         username: 'John Doe',
                //         avatar: 'assets/logo.png',
                //         status: {
                //         state: 'online',
                //         lastChanged: 'today, 14:30'
                //         }
                //     },
                //     {
                //         _id: 4321,
                //         username: 'John Snow',
                //         avatar: 'assets/logo.png',
                //         status: {
                //         state: 'online',
                //         lastChanged: '14 July, 20:00'
                //         }
                //     }
                //     ],
                //     typingUsers: [ 4321 ]
                // }
                // ],
                users: [],
                messages: [],
                userid_map: {},
                usergroup_id: null,
                socket: null,
                // messages: [
                //     {
                //         _id: 7890,
                //         content: 'message 1',
                //         senderId: 1234,
                //         username: 'John Doe',
                //         avatar: 'assets/logo.png',
                //         date: '13 November',
                //         timestamp: '10:20',
                //         system: false,
                //         saved: true,
                //         distributed: true,
                //         seen: true,
                //         deleted: false,
                //         disableActions: false,
                //         disableReactions: false,
                //         file: {},
                //         //   name: 'My File',
                //         //   size: 67351,
                //         //   type: 'png',
                //         //   audio: true,
                //         //   duration: 14.4,
                //         // //   url: 'https://firebasestorage.googleapis.com/...',
                //         // //   preview: 'data:image/png;base64,iVBORw0KGgoAA...'
                //         // },
                //         reactions: {
                //             wink: [
                //                 1234, // USER_ID
                //                 4321
                //             ],
                //             laughing: [
                //                 1234
                //             ]
                //         }   // reaction 1
                //     }   // message 1
                // ],     // messages
            };  // return data
        },   // data
        // async mounted() {
        //     let response = await axiosInstance.get(process.env.VUE_APP_USERGROUPS_API_ENDPOINT + '?q={"_id": "' + this.claims._id + '"}');
        //     this.rooms = response.data.usergroups;
        // },
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
                console.log(this.socket);
                if (this.socket) {
                    return;
                }
                const socket = io("ws://localhost:5010", {transports: ["websocket", "polling"]});
                socket.on('connect', () => {
                    console.log(socket.id);
                });

                socket.on(this.usergroup_id, (data) => {
                    console.log("messages", this.messages);
                    let index = this.messages.length;
                    this.messages[index] = data.data;
                    this.messages = [...this.messages];
                    console.log("received", this.messages);
                });

                socket.on("disconnect", () => {
                    console.log(socket.id);
                });

                this.socket = socket;
                console.log(this.socket);

            },
            async fetchData() {
                let selectedUser = this.selected[0];
                let res = await this.fetch_room_info(selectedUser);
                this.userid_map = res[0]
                this.rooms = res[1]

                // fetch historical messages if any
                this.messages = await this.fetch_historical_messages();

                this.setup_websocket();
            },
            // fetchMessages({ room, options }) {
            //     console.log("fetch messages", room, options);
            //     this.messagesLoaded = false

            //     // use timeout to imitate async server fetched data
            //     setTimeout(() => {
            //         this.messages = []
            //         this.messagesLoaded = true
            //     })
            // },
            sendMessageHandler(msg) {
                let count = this.messages.length;
                if (msg.content || msg.file) {
                    msg._id = count;
                    msg.senderId = this.userid;
                    // msg.content = msg.content?message.content:[]
                    msg.username = this.username;
                    msg.date = new Date();
                    msg.timestamp = new Date().toTimeString();
                    msg.roomId = this.usergroup_id;
                    msg.reactions = {} 
                    this.socket.emit('event', {data: msg});
                }
                // if (message.file) {
                //     this.socket.emit('event', {data: message});
                // }
            },
            // handleClick() {
                //  console.log("handle click", this.selectedUser)
                // document.querySelector('vue-advanced-chat').currentUserId = this.claims._id;
                // document.querySelector('vue-advanced-chat').rooms = this.rooms;
                // document.querySelector('vue-advanced-chat').messages = this.messages;
                // // create and fetch a room for chat with target user.
                // let room = axiosInstance.post(process.env.VUE_APP_USERGROUPS_API_ENDPOINT + "/new", {"users": [this.target_user]});
                // this.rooms = [room];
            // },

            // add() {
            //     // Emit the server side
            //     this.$socket.emit("add", { a: 5, b: 3 });
            // },
 
            // get() {
            //     this.$socket.emit("get", { id: 12 }, (response) => {
            //         console.log(response);
            //     });
            // }
        // },
    //     socket: {
    //         // Prefix for event names
    //         // prefix: "/counter/",

    //         // If you set `namespace`, it will create a new socket connection to the namespace instead of `/`
    //         namespace: "/message",
    //         events: {

    //             // Similar as this.$socket.on("changed", (msg) => { ... });
    //             // If you set `prefix` to `/counter/`, the event name will be `/counter/changed`
    //             //
    //             changed(msg) {
    //                 console.log("Something changed: " + msg);
    //             }

    //             /* common socket.io events
    //             connect() {
    //                 console.log("Websocket connected to " + this.$socket.nsp);
    //             },

    //             disconnect() {
    //                 console.log("Websocket disconnected from " + this.$socket.nsp);
    //             },

    //             error(err) {
    //                 console.error("Websocket error!", err);
    //             }
    //             */
    //         }
    //     }
    // }
        mounted: function() {
            document.querySelector('vue-advanced-chat').currentUserId = this.userid;
            document.querySelector('vue-advanced-chat').rooms = this.rooms;
            document.querySelector('vue-advanced-chat').messages = this.messages;
            // ('form#emit').submit(function(event) {
            //     socket.emit('event', {data: '#emit_data'});
            //     return false;
            // });
            // ('form#broadcast').submit(function(event) {
            //     socket.emit('broadcast', {data: '#broadcast_data'});
            //     return false;
            // });
            // ('form#disconnect').submit(function(event) {
            //     socket.emit('disconnect');
            //     return false;
            // });
        }
    }
}
</script>

<style scoped>
.chatwindow {
    padding-left: 20px;
}
</style>