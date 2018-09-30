import Vue from 'vue'
import { sync } from 'vuex-router-sync'
import App from './components/App'
import router from './router'
import store from './store'
import Helpers from './plugins/Helpers'

sync(store, router)

Vue.use(Helpers)

const app = new Vue({
    router,
    store,
    ...App
})

export {app, router, store}
