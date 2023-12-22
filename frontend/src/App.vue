<script setup>
import Header from './components/Header.vue'
</script>

<template>
  <div class="background-main">
    <Header />
    <div class="main-wrapper">
      <router-view />
    </div>
  </div>
</template>

<style>
body {
  background-color: #797979;
}

.background-main {
  background-color: #d9d9d9;
  box-shadow: 0px 13px 21px 0px rgba(0, 0, 0, 0.62);
  border-radius: 39px 39px 0px 0px;
  margin-left: 37px;
  margin-right: 37px;
  margin-top: 37px;
  height: 100%;
  min-height: 100vh
}

.main-wrapper {
  padding-left: 22px;
}

</style>
