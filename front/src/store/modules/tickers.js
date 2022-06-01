import { api } from '../api'

export default {
  namespaced: true,
  state: {
    tickers: []
  },
  getters: {
    tickers: state => state.tickers
  },
  mutations: {
    UPDATE_TICKERS: (state, payload) => {
      state.tickers = payload
    }
  },
  actions: {
    getTickers: (state) => {
      return new Promise((resolve, reject) => {
        api.get('tickers/').then((response) => {
          state.commit('UPDATE_TICKERS', response.data)
          resolve(response.data)
        }).catch((error) => {
          reject(error)
        })
      })
    }
  }
}
