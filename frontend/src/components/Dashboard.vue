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

        <h4>User Groups</h4>
        <v-text-field single-line clearable dark label="Create user groups" v-model="num_usergroups" placeholder="5" />
        <button id="button-usergroups" class="ui primary button" role="button" v-on:click="create_usergroups()" >
            Go
        </button>
        <v-snackbar v-model="snackbar_usergroups" :timeout="timeout">
            Created {{this.num_usergroups}} usergroups.
        </v-snackbar>

        <h4>Create Communities</h4>
        <v-text-field single-line clearable dark label="Create communities" v-model="num_communities" placeholder="5" />
        <button id="button-communities" class="ui primary button" role="button" v-on:click="create_communities()" >
            Go
        </button>
        <v-snackbar v-model="snackbar_communities" :timeout="timeout">
            Created {{this.num_communities}} communities.
        </v-snackbar>

    </div>

</template>

<script>
    import axiosInstance from '../helpers/interceptor.js';
    import authHelper from '../helpers/auth.js';
    // import {VTextField, VSnackbar} from 'vuetify';


    export default {
        name: 'Dashboard',
        mixins: [authHelper],
        // components: {
        //     VTextField,
        //     VSnackbar
        // },
        data: function() {
            return {
                users: [],
                usergroups: [],
                communities: [],

                new_users: [],
                new_usergroups: [],
                new_communities: [],

                num_users: 0,
                num_usergroups: 0,
                num_communities: 0,

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
                        this.new_users.push(response.data);
                    }
                    this.num_users = this.new_users.length;
                    this.snackbar_users = true

                    // this.$router.push('/users')
                } catch (e) {
                    console.error(e)
                    this.failed = true
                }
            },
            async create_usergroups () {
                try {
                    for (var i=0; i<this.num_usergroups; i++) {
                        const response = await axiosInstance.post(process.env.VUE_APP_USERGROUPS_API_ENDPOINT + '/new')
                        console.log(response)
                        this.new_usergroups.push(response.data)
                    }
                    this.num_usergroups = this.new_usergroups.length;
                    this.snackbar_usergroups = true
                } catch (e) {
                    console.error(e)
                    this.failed = true
                }
            },
            async create_communities () {
                try {
                    for (var i=0; i<this.num_communities; i++) {
                        const response = await axiosInstance.post(process.env.VUE_APP_COMMUNITIES_API_ENDPOINT + '/new')
                        this.new_communities.push(response.data)
                    }
                    this.num_communities = this.new_communities.length;
                    this.snackbar_communities = true

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
