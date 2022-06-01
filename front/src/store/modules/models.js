import { api } from '../api'

export default {
  namespaced: true,
  state: {
    models: []
  },
  getters: {
    models: state => state.models
  },
  mutations: {
    UPDATE_MODELS: (state, payload) => {
      state.models = payload
    }
  },
  actions: {
    getModels: (state) => {
      return new Promise((resolve, reject) => {
        api.get('models/').then((response) => {
          state.commit('UPDATE_MODELS', response.data)
          resolve(response.data)
        }).catch((error) => {
          reject(error)
        })
      })
    }
  }
}
