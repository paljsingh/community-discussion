<template>

    <div class="users">
        <vuetable ref="vuetable"
            class="new-users"
            :api-url="'http://127.0.0.1:5000/api/v1/users'"
            :fields="fields"
            :current-page="0"
            :per-page="20"
            filter=""
            data-path="data"
            pagination-path=""
            >
        </vuetable>
    </div>
</template>

<script>
    import axios from 'axios';
    import Vuetable from 'vuetable-2';
    import Vue from 'vue';
    Vue.component('vuetable', Vuetable);

    export default {
        name: 'Users',
        data: function() {
            return {
                all_users: [],
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
                ]
            }
        },
        methods: {
            async get_all_users () {
                try {
                    const response = await axios.get(process.env.VUE_APP_USERS_API_ENDPOINT)
                    this.all_users = response.data.user
                } catch (e) {
                    console.error(e)
                    this.failed = true
                }
            }
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