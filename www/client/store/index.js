import Vue from 'vue'
import Vuex from 'vuex'
import router from '../router'

Vue.use(Vuex)

const state = {
    projects: null, // when null, app not initialized yet
    names: [],
    name: null
}

const mutations = {
    setProjects(state, projects) {
        state.projects = projects
    },
    setNames(state, names) {
        state.names = names
    },
    setName(state, name) {
        state.name = name
    }
}

const actions = {
    getNames({ commit }) {
        $.getJSON(`${ROOTURL}/expression/`).then(data => {
            const names = data.names.sort((a, b) => a < b ? -1 : 1)
            commit('setNames', names)
            if (names.length > 0) commit('setName', names[0])
            else router.push('/new')
        })
    },
    getProjects({ commit }) {
        $.getJSON(`${ROOTURL}/projects`).then(data => {
            const projects = data.projects.sort((a, b) => a < b ? -1 : 1)
            commit('setProjects', projects)
        })
    }
}

const store = new Vuex.Store({
    state,
    mutations,
    actions
})

export default store
