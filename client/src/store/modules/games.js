import Vue from 'vue'

function concanateSting ({ offset, limit }) {
  let url = '/games'
  if (offset || limit) {
    url += '?'
    if (offset) url += 'offset=' + offset + '&'
    if (limit) url += 'limit=' + limit
  }
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
    },
    addGames (state, games) {
      // All games that are not already in the list
      state.games.push(
        ...games.filter(
          game => !state.games.find(
            g => g.id === game.id)))
    }
  },
  actions: {
    async retrieveGames ({ commit, dispatch }, { offset, limit }) {
      try {
        const res = await Vue.prototype.$http.get(
          concanateSting({ offset, limit }))
        commit('addGames', res.data.data)
      } catch (err) {
        commit('authError', err.message)
      }
    },
    async loadNext ({ dispatch, getters }) {
      await dispatch('retrieveGames',
        { offset: getters.range.max, limit: 10 })
    },
    async loadPrev ({ dispatch, getters }) {
      await dispatch('retrieveGames',
        { offset: getters.range.min - 2, limit: 1 })
    }
  },
  getters: {
    games: state => state.games,
    sortedGames: state => state.games.sort((a, b) => a.id - b.id),
    range: state => {
      return { max: Math.max(...state.games.map(o => o.id), 0),
        min: Math.min(...state.games.map(o => o.id), Number.MAX_SAFE_INTEGER) }
    }
  }
}
