import { api } from '../api'

export default {
  namespaced: true,
  state: {
    optimizers: []
  },
  getters: {
    optimizers: state => state.optimizers
  },
  mutations: {
    UPDATE_OPTIMIZERS: (state, payload) => {
      state.optimizers = payload
    }
  },
  actions: {
    getOptimizers: (state) => {
      return new Promise((resolve, reject) => {
        api.get('optimizators/').then((response) => {
          state.commit('UPDATE_OPTIMIZERS', response.data)
          resolve(response.data)
        }).catch((error) => {
          reject(error)
        })
      })
    }
  }
}
