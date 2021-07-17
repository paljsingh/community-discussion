<template>

    <div class="users">
        <vuetable ref="vuetable"
            class="new-users"
            :api-url="api_url"
            :fields="fields"
            :current-page="0"
            :per-page="20"
            filter=""
            data-path="data"
            pagination-path=""
            :http-fetch="myFetch"
            >
        </vuetable>
    </div>
</template>

<script>
    import Vuetable from 'vuetable-2';
    import Vue from 'vue';
    import axios from 'axios';
    import axiosInstance from '../helpers/interceptor.js'
    Vue.component('vuetable', Vuetable);

    export default {
        name: 'Users',
        data: function() {
            return {
                all_users: [],
                api_url: process.env.VUE_APP_USERS_API_ENDPOINT,
                fields: [
                    {
                      name: 'name',
                      title: 'User Name'
                    },
                    {
                      name: 'email',
                      title: 'Email'
                    },
                    {
                      name: 'token',
                      title: 'JWT Token'
                    }
                ],
                httpOptions: {
                    headers: this.$auth_header
                }
            }
        },
        methods: {
            async get_all_users () {
                try {
                    const response = await axios.get(this.api_url)
                    this.all_users = response.data.user
                } catch (e) {
                    console.error(e)
                    this.failed = true
                }
            },
            async myFetch(apiUrl) {    // eslint
                return await axiosInstance.get(apiUrl)

            },
        }
    };

</script>

<style scoped>
.users {
    position: relative;
    float: left;
    width: 80%;
}
</style>