/*!
* Copyright (c) 2018-Present, Okta, Inc. and/or its affiliates. All rights reserved.
* The Okta software accompanied by this notice is provided pursuant to the Apache License, Version 2.0 (the "License.")
*
* You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0.
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
* WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
*
* See the License for the specific language governing permissions and limitations under the License.
*/

<template>
    <div class="home" id="home">
        <div v-if="!this.token" class="intro">
            <div class="logo">
                <img class="image" src="@/assets/logo.png" />
            </div>
            <div class="elem">
                <p>
                    The c18n app is a PoC app to demonstrate <br/>
                    a community discussion platform using the <br/>
                    stream processing applications.<br/>
                </p>
                <v-btn v-on:click="login">
                    Login with Okta
                </v-btn>
                <v-tooltip bottom>
                    <template v-slot:activator="{ on, attrs }">
                        <v-icon color="primary" dark v-bind="attrs" v-on="on">mdi-information</v-icon>
                    </template>
                    <p>
                        Users authenticated with okta sso are treated as admin users.
                        <br/>
                        Admin users can access the dashboard and create communities, user groups and dummy users.
                    </p>
                </v-tooltip>
            </div>

            <div class="elem">or</div>

            <div data-app>
                <div class="elem">
                    <v-text-field dark ref="jwt_token" label="Paste JWT Token" outlined clearable ></v-text-field>
                    <v-btn v-on:click="login_dummy">
                        Impersonate a Dummy User
                    </v-btn>
                    <v-tooltip bottom>
                        <template v-slot:activator="{ on, attrs }">
                            <v-icon color="primary" dark v-bind="attrs" v-on="on">mdi-information</v-icon>
                        </template>
                        <p>
                            Dummy users are fake users with randomized ids and auto-generated JWT tokens.<br/>
                            The backend application assigns these users with role having limited capabilities<br/>
                            (e.g. send direct messages to other users or user groups.)<br/>
                            The JWT tokens of the dummy users are visible to the admin user on the dashboard.<br/>
                            It is advisable to use an 'incognito window' for impersonating multiple dummy users.
                        </p>
                    </v-tooltip>
                </div>
            </div>
        </div> <!-- !isAuthenticated -->

        <div v-if="this.token" class="content">
            <Navigation />
            <Communities v-if="template_name === 'communities'"/>
            <UserGroups v-if="template_name === 'usergroups'"/>
            <Users v-if="template_name === 'users'"/>
            <Dashboard v-if="template_name === 'dashboard'"/>
            <Profile v-if="template_name === 'profile'"/>
        </div>
    </div>
</template>

<script>
// import Vue from 'vue'
import Navigation from './Navigation.vue'
import Communities from './Communities.vue'
import UserGroups from './UserGroups.vue'
import Users from './Users.vue'
import Dashboard from './Dashboard.vue'
import Profile from './Profile.vue'
import authHandler from '../auth/index.js';

export default {
    name: 'home',
    props: ['template_name'],
    mixins: [authHandler],
    components: {
        Navigation,
        Communities,
        UserGroups,
        Users,
        Dashboard,
        Profile
    },
    data: function () {
        return {
            claims: '',
            activetab: 'users',
        }
    },
}

</script>

<style scoped>
.home {
    text-align: left;
    padding: 0px;
    margin: 0px;
}
.home .intro {
    position: fixed;
    width: 30% !important;
    left: 350px !important;
    top: 100px;
}
.home .content {
    top: 100px;
    position: fixed;
    height: 100% !important;
    width: 100% !important;
}
.logo {
    position: fixed;
    max-width: 500px;
    display: block;
    top: 25%;
    right: 10%;
    margin-right: 10px;
}
img {
    max-width:100%;
    max-height:100%;
}
.elem {
    margin-bottom:30px;
    margin-top:30px;
}
</style>