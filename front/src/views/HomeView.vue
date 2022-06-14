<template lang="pug">
  v-container(:fill-height="isLoad" :fluid="isLoad")
    template(v-if="isLoad")
      v-row(align="center" justify="center")
        v-col.text-subtitle-1.text-center(cols="12") Предсказание загружается...
        v-progress-circular(
          :size="300"
          :width="10"
          color="purple"
          indeterminate
          v-if="isLoad"
        )
    template(v-else)
      v-row
        v-col
          h3 Форма составления портфеля
      v-row
        v-col
          v-tooltip(bottom)
            template(v-slot:activator="{ on, attrs }")
              v-icon(v-bind="attrs" v-on="on") mdi-lightbulb-question
            div.tl
              h7 Инструкция использования:
              ol
                li Выберите даты в рамках которых будут выгружены графики акций.
                li Выберите тикеры интересующих компаний.
                li Укажите сумму инвестирования в рублях.
                li Выберите модель предсказания (нейронная сеть или временные ряды)
                li Выберите критерий подбора акций (Коэффициент шарпа - больший риск и больший доход, минимальная волатильность - меньший риск и меньший доход)
                li Введите срок прогнозирования в месяцах (рекомендуемый промежуток 10-12 месяцев)
              p На выходе будет получена статистика по собранному портфелю.
              i Учтите, что сервис работает только с российскими акциями.
              br
              i Аналитика сервиса не является индивидуальной инвестиционной рекомендацией.
      v-row
        v-col(
          cols="4"
        )
          v-form(v-model="isValid" ref="mainForm")
            // Дата начала
            v-menu(
              ref="dateFromPickerMenu"
              v-model="dateFromPickerMenu"
              :close-on-content-click="false"
              :return-value.sync="dateFrom"
              transition="scale-transition"
              offset-y
              min-width="auto"
            )
              template(v-slot:activator="{ on, attrs }")
                v-text-field(
                  :value="computedDateFrom"
                  clearable
                  label="С какой даты выгрузить данные"
                  readonly
                  v-bind="attrs"
                  v-on="on"
                  :rules="dateRules"
                  @click:clear="dateFrom = null"
                )
              v-date-picker(
                v-model="dateFrom"
                no-title
                scrollable
                :max="dateTo || (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10)"
                locale="ru-RU"
                first-day-of-week=1
              )
                v-spacer
                v-btn(text @click="dateFromPickerMenu = false") Cancel
                v-btn(text @click="$refs.dateFromPickerMenu.save(dateFrom)") OK
            // Дата конца
            v-menu(
              ref="dateToPickerMenu"
              v-model="dateToPickerMenu"
              :close-on-content-click="false"
              :return-value.sync="dateTo"
              transition="scale-transition"
              offset-y
              min-width="auto"
            )
              template(v-slot:activator="{ on, attrs }")
                v-text-field(
                  :value="computedDateTo"
                  clearable
                  label="По какую дату выгрузить данные"
                  readonly
                  v-bind="attrs"
                  v-on="on"
                  :rules="dateRules"
                  @click:clear="dateTo = null"
                )
              v-date-picker(
                v-model="dateTo"
                no-title
                scrollable
                :min="dateFrom"
                :max="(new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10)"
                locale="ru-RU"
                first-day-of-week=1
              )
                v-spacer
                v-btn(text @click="dateToPickerMenu = false") Cancel
                v-btn(text @click="$refs.dateToPickerMenu.save(dateTo)") OK
            // Выбор тикеров
            v-autocomplete(
              v-model="selectedTickers",
              :items="tickers",
              label="Тикеры"
              multiple
              clearable
              small-chips
              deletable-chips
              hint="Выберите тикеры"
              persistent-hint
              :rules="tickersRules"
            )
            v-text-field(
              v-model.number="amount"
              :rules="amountRules"
              required
              label="Сумма для составления портфеля (руб.)"
              type="number"
            )
            v-autocomplete(
              :items="models"
              item-text="desc"
              item-value="model_name"
              label="Модель предсказания"
              required
              v-model="selectModel"
              :hint="modelHint"
              :rules="selectModelRules"
              return-object
            )
            v-autocomplete(
              :items="optimizers"
              item-text="desc"
              item-value="optimization_type"
              label="Критерий оптимизации портфеля"
              required
              v-model="selectOptimizer"
              :hint="optimizerHint"
              :rules="selectOptimizerRules"
              return-object
            )
            v-text-field(
              v-model.number="monthCount"
              :rules="monthCountRules"
              required
              label="Кол-во месяцев для предсказания"
              type="number"
            )
            v-btn(@click="redirectToChart" :disabled="!isValid" :dark="isValid") Составить портфель
