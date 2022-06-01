<template lang="pug">
v-app
  v-main
    Header
    router-view
</template>

<script>

import Header from '@/components/Header'
export default {
  name: 'App',
  components: { Header },
  data: () => ({
    //
  })
}
</script>

<style>
@font-face {
  font-style: normal;
  font-weight: 400;
  font-family: "Montserrat";
  font-display: swap;
  src:
    url("assets/fonts/montserrat-regular.woff2") format("woff2"),
    url("assets/fonts/montserrat-regular.woff") format("woff");
}
@font-face {
  font-style: normal;
  font-weight: 500;
  font-family: "Montserrat";
  font-display: swap;
  src:
    url("assets/fonts/montserrat-medium.woff2") format("woff2"),
    url("assets/fonts/montserrat-medium.woff") format("woff");
}
@font-face {
  font-style: normal;
  font-weight: 600;
  font-family: "Montserrat";
  font-display: swap;
  src:
    url("assets/fonts/montserrat-semibold.woff2") format("woff2"),
    url("assets/fonts/montserrat-semibold.woff") format("woff");
}
@font-face {
  font-style: normal;
  font-weight: 700;
  font-family: "Montserrat";
  font-display: swap;
  src:
    url("assets/fonts/montserrat-bold.woff2") format("woff2"),
    url("assets/fonts/montserrat-bold.woff") format("woff");
}
#app {
  font-family: "Montserrat", "Arial", sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}
</style>
