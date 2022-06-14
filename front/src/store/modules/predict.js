import { api } from '../api'

export default {
  namespaced: true,
  state: {
    labels: [],
    values: [],
    other: 0,
    error: null,
    otherLabels: [],
    sectorLabels: [],
    sectorValues: [],
    seriesStocks: [],
    xAnnotationStocks: null,
    xAxisStocks: [],
    expectedAnnualReturn: null,
    annualVolatility: null,
    sharpeRatio: null
  },
  getters: {
    labels: state => state.labels,
    values: state => state.values,
    other: state => state.other,
    error: state => state.error,
    otherLabels: state => state.otherLabels,
    sectorLabels: state => state.sectorLabels,
    sectorValues: state => state.sectorValues,
    seriesStocks: state => state.seriesStocks,
    xAnnotationStocks: state => state.xAnnotationStocks,
    xAxisStocks: state => state.xAxisStocks,
    expectedAnnualReturn: state => state.expectedAnnualReturn,
    annualVolatility: state => state.annualVolatility,
    sharpeRatio: state => state.sharpeRatio
  },
  mutations: {
    UPDATE_LABELS: (state, payload) => {
      state.labels = payload
    },
    UPDATE_VALUES: (state, payload) => {
      state.values = payload
    },
    UPDATE_OTHER: (state, payload) => {
      state.other = payload
    },
    UPDATE_ERROR: (state, detail) => {
      state.error = detail
    },
    CLEAR_ERROR: (state) => {
      state.error = null
    },
    UPDATE_OTHER_LABELS: (state, payload) => {
      state.otherLabels = payload
    },
    UPDATE_SECTOR_LABELS: (state, payload) => {
      state.sectorLabels = payload
    },
    UPDATE_SECTOR_VALUES: (state, payload) => {
      state.sectorValues = payload
    },
    UPDATE_SERIES_STOCKS: (state, payload) => {
      state.seriesStocks = payload
    },
    UPDATE_X_ANNOTATIONS_STOCKS: (state, payload) => {
      state.xAnnotationStocks = payload
    },
    UPDATE_X_AXIS_STOCKS: (state, payload) => {
      state.xAxisStocks = payload
    },
    UPDATE_EXPECTED_ANNUAL_RETURN: (state, payload) => {
      state.expectedAnnualReturn = payload
    },
    UPDATE_ANNUAL_VOLATILITY: (state, payload) => {
      state.annualVolatility = payload
    },
    UPDATE_SHARPE_RATIO: (state, payload) => {
      state.sharpeRatio = payload
    }
  },
  actions: {
    getPredict: (state, params) => {
      return new Promise((resolve, reject) => {
        api.get('predict/', { params }).then((response) => {
          state.commit('UPDATE_LABELS', response.data.labels)
          state.commit('UPDATE_VALUES', response.data.values)
          state.commit('UPDATE_OTHER', response.data.other)
          state.commit('UPDATE_OTHER_LABELS', response.data.other_labels)
          state.commit('UPDATE_SECTOR_LABELS', response.data.labels_sector)
          state.commit('UPDATE_SECTOR_VALUES', response.data.values_sector)
          state.commit('UPDATE_SERIES_STOCKS', response.data.series_stocks)
          state.commit('UPDATE_X_ANNOTATIONS_STOCKS', response.data.x_annotations_stocks)
          state.commit('UPDATE_X_AXIS_STOCKS', response.data.xaxis_stocks)
          state.commit('UPDATE_EXPECTED_ANNUAL_RETURN', response.data.expected_annual_return)
          state.commit('UPDATE_ANNUAL_VOLATILITY', response.data.annual_volatility)
          state.commit('UPDATE_SHARPE_RATIO', response.data.sharpe_ratio)
          resolve(response.data)
        }).catch((error) => {
          state.commit('UPDATE_ERROR', error.response.data.detail.error)
          state.commit('UPDATE_SERIES_STOCKS', error.response.data.detail.series_stocks)
          state.commit('UPDATE_X_ANNOTATIONS_STOCKS', error.response.data.detail.x_annotations_stocks)
          state.commit('UPDATE_X_AXIS_STOCKS', error.response.data.detail.xaxis_stocks)
          reject(error.response.data)
        })
      })
    },
    clearError: (state) => {
      state.commit('CLEAR_ERROR')
    }
  }
}
