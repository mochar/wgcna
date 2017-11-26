<template>
<div class="h-100">
    <nav class="navbar navbar-expand-lg navbar-light" id="navbar-main">
        <div class="container">
            <router-link to="/" class="navbar-brand text-main font-weight-bold">WGCNA</router-link>
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>

            <div class="collapse navbar-collapse" id="navbarNav">
                <div class="navbar-nav">
                    <router-link :to="`/analyze/${analyzeTo}`" class="nav-item nav-link" 
                            active-class="active" tag="a" v-if="$store.getters.project">
                        Analyze
                    </router-link>
                    <span class="nav-item nav-link text-muted" v-else>Analyze</span>
                    <router-link to="/integrate" class="nav-item nav-link" active-class="active" tag="a">
                        Integrate
                    </router-link>
                </div>
            </div>
            <button class="btn btn-light float-right" id="new-project-btn" data-toggle="modal" data-target="#new-modal">
                <span class="fa fa-plus"></span>
                New Project
            </button>
        </div>
    </nav>

    <div class="container" id="app">
        <router-view></router-view>
    </div>

    <new-project-modal></new-project-modal>
</div>
</template>

<script>
import 'bootstrap'
import Vue from 'vue'
import NewProjectModal from 'components/NewProjectModal'

Vue.filter('round', function(value, decimals) {
  if(!value) value = 0
  if(!decimals) decimals = 0
  return Math.round(value * Math.pow(10, decimals)) / Math.pow(10, decimals)
})

$.ajaxSetup({ xhrFields: { withCredentials: true } })

export default {
    components: {
        NewProjectModal
    },

    created() {
        this.$store.dispatch('getProjects').then(data => {
            if (data.length > 0) this.$store.commit('setProjectIndex', 0)
        })
    },

    computed: {
        analyzeTo() {
            const project = this.$store.getters.project
            return project === null ? '' : project.id
        }
    }
}
</script>

<style src="../../node_modules/font-awesome/css/font-awesome.min.css"></style>
<style src="../../node_modules/bootstrap/dist/css/bootstrap.min.css"></style>
<style src="../../node_modules/webui-popover/dist/jquery.webui-popover.min.css"></style>
<style>
html {
    overflow-y: scroll;
    font-size: 14px;
}

input[type=text] {
    border: 1px solid #ccc;
    box-shadow: initial;
}

svg {
    font-family: sans-serif;
    font-size: 10pt;
}

#app {
    margin-top: 1rem;
    color: #222 !important;
}

.badge-pill {
    border-radius: 10rem !important;
}

.btn {
    cursor: pointer;
    position: relative;
    -webkit-transition: initial;
       -moz-transition: initial;
            transition: initial;
}

/* .btn-primary, .btn-success, .btn-danger {
    border-width: 0 1px 2px 1px;
}
.btn-secondary { border-width: 1px 1px 2px 1px }

.btn-primary:active, .btn-success:active, .btn-danger:active {
    border-width: 2px 1px 0 1px;
}
.btn-secondary:active { border-width: 2px 1px 1px 1px } */

.btn-primary { 
    background-color: #0c7dd6;
    border-color: #0c7dd6;
}
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


* {
    -webkit-border-radius: 0 !important;
    -moz-border-radius: 0 !important;
    border-radius: 0 !important;
}

.custom-radio .custom-control-indicator {
    border-radius: 50% !important;
}

/* .btn-primary { border-color: #01549b; }
.btn-primary:hover, .btn-primary:active { background-color: #0275d8; }
.btn-success { border-color: #419641; }
.btn-success:hover, .btn-success:hover { background-color: #5cb85c; }
.btn-danger { border-color: #c12e2a; }
.btn-danger:hover, .btn-danger:active { background-color: #d9534f; }
.btn-secondary { border-color: #adadad; }
.btn-secondary:hover, .btn-secondary:active { background-color: #fff;  }
.btn:hover:not(:disabled) {
    top: -1px;
    box-shadow: 0px 1px 1px 0px #eee;
}
.btn:active { top: 1px !important; }
.btn:focus { box-shadow: inherit; }
.btn:focus:hover:not(:active) {
    top: 0px !important;
}
a:active, .btn-link:active {
    color: #333;
} */

.text-main {
    color: #01549b !important;
}
.border-main {
    border-color: #01549b !important;
}

.text-normal {
    color: #5a5a5a !important;
}

#new-project-btn {
    color: #111;
    background-color: #f8f8f8;
    border-color: #dae0e54d;
    /* background: -moz-linear-gradient(hsl(0, 0, 100%), hsl(0, 0, 30%));
    background: linear-gradient(hsl(0, 0%, 97%), hsl(0, 0%, 95%));  */
}

#navbar-main {
    border-bottom: 1px solid #eaeaea;
    border-top: 2px solid #01549b;
    background-color: #fcfcfc66;
}

.block-title {
    color: #01549b;
    letter-spacing: 1px;
    font-weight: bold;
    margin-bottom: 1rem;
}
</style>