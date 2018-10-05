<template>
<div class="h-100">
    <div class="container" id="app">
        <div id="navigation" class="d-flex justify-content-between align-items-center">
            <router-link to="/" class="navbar-brand text-main font-weight-bold">WGCNA</router-link>
            <ul class="nav nav-pills nav-fill" v-if="!isNewPage">
                <router-link :to="`/analyze/${analyzeTo}`" class="nav-item nav-link pl-3 pr-3 btn btn-link" 
                        active-class="active text-main" tag="button" >
                        <!-- v-if="$store.state.projects.length > 0"> -->
                    Analyze
                </router-link>
                <!-- <span class="nav-item nav-link text-muted" v-else>Analyze</span> -->
                <router-link to="/integrate" class="nav-item nav-link pl-3 pr-3 btn btn-link" active-class="active" tag="button" 
                                :disabled="$store.state.projects.length < 2">
                    Integrate
                </router-link>
            </ul>
            <router-link to="/new" class="btn btn-light float-right" id="new-project-btn" tag="button" v-if="!isNewPage">
                <span class="fa fa-plus"></span>
                New Project
            </router-link>
            <button class="btn btn-light float-right" id="new-project-btn" @click="$router.go(-1)" v-else>
                Cancel
            </button>
        </div>

        <hr id="content-hr" class="mb-4" />

        <keep-alive exclude="new,project">
            <router-view></router-view>
        </keep-alive>
    </div>
</div>
</template>

<script>
import Vue from 'vue'

Vue.filter('round', function(value, decimals) {
  if(!value) value = 0
  if(!decimals) decimals = 0
  return Math.round(value * Math.pow(10, decimals)) / Math.pow(10, decimals)
})

$.ajaxSetup({ xhrFields: { withCredentials: true } })

export default {
    created() {
        this.$store.dispatch('getProjects').then(() => {
            this.$store.commit('setProjectLoading', false)
        })
    },

    computed: {
        analyzeTo() {
            const project = this.$store.getters.project
            return project ? project.id : this.$store.getters.projectIds[0]
        },
        isNewPage() {
            return this.$route.name === 'new'
        }
    }
}
</script>

<style src="../../node_modules/font-awesome/css/font-awesome.min.css"></style>
<style src="../../node_modules/webui-popover/dist/jquery.webui-popover.min.css"></style>
<style src="../../client/external/distrochart.css"></style>
<style lang="scss">
@import "../../node_modules/bootstrap/scss/bootstrap";

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


.bg-lipidomics {
    background-color: #fbc93d !important;
}
.text-lipidomics {
    color: #fbc93d !important;
}
.bg-metabolomics {
    background-color: #6cc0e5;
}
.text-metabolomics {
    color: #6cc0e5;
}
.bg-transcriptomics {
    background-color: #fb4f4f;
}
.text-transcriptomics {
    color: #fb4f4f;
}

#new-project-btn {
    color: #363636;
    background-color: #f8f8f8;
    /* border-color: #dae0e54d; */
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

#navigation {
    padding-left: .5rem;
    padding-right: .5rem;
}
#navigation .nav-link.active {
    background-color: transparent;
    color: #01549b !important;
    border-bottom: 2px solid;
}
#navigation .nav-link:not(.active) {
    color: grey;
}

#content-hr {
    margin-top: .75rem;
    border-top-width: 2px;
}
</style>
