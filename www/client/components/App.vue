<template>
<div class="container" id="app">
    <router-view></router-view>
</div>
</template>

<script>
import 'bootstrap'
import Vue from 'vue'

Vue.filter('round', function(value, decimals) {
  if(!value) value = 0
  if(!decimals) decimals = 0
  return Math.round(value * Math.pow(10, decimals)) / Math.pow(10, decimals)
})
</script>

<style>
@import "../../node_modules/bootstrap/dist/css/bootstrap.min.css";
@import "../../node_modules/font-awesome/css/font-awesome.min.css";

#app {
    margin-top: 1rem;
}
</style>