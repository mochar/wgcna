import Vue from 'vue'
import Vuex from 'vuex'
import router from '../router'

Vue.use(Vuex)

const state = {
    projects: [],
    projectIndex: null,
    projectLoading: true,
    traitData: null
}

const getters = {
    project: state => {
        return state.projectIndex === null ? null : state.projects[state.projectIndex]
    },
    nominalTraits: (state, getters) => {
        const project = getters.project
        if (!project && !project.traits) return null
        return Object.keys(project.traits).filter(t => project.traits[t] === 'N')
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
    setTraitData(state, data) {
        state.traitData = data
    },
    removeProject(state, index) {
        let projects = [...state.projects]
        projects.splice(index, 1)
        state.projects = projects
        state.projectIndex = state.projects.length >= 1 ? 0 : null
        state.traitData = null
    }
}

const actions = {
    getProjects({ commit }) {
        return $.getJSON(`${ROOTURL}/projects/`).then(data => {
            const projects = data.projects
            commit('setProjects', projects)
            return projects
        })
    },
    getTraitData({ state, getters, commit }) {
        if (state.traitData) return Promise.resolve()
        return $.getJSON(`${ROOTURL}/projects/${getters.project.id}/trait?transpose=true`).then(data => {
            commit('setTraitData', JSON.parse(data))
        })
    },
    selectProjectById({ commit }, id) {
        commit('setTraitData', null)
        commit('setProjectById', id)
    }
}

const store = new Vuex.Store({
    state,
    getters,
    mutations,
    actions
})

export default store
