import Vue from 'vue'

export default {
  state: {
    status: '',
    recommendations: []
  },
  mutations: {
    resetRecommendations (state) {
      state.recommendations = []
    },
    setRecommendations (state, rec) {
      state.recommendations = rec
    },
    setStatus (state, status) {
      state.status = status
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
    async initialize ({ commit }) {
      commit('setStatus', 'initializing')
      try {
        const res = await Vue.prototype.$http.get('/initModel')
        commit('setStatus', res.data)
      } catch (err) {
        commit('authError', err.message)
      } finally {
        commit('setStatus', 'finished')
      }
    },
    async retrieveRecommendations ({ commit, dispatch }) {
      try {
        const res = await Vue.prototype.$http.get('/recommendations')
        if (res.data.message === 'Model is not initialized. Please do so with /initModel') {
          dispatch('initialize')
        } else { commit('setRecommendations', res.data.recommendations) }
      } catch (err) {
        commit('authError', err.message)
      }
    }
  },
  getters: {
    recommendations: state => state.recommendations,
    recommendationsLoaded: state => {
      return state.recommendations ? !!state.recommendations.length : false
    }
  }
}