</template>

<script>
import moment from 'moment'
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'Home',
  data: () => ({
    isLoad: false,
    isValid: true,
    dateFrom: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10),
    dateFromPickerMenu: false,
    dateTo: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10),
    dateToPickerMenu: false,
    dateRules: [
      v => !!v || 'Выберите дату'
    ],
    amount: 1000,
    amountRules: [
      v => !!v || 'Обязательное поле',
      v => v >= 1000 || 'Сумма должна быть больше 1000'
    ],
    selectedTickers: null,
    tickersRules: [
      v => (!!v && v.length && v.length > 0) || 'Выберите тикеры',
      v => (!!v && v.length && v.length > 1) || 'Выберите несколько тикеров'
    ],
    monthCount: 10,
    monthCountRules: [
      v => !!v || 'Обязательное поле',
      v => v > 0 || 'Должно быть положительным'
    ],
    selectModel: null,
    selectModelRules: [
      v => !!v || 'Выберите модель'
    ],
    selectOptimizer: null,
    selectOptimizerRules: [
      v => !!v || 'Выберите как оптимизировать портфель'
    ]
  }),
  beforeMount () {
    this.dateFrom = this.userData.dateFrom
    this.dateTo = this.userData.dateTo
    this.selectedTickers = this.userData.selectedTickers
    this.monthCount = this.userData.monthCount
    this.amount = this.userData.amount
    this.selectModel = this.userData.selectModel
    this.selectOptimizer = this.userData.selectOptimizer
  },
  computed: {
    ...mapGetters(
      {
        tickers: 'tickers/tickers',
        models: 'models/models',
        userData: 'formData/data',
        optimizers: 'optimizers/optimizers'
      }
    ),
    computedDateTo () {
      return this.formatMomentDate(this.dateTo)
    },
    computedDateFrom () {
      return this.formatMomentDate(this.dateFrom)
    },
    modelHint () {
      return this.selectModel ? this.selectModel.hint : ''
    },
    optimizerHint () {
      return this.selectOptimizer ? this.selectOptimizer.hint : ''
    }
  },
  methods: {
    ...mapActions(
      {
        getTickers: 'tickers/getTickers',
        getPredict: 'predict/getPredict',
        getModels: 'models/getModels',
        clearError: 'predict/clearError',
        saveData: 'formData/saveData',
        getOptimizers: 'optimizers/getOptimizers'
      }
    ),
    formatMomentDate (d) {
      return d ? moment(d).locale('ru').format('LL') : ''
    },
    redirectToChart () {
      const userData = {
        selectedTickers: this.selectedTickers,
        dateFrom: this.dateFrom,
        dateTo: this.dateTo,
        amount: this.amount,
        selectModel: this.selectModel,
        monthCount: this.monthCount,
        selectOptimizer: this.selectOptimizer
      }
      this.saveData(userData)
      this.clearError()
      this.isLoad = true
      this.getPredict(
        {
          tickers_name: this.selectedTickers + '',
          date_from: this.dateFrom,
          date_to: this.dateTo,
          total_sum: this.amount,
          model_name: this.selectModel.model_name,
          month: this.monthCount,
          optimization_type: this.selectOptimizer.optimization_type
        }
      ).then(
        () => {
          this.isLoad = false
          this.$router.push({ path: '/chart' })
        }
      ).catch(
        () => {
          this.isLoad = false
          this.$router.push({ path: '/chart' })
        }
      )
    }
  },
  mounted () {
    this.getTickers()
    this.getModels()
    this.getOptimizers()
  }
}
</script>

<style scoped>

@-moz-keyframes loader {
  from {
    transform: rotate(0);
  }
  to {
    transform: rotate(360deg);
  }
}

@-webkit-keyframes loader {
  from {
    transform: rotate(0);
  }
  to {
    transform: rotate(360deg);
  }
}

@-o-keyframes loader {
  from {
    transform: rotate(0);
  }
  to {
    transform: rotate(360deg);
  }
}

@keyframes loader {
  from {
    transform: rotate(0);
  }
  to {
    transform: rotate(360deg);
  }
}
.tl {
  width: 400px;
}
</style>
