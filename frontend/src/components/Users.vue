<template>
    <v-col class="users">
        <v-card dark>
            <v-card-title dark>
                <v-text-field
                    v-model="search"
                    append-icon="mdi-magnify"
                    label="Search"
                    single-line
                    hide-details
                    dark
                ></v-text-field>
            </v-card-title>
            <v-data-table
                :items="items"
                :headers="headers"
                :options.sync="options"
                :server-items-length="total"
                hide-default-header
                class="elevation-1"
                loading
                loading-text="Loading... Please wait"
                dense
                :search="search"
                :footer-props="{
                    'items-per-page-text':'',
                    'items-per-page-options': []
                }"
                @update:pagination="handlePageChange"
                dark
            >
                <template v-slot:[`item.token`]="{item}">
                    <CopyToken :item="item" usertype="" />
                </template>
            </v-data-table>
        </v-card>
        <div class="chatwindow">
            <chat-window :current-user-id="currentUserId" :rooms="rooms" single-room :messages="messages"/>
        </div>
    </v-col>
</template>

<script>
    import axiosInstance from '../helpers/interceptor.js';
    import CopyToken from './CopyToken.vue';
    import authHandler from '../auth/index.js';
    import ChatWindow from 'vue-advanced-chat'
    import 'vue-advanced-chat/dist/vue-advanced-chat.css'
    
    export default {
        name: 'Users',
        mixins: [authHandler],
        components: {
            CopyToken,
            ChatWindow    
        },
        watch: {
            options: {
                handler() {
                    this.fetchData();
                },
                deep: true
            }
        },
        data: function() {
            return {
                items: [],
                headers: [
                    {
                        text: 'User',
                        value: 'name',
                    },
                    {
                        text: 'Copy JWT Token',
                        value: 'token',
                    }
                ],
                apiUrl: process.env.VUE_APP_USERS_API_ENDPOINT,
                search: "",
                options: {},
                total: 0,
                rooms: [{
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
    },
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
    ],
    typingUsers: [ 4321 ]
  }],
                currentUserId: 1234,
                messages: [{
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
    }
  }
            ],

            }
        },
        methods: {
            async fetchData() {
                let response = (await axiosInstance.get(this.apiUrl, {params: this.options})).data;
                this.items = response.data;
                this.total = response.pagination.total;
                this.size = response.pagination.size;
            },
            handlePageChange(value) {
                console.log(value)
                this.page = value;
            },
            mounted() {
                document.querySelector('vue-advanced-chat').currentUserId = this.currentUserId
                document.querySelector('vue-advanced-chat').rooms = this.rooms
                document.querySelector('vue-advanced-chat').messages = this.messages
            }
        }
    };

</script>

<style scoped>
.users {
    position: fixed;
    width: 250px;
    left: 200px;
    top: 60px;
    font-size: 12px;
    /* background: #000; */
}
.chatwindow {
    /* background: #012; */
    position: fixed;
    width: 800px;
    left: 450px;
    top: 60px;  
}

</style>