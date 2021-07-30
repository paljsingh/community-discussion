<template>
    <div class="dashboard" v-if="this.usertype === 'okta'">
        <h4>Create Dummy Users</h4>
        <v-text-field single-line clearable dark label="Create users" v-model="num_users" placeholder="5" />
        <button id="button-dummy-users" class="ui primary button" role="button" v-on:click="create_users()" >
            Go
        </button>
        <v-snackbar v-model="snackbar_users" :timeout="timeout">
            Created {{this.num_users}} users.
        </v-snackbar>


        <h4>Create Communities</h4>
        <v-text-field single-line clearable dark label="Create communities" v-model="num_communities" placeholder="5" />
        <button id="button-communities" class="ui primary button" role="button" v-on:click="create_communities()" >
            Go
        </button>
        <v-snackbar v-model="snackbar_communities" :timeout="timeout">
            Created {{this.num_users}} communities.
        </v-snackbar>

        <h4>User Groups</h4>
        <v-text-field single-line clearable dark label="Create user groups" v-model="num_usergroups" placeholder="5" />
        <button id="button-usergroups" class="ui primary button" role="button" v-on:click="create_usergroups()" >
            Go
        </button>
        <v-snackbar v-model="snackbar_usergroups" :timeout="timeout">
            Created {{this.num_users}} usergroups.
        </v-snackbar>
    </div>

</template>

<script>
    import axiosInstance from '../helpers/interceptor.js';
    import authHandler from '../auth/index.js';


    export default {
        name: 'Dashboard',
        mixins: [authHandler],

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

                snackbar_users: false,
                snackbar_communities: false,
                snackbar_usergroups: false,
                timeout: 1000,

            }
        },
        methods: {
            async create_users () {
                console.log(this.num_users);
                this.new_users = [];
                try {
                    for (var i=0; i<this.num_users; i++) {
                        const response = await axiosInstance.post(process.env.VUE_APP_USERS_API_ENDPOINT + '/new');
                        console.info(response.data)
                        this.new_users.push(response.data.users);
                    }
                    this.num_users = this.new_users.length;
                    this.snackbar_users = true

                    // this.$router.push('/users')
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

<style scoped>
.dashboard {
    position: fixed;
    width: 250px;
    left: 250px;
    top: 60px;
    font-size: 12px;
    /* background: #000; */
}

</style>
