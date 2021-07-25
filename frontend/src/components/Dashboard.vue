<template>
    <div class="Dashboard">

        <p>List of communities</p>
        <div class="field" id="alert" v-if="new_users.length">
            <vuetable ref="vuetable"
                class="new-users"
                :api-url="'http://127.0.0.1:5000/api/v1/communities'"
                :fields="fields"
                :current-page="0"
                :per-page="20"
                filter=""
                data-path="data"
                pagination-path=""
                >
            </vuetable>
        </div>

        <h4>Create Dummy Users</h4>
        <label for="text-dummy-users">How many dummy users to create?</label>
        <input type="text" id="text-dummy-users" v-model="num_users" placeholder=num_users />
        <button id="button-dummy-users" class="ui primary button" role="button" v-on:click="create_users()" >
            Go
        </button>
    </div>
</template>

<script>
    import axiosInstance from '../helpers/interceptor.js';

    export default {
        name: 'Dashboard',
        data: function() {
            return {
                users: [],
                usergroups: [],
                communities: [],

                new_users: [],
                new_usergroups: [],
                new_communities: [],

                num_users: [],
                num_usergroups: [],
                num_communities: [],
            }
        },
        methods: {
            async create_users () {
                try {
                    for (var i=0; i<this.num_users; i++) {
                        const response = await axiosInstance.post(process.env.VUE_APP_USERS_API_ENDPOINT + '/new');
                        console.info(response.data)
                        this.new_users.push(response.data.users);
                    }
                } catch (e) {
                    console.error(e)
                    this.failed = true
                }
            },
            async create_user_groups () {
                try {
                    for (var i=0; i<self.num_users; i++) {
                        const response = await axiosInstance.post(process.env.VUE_APP_USER_GROUPS_API_ENDPOINT + '/new')
                        this.new_usergroups.append(response.data.usergroups)
                    }
                } catch (e) {
                    console.error(e)
                    this.failed = true
                }
            },
            async create_communities () {
                try {
                    for (var i=0; i<self.num_users; i++) {
                        const response = await axiosInstance.post(process.env.VUE_APP_COMMUNITIES_API_ENDPOINT + '/new')
                        this.new_communitiess.append(response.data.communities)
                    }
                } catch (e) {
                    console.error(e)
                    this.failed = true
                }
            }
        }
    };
</script>
