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

import Vue from 'vue'
import Router from 'vue-router'
import 'semantic-ui-css/semantic.min.css'

import HomeComponent from '../components/Home.vue'
import ProfileComponent from '../components/Profile.vue'
import UsersComponent from '../components/Users.vue'
import UserGroupsComponent from '../components/UserGroups.vue'
import CommunitiesComponent from '../components/Communities.vue'
import AdminComponent from '../components/Admin.vue'

import { OktaAuth } from '@okta/okta-auth-js'
import OktaVue, { LoginCallback } from '@okta/okta-vue'
import authConfig from '@/config'

Vue.use(Router)

const oktaAuth = new OktaAuth(authConfig.oidc)

Vue.use(OktaVue, { oktaAuth })

const router = new Router({
  mode: 'history',
  components: {
    HomeComponent,
    ProfileComponent,
    UsersComponent,
    UserGroupsComponent,
    CommunitiesComponent,
    AdminComponent
  },
  routes: [
    {
      // handles OAuth callback
      path: '/login/callback',
      component: LoginCallback
    },
    // default path
    {
      path: '/',
      component: HomeComponent,
    },
    {
      path: '/communities',
      component: CommunitiesComponent,
      meta: { 'isLoggedIn': true},
    },
    {
      path: '/usergroups',
      component: UserGroupsComponent,
      meta: { 'isLoggedIn': true},
    },
    {
      path: '/users',
      component: UsersComponent,
      meta: { 'isLoggedIn': true},
    },
    {
      path: '/admin',
      component: AdminComponent,
      meta: { 'isLoggedIn': true, 'isOktaUser': true },
    },
    {
      path: '/profile',
      component: ProfileComponent,
      meta: { 'isLoggedIn': true},
    }
  ]
})


router.beforeEach(async (to, from, next) => {
  if (to.matched.some((record) => record.meta.isLoggedIn)) {
      if (isAuthenticated()) {
          next()
      } else {
          next('/')
      }
  } else {
      next()
  }
})

function isAuthenticated() {
  let authenticated = false
  if(localStorage.getItem('dummy-jwt-token')) {
      authenticated = true
  } else if (localStorage.getItem('okta-token-storage')) {
      authenticated = true
  }
  return authenticated
}

export default router;