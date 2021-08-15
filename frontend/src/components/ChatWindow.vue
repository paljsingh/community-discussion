<template>
    <div class='chatwindow'>
        <VueChat :current-user-id="currentUserId" :rooms="rooms" :messages="messages" />
    </div>
</template>

<script>
    // import Vue from 'vue';
    import VueChat from 'vue-advanced-chat'
    import 'vue-advanced-chat/dist/vue-advanced-chat.css'
    import io from "socket.io";
    import axiosInstance from '../helpers/interceptor';
    // import authHandler from '../auth/index.js';
    
    // import VueWebsocket from "vue-websocket";

    // Vue.use(VueWebsocket, process.env.VUE_APP_WEBSOCKET_API_ENDPOINT, {
    //     reconnection: false
    // });
    
    export default {
        name: 'Users',
        props: ['selected'],
        currentUserId: null,
        watch: {
            async selected() {
                let selectedUserId = this.selected[0]._id;
                let room = await axiosInstance.post(process.env.VUE_APP_USERGROUPS_API_ENDPOINT + "/new", {"user_ids": [selectedUserId]});
                let users = []
                console.log(room, room.data, room.data.users);

                room.data.users.forEach(function(user) {
                    console.log("adding user_id");
                    users.append(user._id);
                });
                this.rooms = [{'roomId': room.data._id, 'roomName': room.data.name, 'users': users}];
                console.log(this.rooms);
                // this.messages = 
                // document.querySelector('vue-advanced-chat').rooms = this.rooms;
                // document.querySelector('vue-advanced-chat').messages = this.messages;
                // document.querySelector('vue-advanced-chat').currentUserId = this.selected[0]._id;
                // create and fetch a room for chat with target user.
            }
        },
        components: {
            VueChat
        },
        data: function() {
            return {
                rooms: [],
                claims: {'_id': 1},
                currentUserId: 0,
                messages: [],
                    // {
                    //     _id: 7890,
                    //     content: 'message 1',
                    //     senderId: 1234,
                    //     username: 'John Doe',
                    //     avatar: 'assets/imgs/doe.png',
                    //     date: '13 November',
                    //     timestamp: '10:20',
                    //     system: false,
                    //     saved: true,
                    //     distributed: true,
                    //     seen: true,
                    //     deleted: false,
                    //     disableActions: false,
                    //     disableReactions: false,
                        // file: {
                        //   name: 'My File',
                        //   size: 67351,
                        //   type: 'png',
                        //   audio: true,
                        //   duration: 14.4,
                        //   url: 'https://firebasestorage.googleapis.com/...',
                        //   preview: 'data:image/png;base64,iVBORw0KGgoAA...'
                        // },
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
    width: 800px;
    left: 500px;
    top: 60px;  
}

</style>