import Vue from 'vue'
export default {
  state: {
    userData: {},
    forOnboardingNeeded: 10
  },
  mutations: {
    resetUser (state) {
      state.userData = {}
    },
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
    ratings: state => state.userData.ratings,
    // True if less than 3 games already rated
    onboarding: state =>
      !(state.userData.ratings &&
        state.userData.ratings.length >=
        state.forOnboardingNeeded),
    neededRatingsAmount: state => state.forOnboardingNeeded - state.userData.ratings.length
  }
}
