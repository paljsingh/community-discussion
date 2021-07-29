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
        <ChatWindow />
    </v-col>
</template>

<script>
    import Vue from 'vue';
    import Vuetable from 'vuetable-2';
    import axiosInstance from '../helpers/interceptor.js';
    import CopyToken from './CopyToken.vue';
    import ChatWindow from './ChatWindow.vue';
    Vue.component('vuetable', Vuetable);
    Vue.component('CopyToken', CopyToken);
    Vue.component('ChatWindow', ChatWindow);
    import authHandler from '../auth/index.js';

    
    export default {
        name: 'Users',
        mixins: [authHandler],
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
</style>