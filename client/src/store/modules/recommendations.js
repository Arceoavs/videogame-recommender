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
    },
    hideRecommendation (state, recommendationId) {
      // Do not include recommendation any more
      // Even before re-retrieving
      for (var i = 0; i < state.recommendations.length; i++) {
        if (state.recommendations[i].id === recommendationId) {
          state.recommendations.splice(i, 1)
        }
      }
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
