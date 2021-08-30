<template>
    <v-col class="content">
        <div class="col1">
            <v-card dark>
                <v-card-title dark>
                    <v-text-field
                        v-model="search"
                        append-icon="mdi-magnify"
                        label="Search"
                        single-line
                        hide-details
                        v-on:change="this.fetchData"
                        dark
                    ></v-text-field>
                </v-card-title>
                <v-data-table
                    :items="items"
                    :headers="headers"
                    :options.sync="options"

                    :single-select="singleSelect"
                    item-key="name"
                    v-model="selected"

                    class="elevation-1"
                    :footer-props="{
                        'items-per-page-text':'',
                        'items-per-page-options': []
                    }"
                    :server-items-length="total"
                    @update:pagination="handlePageChange"
                    @click:row="handleClick"

                    :loading-text="loading_text"
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
        </div>
        <div class="col2">
            <ChatWindow :selected="selected" />
        </div>
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
                loading_text: "Loading... Please wait",
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
                total: 0,
                page: 1,
                perPage: 10,
                options: {}
            }
        },
        methods: {
            async fetchData() {
                let params = Object.assign({}, this.options, {'name': this.search});
                let response = (await axiosInstance.get(this.apiUrl, {params: params})).data;
                this.items = response.data;

                this.total = response.pagination.total;
                this.size = (response.pagination.total-1) / response.pagination.page + 1;

                if (this.total == 0) {
                    this.loading_text = "no users."
                }
            },
            handlePageChange(value) {
                this.page = value;
            },
            handleClick(selectedUser) {
                this.selected = [selectedUser];
            },
        }
    };

</script>

<style scoped>
.content {
    position: relative;
    left: 10px;
}
.col1 {
    position: relative;
    width: 20%;
    float: left;
    margin: 20px 0px 20px 0px;
}
.col2 {
    position: relative;
    float: left;
    width: 70%;
    margin: 20px 0px 20px 0px;
}
</style>