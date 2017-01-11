import { app } from './app'

$.ajaxSetup({ xhrFields: { withCredentials: true } })
app.$mount('#app')
