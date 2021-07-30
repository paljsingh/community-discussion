<template>
    <div class='chatwindow'>
        <VueChat :current-user-id="currentUserId" :rooms="rooms" single-room :messages="messages"/>
    </div>
</template>

<script>
    import Vue from 'vue';
    import VueChat from 'vue-advanced-chat'
    import 'vue-advanced-chat/dist/vue-advanced-chat.css'
    import authHandler from '../auth/index.js';
    import VueWebsocket from "vue-websocket";

    Vue.use(VueWebsocket, process.env.VUE_APP_WEBSOCKET_API_ENDPOINT, {
        reconnection: false
    });
    
    export default {
        name: 'Users',
        mixins: [authHandler],
        components: {
            VueChat
        },
        data: function() {
            return {
                rooms: [
                    {
                        roomId: 1,
                        roomName: 'Room 1',
                        avatar: 'assets/imgs/people.png',
                        unreadCount: 4,
                        index: 3,
                        lastMessage: {
                            content: 'Last message received',
                            senderId: 1234,
                            username: 'John Doe',
                            timestamp: '10:20',
                            saved: true,
                            distributed: false,
                            seen: false,
                            new: true
                        },  // last message
                        users: [
                            {
                                _id: 1234,
                                username: 'John Doe',
                                avatar: 'assets/imgs/doe.png',
                                status: {
                                    state: 'online',
                                    lastChanged: 'today, 14:30'
                                }
                            },
                            {
                                _id: 4321,
                                username: 'John Snow',
                                avatar: 'assets/imgs/snow.png',
                                status: {
                                    state: 'offline',
                                    lastChanged: '14 July, 20:00'
                                }
                            }
                        ],  // users
                        typingUsers: [ 4321 ]
                    }   // room1
                ],  // rooms
                currentUserId: 1234,
                messages: [
                    {
                        _id: 7890,
                        content: 'message 1',
                        senderId: 1234,
                        username: 'John Doe',
                        avatar: 'assets/imgs/doe.png',
                        date: '13 November',
                        timestamp: '10:20',
                        system: false,
                        saved: true,
                        distributed: true,
                        seen: true,
                        deleted: false,
                        disableActions: false,
                        disableReactions: false,
                        // file: {
                        //   name: 'My File',
                        //   size: 67351,
                        //   type: 'png',
                        //   audio: true,
                        //   duration: 14.4,
                        //   url: 'https://firebasestorage.googleapis.com/...',
                        //   preview: 'data:image/png;base64,iVBORw0KGgoAA...'
                        // },
                        reactions: {
                            wink: [
                                1234, // USER_ID
                                4321
                            ],
                            laughing: [
                                1234
                            ]
                        }   // reaction 1
                    }   // message 1
                ],     // messages
            };  // return data
        },   // data
        methods: {
            created() {
                document.querySelector('vue-advanced-chat').currentUserId = this.currentUserId
                document.querySelector('vue-advanced-chat').rooms = this.rooms
                document.querySelector('vue-advanced-chat').messages = this.messages
            },
            add() {
                // Emit the server side
                this.$socket.emit("add", { a: 5, b: 3 });
            },
 
            get() {
                this.$socket.emit("get", { id: 12 }, (response) => {
                    console.log(response);
                });
            }
        },
        socket: {
            // Prefix for event names
            // prefix: "/counter/",

            // If you set `namespace`, it will create a new socket connection to the namespace instead of `/`
            namespace: "/message",
            events: {

                // Similar as this.$socket.on("changed", (msg) => { ... });
                // If you set `prefix` to `/counter/`, the event name will be `/counter/changed`
                //
                changed(msg) {
                    console.log("Something changed: " + msg);
                }

                /* common socket.io events
                connect() {
                    console.log("Websocket connected to " + this.$socket.nsp);
                },

                disconnect() {
                    console.log("Websocket disconnected from " + this.$socket.nsp);
                },

                error(err) {
                    console.error("Websocket error!", err);
                }
                */
            }
        }
    }
</script>