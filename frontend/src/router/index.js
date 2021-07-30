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

import HomeComponent from '@/components/Home'

import { OktaAuth } from '@okta/okta-auth-js'
import OktaVue, { LoginCallback } from '@okta/okta-vue'
import authConfig from '@/config'
import store from '../store/index'

Vue.use(Router)

const oktaAuth = new OktaAuth(authConfig.oidc)

Vue.use(OktaVue, { oktaAuth })

const router = new Router({
  mode: 'history',
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
      props: {template_name: 'profile'},

    },
    {
      path: '/communities',
      component: HomeComponent,
      props: {template_name: 'communities'},
      meta: { 'isLoggedIn': true},
    },
    {
      path: '/usergroups',
      component: HomeComponent,
      props: {template_name: 'usergroups'},
      meta: { 'isLoggedIn': true},
    },
    {
      path: '/users',
      component: HomeComponent,
      props: {template_name: 'users'},
      meta: { 'isLoggedIn': true},
    },
    {
      path: '/dashboard',
      component: HomeComponent,
      props: {template_name: 'dashboard'},
      meta: { 'isLoggedIn': true, 'isOktaUser': true },
    },
    {
      path: '/profile',
      component: HomeComponent,
      props: { template_name: 'profile'},
      meta: { 'isLoggedIn': true},
    }
  ]
})


// ensure the require prequisites as mentioned by meta field are met, before loading this route.
router.beforeEach((to, from, next) => {
  let flag = true
  if (to.meta.isLoggedIn) {
    if (! store.state.account.token) {
      flag = false
    }
  }
  if (to.meta.isOktaUser) {
    if (! store.state.account.usertype === 'okta') {
      flag = false
    }
  }

  if (flag) {
    next()
  } else {
    next(false)
  }
})

export default router;