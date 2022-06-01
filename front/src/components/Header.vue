<template lang="pug">
v-toolbar(elevation="1" dense dark)
  template(v-if="currentPage && currentPage === 'Home'")
    v-toolbar-title Главная (Предложенный портфель не является рекоммендацией)
  template(v-else)
    v-btn(@click="goToHome") На главную
</template>

<script>
export default {
  name: 'Header',
  computed: {
    currentPage () {
      return this.$route.name
    }
  },
  methods: {
    goToHome () {
      this.$router.push({ path: '/' })
    }
  }
}
</script>

<style scoped>

</style>
