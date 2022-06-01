import Vue from 'vue'
import Vuex from 'vuex'
import tickers from './modules/tickers'
import predict from './modules/predict'
import models from './modules/models'
import formData from './modules/formData'
import optimizers from './modules/optimizers'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    tickers,
    predict,
    models,
    formData,
    optimizers
  }
})
