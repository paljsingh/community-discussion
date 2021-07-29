<template>
    <div class="chat">
        <v-card-title>
        john doe
        </v-card-title>
        <template v-for="msg in messages">
            <div :class="{ 'd-flex ': msg.me }">
            <v-menu offset-y>
                <template v-slot:activator="{ on }">
                <v-hover > <!-- v-slot:default="{ hover }"> -->
                    <v-chip :color="msg.me ? 'primary' : ''" dark style="height:auto;white-space: normal;" class="pa-4 mb-2" v-on="on">
                    {{ msg.content }}
                    <sub class="ml-2" style="font-size: 0.5rem;">{{ msg.created_at }}</sub>
                    <!-- <v-icon v-if="hover" small>
                        expand_more
                    </v-icon> -->
                    </v-chip>
                </v-hover>
                </template>
                <v-list>
                <v-list-item>
                    <v-list-item-title>delete</v-list-item-title>
                </v-list-item>
                </v-list>
                
            </v-menu>
            </div>
        </template>
        <v-card-text class="send-message">
            <v-text-field v-model="messageForm.content" label="type_a_message" type="text" no-details outlined append-outer-icon="send"
            @keyup.enter="messages.push(messageForm)" @click:append-outer="messages.push(messageForm)" hide-details />
        </v-card-text>
    </div>
</template>

<script>
import { defineComponent } from '@vue/composition-api'

export default defineComponent({
    setup() {
        
    },
    data: function() {
        return {
            activeChat: 1,
            parents: [
                {
                    id: 1,
                    title: "john doe",
                    active: true
                },
                {
                    id: 3,
                    title: "scarlett",
                    active: false
                },
                {
                    id: 4,
                    title: "scarlett",
                    active: false
                },
                {
                    id: 5,
                    title: "scarlett",
                    active: false
                },
                {
                    id: 6,
                    title: "scarlett",
                    active: false
                },
                {
                    id: 7,
                    title: "scarlett",
                    active: false
                },
                {
                    id: 8,
                    title: "scarlett",
                    active: false
                },
                {
                    id: 9,
                    title: "scarlett",
                    active: false
                },
                {
                    id: 10,
                    title: "scarlett",
                    active: false
                },
                {
                    id: 11,
                    title: "scarlett",
                    active: false
                },
                {
                    id: 12,
                    title: "scarlett",
                    active: false
                },
                {
                    id: 13,
                    title: "scarlett",
                    active: false
                },
                {
                    id: 14,
                    title: "scarlett",
                    active: false
                }
            ],
            messages: [
                {
                    content: "lorem ipsum",
                    me: true,
                    created_at: "11:11am"
                },
                {
                    content: "dolor",
                    me: false,
                    created_at: "11:11am"
                },
                {
                    content: "dolor",
                    me: false,
                    created_at: "11:11am"
                },
                {
                    content: "dolor",
                    me: false,
                    created_at: "11:11am"
                },
                {
                    content: "dolor",
                    me: true,
                    created_at: "11:11am"
                },
                {
                    content: "dolor",
                    me: false,
                    created_at: "11:12am"
                },
                {
                    content: "dolor",
                    me: false,
                    created_at: "11:14am"
                }
            ],
            messageForm: {
                content: "",
                me: true,
                created_at: "11:11am"
            }
        }
    }
});
</script>

<style scoped>
.chat {
    /* background: #012; */
    position: fixed;
    width: 800px;
    left: 450px;
    top: 60px;
    overflow: auto    
}
.send-message{
    background: #fff;
    position: fixed;
    width: 780px !important;
    left: 460px !important;
    top: 600px;
}
</style>