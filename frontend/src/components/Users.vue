<template>

    <div class="users">
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
                    <input type="text" v-model="item.token" hidden>
                    <v-btn type="button" v-clipboard:copy="item.token" @click="snackbar = true">
                        <v-icon dark>mdi-content-copy</v-icon>
                    </v-btn>
                    <v-snackbar v-model="snackbar" :timeout="timeout">
                        Token Copied to clipboard.
                    </v-snackbar>
                </template>
            </v-data-table>
        </v-card>
    </div>
</template>

<script>
    import Vue from 'vue';
    import Vuetable from 'vuetable-2';
    import VueClipboard from 'vue-clipboard2';
    import axiosInstance from '../helpers/interceptor.js'
    Vue.component('vuetable', Vuetable);
    VueClipboard.config.autoSetContainer = true
    Vue.use(VueClipboard)
    
    export default {
        name: 'Users',
        props: {
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
                snackbar: false,
                timeout: 1000,
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
            // transform(record) {
            //     return {
            //         name: record.name,
            //         token: record.token.substr(0, 50),
            //     };
            // },
            onCopy(e) {
                e.info.hidden = false;
            },
        }
    };

</script>

<style scoped>
.users {
    position: relative;
    float: left;
    width: 20%;
    font-size: 12px;
    /* background: #000; */
}
</style>