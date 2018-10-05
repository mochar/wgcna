import './promise-polyfill'
import 'bootstrap/js/src/util'
import 'bootstrap/js/src/dropdown'
import { app } from './app'

// Enable progressive web app support (with offline-plugin)
if (process.env.NODE_ENV === 'production') {
  require('./pwa')
}

$.ajaxSetup({ xhrFields: { withCredentials: true } })
app.$mount('#app')
