import Vue from 'vue'
import Vuex from 'vuex'
import router from '../router'

Vue.use(Vuex)

const state = {
    names: [],
    name: null
}

const mutations = {
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
    }
}

const store = new Vuex.Store({
    state,
    mutations,
    actions
})

export default store
