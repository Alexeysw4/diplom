<template lang="pug">
v-container(:fill-height="!!error" :fluid="!!error")
  template(v-if="error")
    v-row(align="center" justify="center" v-if="error")
      v-alert(
        prominent
        type="error"
      )
        v-row(align="center")
          v-col.grow {{ error || 'Ошибка :(' }}
          v-col.shrink
            v-btn(@click="refresh") Назад
          v-col.shrink(v-if="chartStocks && seriesStocks")
            v-dialog(v-model="dialog" height="900" width="1000" )
              template(v-slot:activator="{ on, attrs }")
                v-btn(v-bind="attrs" v-on="on") Детали
              v-card
                v-card-title Цены акций
                v-divider
                apexchart(
                  :options="chartStocks"
                  :series="seriesStocks"
                  height="500"
                  width="900"
                )
  template(v-else)
    v-row(justify="space-between")
      v-col(cols="4")
        h3 Деление по акциям
        apexchart(
          :options="chartOptionsStocks"
          :series="valuesStocks"
        )
      v-col(cols="5")
        h3 Деление по отраслям
        apexchart(
          :options="chartOptionsSector"
          :series="sectorValues"
        )
    v-row(justify="space-between")
      v-col(cols="5" v-if="otherLabels && otherLabels.length && otherLabels.length >= 1")
        h3 Оставшиеся акции
        v-list-item(v-for="(item, idx) in otherLabels" :key="idx")
          p #[strong {{ idx+1 }}]. {{ item }}
      v-col(cols="5")
        h3 Итого:
        v-list
          v-list-item(v-for="(item, idx) in seriesComputed" :key="idx")
            p #[strong {{ idx+1 }}]. {{ chartOptionsStocks.labels[idx].toLocaleString() }} - {{ item.toLocaleString() }}% #[i (]#[i {{ valuesStocks.at(idx).toLocaleString() }}] #[i {{ getNounStocks(valuesStocks.at(idx)) }})]
        p #[b Остаток]: {{ remains.toLocaleString() }} руб.
    //v-row(v-if="expectedAnnualReturn || expectedAnnualReturn || sharpeRatio")
    //  h3 Статистика
    //  v-simple-table
    //   template(v-slot:default)
    //    thead
    //      tr
    //        th Название параметра
    //        th Значение
    //    tbody
    //      tr(v-if="expectedAnnualReturn")
    //        td Ожидаемый годовой доход
    //        td {{ (expectedAnnualReturn * 100).toFixed(2) }} %
    //      tr(v-if="annualVolatility")
    //        td Годовая волатильность
    //        td {{ (annualVolatility * 100).toFixed(2) }} %
    //      tr(v-if="sharpeRatio")
    //        td Коэффициент Шарпа
    //        td {{ sharpeRatio }}
    v-row
      apexchart(
        :options="chartStocks"
        :series="seriesStocks"
        height="500"
        width="1200"
      )
</template>

<script>
import VueApexCharts from 'vue-apexcharts'
import { mapGetters } from 'vuex'

export default {
  name: 'ChartView',

  components: {
    apexchart: VueApexCharts
  },
  beforeMount () {
    this.chartOptionsStocks.labels = this.labelsStocks
    this.chartOptionsSector.labels = this.sectorLabels
    this.chartStocks.xaxis.categories = this.xAxisStocks
    this.chartStocks.xaxis.categories = this.xAxisStocks
    this.chartStocks.annotations.xaxis[0].x = new Date(this.xAnnotationStocks).getTime()
  },
  computed: {
    ...mapGetters(
      {
        labelsStocks: 'predict/labels',
        valuesStocks: 'predict/values',
        remains: 'predict/other',
        error: 'predict/error',
        otherLabels: 'predict/otherLabels',
        sectorLabels: 'predict/sectorLabels',
        sectorValues: 'predict/sectorValues',
        seriesStocks: 'predict/seriesStocks',
        xAnnotationStocks: 'predict/xAnnotationStocks',
        xAxisStocks: 'predict/xAxisStocks',
        expectedAnnualReturn: 'predict/expectedAnnualReturn',
        annualVolatility: 'predict/annualVolatility',
        sharpeRatio: 'predict/sharpeRatio'
      }
    ),
    seriesComputed () {
      const sumOfSeries = this.valuesStocks.reduce((partialSum, a) => partialSum + a, 0)
      return this.valuesStocks.map(function (el) {
        return el / sumOfSeries * 100
      })
    }
  },
  data () {
    return {
      isLoad: true,
      chartOptionsStocks: {
        chart: {
          type: 'donut'
        },
        labels: [],
        legend: {
          show: true
        }
      },
      chartOptionsSector: {
        chart: {
          type: 'donut'
        },
        labels: [],
        legend: {
          show: true
        }
      },
      chartStocks: {
        chart: {
          height: 350,
          type: 'line',
          stacked: false
        },
        dataLabels: {
          enabled: false
        },
        markers: {
          size: 0
        },
        title: {
          text: 'Цены на акции',
          align: 'left'
        },
        annotations: {
          xaxis: [
            {
              x: null,
              strokeDashArray: 0,
              borderColor: '#775DD0',
              label: {
                borderColor: '#775DD0',
                style: {
                  color: '#fff',
                  background: '#775DD0'
                },
                text: 'Прогноз'
              }
            }
          ]
        },
        yaxis: {
          labels: {
            formatter: function (val) {
              return val.toFixed(0)
            }
          },
          title: {
            text: 'Цена акции (руб.)'
          }
        },
        xaxis: {
          type: 'datetime',
          categories: []
        },
        tooltip: {
          shared: false,
          y: {
            formatter: function (val) {
              return val.toFixed(2)
            }
          }
        }
      },
      dialog: false
    }
  },
  methods: {
    refresh () {
      this.$router.push({ path: '/' })
    },
    getNounStocks (number) {
      let n = Math.abs(number)
      const one = 'акция'
      const two = 'акции'
      const five = 'акций'
      n %= 100
      if (n >= 5 && n <= 20) {
        return five
      }
      n %= 10
      if (n === 1) {
        return one
      }
      if (n >= 2 && n <= 4) {
        return two
      }
      return five
    }
  }
}
</script>

<style scoped>
</style>
