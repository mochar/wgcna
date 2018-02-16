import Vue from 'vue'
import Vuex from 'vuex'
import router from '../router'

Vue.use(Vuex)

const state = {
    projects: [],
    projectIndex: null,
    projectLoading: true
}

const getters = {
    project: state => {
        return state.projectIndex === null ? null : state.projects[state.projectIndex]
    },
    projectIds: state => {
        return state.projects.map(project => project.id)
    }
}

const mutations = {
    setProjects(state, projects) {
        state.projects = projects
    },
    setProjectIndex(state, index) {
        state.projectIndex = index
    },
    setProjectById(state, id) {
        for (let index = 0; index < state.projects.length; index++) {
            const project = state.projects[index]
            if (project.id === id) {
                state.projectIndex = index
                break
            }
        }
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
