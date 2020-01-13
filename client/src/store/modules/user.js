import Vue from 'vue'
export default {
  state: {
    userData: {}
  },
  mutations: {
    setUser (state, user) {
      state.userData = user
    }
  },
  actions: {
    async retrieveUserData ({ commit }) {
      try {
        const res = await Vue.prototype.$http.get('/user')
        commit('setUser', res.data.user)
      } catch (err) {
        commit('authError', err.message)
      }
    }
  },
  getters: {
    ratings: state => state.userData.ratings
  }
}
