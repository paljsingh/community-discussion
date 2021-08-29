<template>
    <div class='chatwindow'>
        <VueChat :current-user-id="currentUserId" :rooms="rooms" :messages="messages"
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
    import io from "socket.io";
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
                currentUserId: 1234,
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
            async fetchData() {
                let selectedUserId = this.selected[0]._id;
                let selectedUserName = this.selected[0].name;

                // create a new room (or obtain one if already exists)
                let response = (await axiosInstance.post(process.env.VUE_APP_USERGROUPS_API_ENDPOINT + "/new", {"user_id": selectedUserId})).data;

                // map user ids to user names.
                let user_id_map = {}

                // response contains a usergroup/room structure with id/name/tags and users list.
                let usergroup_id = response._id
                response.users.forEach((user) => {
                    let u = {}
                    u._id = user._id
                    u.username = user.name
                    u.status = {
                        state: 'online'
                    }
                    this.users.push(u)
                    user_id_map[user._id] = user.name
                });
                
                // assign new room to vue-adv-chat rooms list.
                // let num_rooms = this.rooms.length
                let room = {
                    roomId: 1,
                    roomName: selectedUserName,
                    unreadCount: 0,     // hardcoded for now
                    index: 1,           // hardcoded for now
                    lastMessage: {'content': '' },  // hardcoded for now
                    users: this.users,
                    typingUsers: []     // TODO
                }
                // for performance, as suggested here - https://github.com/antoine92190/vue-advanced-chat
                this.rooms.push(room)
                // this.rooms = [...this.rooms]

                // fetch historical messages if any
                let messageApiUrl = process.env.VUE_APP_USERGROUPS_MESSAGES_API_ENDPOINT.replace('usergroup_id', usergroup_id)
                response = (await axiosInstance.get(messageApiUrl)).data;
                let count = 0
                response.data.forEach((message) => {
                    let m = {}
                    m._id = count
                    m.senderId = message.created_by
                    m.content = message.content?message.content:[]
                    m.username = user_id_map[message.created_by]
                    m.date = message.creation_date.substring(5, 15)     // TODO: parse date here
                    m.timestamp = message.creation_date.substring(17, 22)     // TODO: parse date here
                    m.file = {}
                    m.reactions = {}
                    this.messages.push(m);

                    count += 1
                });
            },
            fetchMessages({ room, options }) {
                console.log("fetch messages", room, options);
                this.messagesLoaded = false

                // use timeout to imitate async server fetched data
                setTimeout(() => {
                    this.messages = []
                    this.messagesLoaded = true
                })
            },
            sendMessageHandler(message) {
                console.log(message.content)
                console.log(message.file)
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
            document.querySelector('vue-advanced-chat').currentUserId = this.currentUserId
            document.querySelector('vue-advanced-chat').rooms = this.rooms
            document.querySelector('vue-advanced-chat').messages = this.messages
            let namespace = '/message';
            let socket = io(namespace, {transports: ['websocket'], upgrade: false});

            socket.on('connect', function() {
                socket.emit('event', {data: 'connected to the SocketServer...'});
            });

            socket.on('response', function(msg, cb) {
                console.log('<br>' + '<div/> logs #' + msg.count + ': ' + msg.data);
                if (cb)
                    cb();
            });
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
    /* background: #012; */
    position: fixed;
    width: 600px;
    left: 400px;
    top: 60px;  
}

</style>