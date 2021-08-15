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
                :search="search"
                :options.sync="options"
                :server-items-length="total"
                :single-select="singleSelect"
                item-key="name"
                v-model="selected"
                class="elevation-1"
                :footer-props="{
                    'items-per-page-text':'',
                    'items-per-page-options': []
                }"
                @update:pagination="handlePageChange"
                @click:row="handleClick"
                loading-text="Loading... Please wait"
                loading: true
                hide-default-header
                dark
                dense
            >
                <template v-slot:[`item.token`]="{item}">
                    <CopyToken :item="item" />
                </template>
            </v-data-table>
        </v-card>
        <ChatWindow :selected="selected" />
    </v-col>
</template>

<script>
    import axiosInstance from '../helpers/interceptor.js';
    import CopyToken from './CopyToken.vue';
    import authHelper from '../helpers/auth.js';
    import ChatWindow from './ChatWindow.vue'; 

    export default {
        name: 'Users',
        mixins: [authHelper],
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
            },
        },
        data: function() {
            return {
                items: [],
                singleSelect: false,
                selected: [],
                headers: [
                    {
                        text: 'User',
                        value: 'name',
                        filterable: true,
                    },
                    {
                        text: 'Copy JWT Token',
                        value: 'token',
                        filterable: false,
                    }
                ],
                apiUrl: process.env.VUE_APP_USERS_API_ENDPOINT,
                search: "",
                options: {},
                total: 0,
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
            handleClick(selectedUser) {
                this.selected = [selectedUser];
            },

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
</style>