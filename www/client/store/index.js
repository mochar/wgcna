import Vue from 'vue'
import Vuex from 'vuex'
import router from '../router'

Vue.use(Vuex)

const state = {
    projects: [], // when null, app not initialized yet
    projectIndex: null,
    projectLoading: true
}

const getters = {
    project: state => {
        return state.projects[state.projectIndex]
    }
}

const mutations = {
    setProjects(state, projects) {
        state.projects = projects
    },
    setProjectIndex(state, index) {
        state.projectIndex = index
    },
    editProject(state, edits) {
        Vue.set(state.projects, state.projectIndex, 
            {...state.projects[state.projectIndex], ...edits})
    },
    setProjectLoading(state, loading) {
        state.projectLoading = loading
    },
}

const actions = {
    getProjects({ commit }) {
        return $.getJSON(`${ROOTURL}/projects/`).then(data => {
            const projects = data.projects
            commit('setProjects', projects)
            commit('setProjectLoading', false)
            return projects
        })
    }
}

const store = new Vuex.Store({
    state,
    getters,
    mutations,
    actions
})

export default store
