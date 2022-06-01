export default {
  namespaced: true,
  state: {
    data: {
      dateFrom: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10),
      dateTo: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10),
      selectedTickers: null,
      monthCount: 10,
      amount: 1000,
      selectModel: null,
      selectOptimizer: null
    }
  },
  getters: {
    data: state => state.data
  },
  mutations: {
    UPDATE_DATA: (state, userData) => {
      state.data = userData
    }
  },
  actions: {
    saveData: (state, data) => {
      state.commit('UPDATE_DATA', data)
    }
  }
}
