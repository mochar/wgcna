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
                <font-awesome-icon icon="plus" />
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

<style src="../styles/main.scss" lang="scss"></style>
<style>
#app {
    margin-top: 1rem;
    color: #222 !important;
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
