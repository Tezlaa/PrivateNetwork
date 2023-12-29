<script setup>
import Header from './components/header/Header.vue'


</script>

<template>
  <div class="background-main">
    <Header />
    <div class="main-wrapper">
      <div class="background-icon">
        <img src="/logo.png" alt="">
      </div>
      
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
  min-height: 100vh;
  position: relative;
}

.background-icon {
  position: absolute;
	bottom: 0px;
	right: 0;
  left: 0;
  z-index: 1;
  opacity: 0.17;
}

.main-wrapper {
  padding-left: 22px;
  z-index: 2;
}

</style>
