import Vue from 'vue'

export default {
  state: {
    recommendations: []
  },
  mutations: {
    resetRecommendations (state) {
      state.recommendations = []
    },
    setRecommendations (state, rec) {
      state.recommendations = rec
    }
  },
  actions: {
    async retrieveRecommendations ({ commit }) {
      try {
        const res = await Vue.prototype.$http.get('/recommendations')
        commit('setRecommendations', res.data.recommendations)
      } catch (err) {
        commit('authError', err.message)
      }
    }
  },
  getters: {
    recommendations: state => state.recommendations,
    recommendationsLoaded: state => {
      return !!state.recommendations.length
    }
  }
}
