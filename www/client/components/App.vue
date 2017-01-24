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

.btn-primary, .btn-success, .btn-danger {
    border-width: 0 1px 2px 1px;
}
.btn-secondary { border-width: 1px 1px 2px 1px }

.btn-primary:active, .btn-success:active, .btn-danger:active {
    border-width: 2px 1px 0 1px;
}
.btn-secondary:active { border-width: 2px 1px 1px 1px }

.btn-primary { border-color: #01549b; }
.btn-primary:hover, .btn-primary:focus { background-color: #0275d8; }
.btn-success { border-color: #419641; }
.btn-success:hover, .btn-success:focus { background-color: #5cb85c; }
.btn-danger { border-color: #c12e2a; }
.btn-danger:hover, .btn-danger:focus { background-color: #d9534f; }
.btn-secondary { border-color: #adadad; }
.btn-secondary:hover, .btn-secondary:focus { background-color: #fff;  }

.btn:focus {
    box-shadow: inherit;
}
</style>