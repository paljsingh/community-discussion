const state = {
  token: null,
  claims: null,
  usertype: null,
};

const mutations = {
  logout(state) {
    state.token = null;
    state.claims = null;
  },
  login(state, token) {
    state.token = token;
  },
  claims(state, claims) {
      state.claims = claims
  },
  usertype(state, usertype) {
    state.usertype = usertype
  }
};

export default {
  state,
  mutations
}