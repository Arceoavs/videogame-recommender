import Vue from 'vue'

function concanateSting ({ offset, limit }) {
  let url = '/games'
  if (offset || limit) {
    url += '?'
    if (offset) url += 'offset=' + offset + '&'
    if (limit) url += 'limit=' + limit
  }
  console.log(url)
  return url
}
export default {
  state: {
    games: []
  },
  mutations: {
    resetGames (state) {
      state.games = []
    },
    setGames (state, games) {
      state.games = games
    }
  },
  actions: {
    async retrieveGames ({ commit }, { offset, limit }) {
      try {
        const res = await Vue.prototype.$http.get(concanateSting({ offset, limit }))
        commit('setGames', res.data.data)
      } catch (err) {
        commit('authError', err.message)
      }
    }
  },
  getters: { games: state => state.games }
}
