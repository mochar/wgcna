import Vue from 'vue'
import { sync } from 'vuex-router-sync'
import App from './components/App'
import router from './router'
import store from './store'
import Helpers from './plugins/Helpers'
import { library } from '@fortawesome/fontawesome-svg-core'

// Line by line because of bug: https://github.com/FortAwesome/react-fontawesome/issues/70
import { faEdit } from '@fortawesome/free-solid-svg-icons/faEdit'
import { faPlus } from '@fortawesome/free-solid-svg-icons/faPlus'
import { faChevronLeft } from '@fortawesome/free-solid-svg-icons/faChevronLeft'
import { faChevronRight } from '@fortawesome/free-solid-svg-icons/faChevronRight'
import { faCog } from '@fortawesome/free-solid-svg-icons/faCog'
import { faInfo } from '@fortawesome/free-solid-svg-icons/faInfo'
import { faEllipsisV } from '@fortawesome/free-solid-svg-icons/faEllipsisV'
import { faCut } from '@fortawesome/free-solid-svg-icons/faCut'
import { faAngleDoubleLeft } from '@fortawesome/free-solid-svg-icons/faAngleDoubleLeft'
import { faAngleDoubleRight } from '@fortawesome/free-solid-svg-icons/faAngleDoubleRight'
import { faCaretDown } from '@fortawesome/free-solid-svg-icons/faCaretDown'
import { faDownload } from '@fortawesome/free-solid-svg-icons/faDownload'
import { faSync } from '@fortawesome/free-solid-svg-icons/faSync'
import { faCheck } from '@fortawesome/free-solid-svg-icons/faCheck'
import { faCertificate } from '@fortawesome/free-solid-svg-icons/faCertificate'
import { faChartBar } from '@fortawesome/free-solid-svg-icons/faChartBar'
import { faUpload } from '@fortawesome/free-solid-svg-icons/faUpload'
import { faRetweet } from '@fortawesome/free-solid-svg-icons/faRetweet'
import { faCircle } from '@fortawesome/free-solid-svg-icons/faCircle'
import { faEye } from '@fortawesome/free-regular-svg-icons/faEye'
import { faTrashAlt } from '@fortawesome/free-regular-svg-icons/faTrashAlt'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

library.add(faPlus, faChevronLeft, faChevronRight, faCog, faInfo, faEllipsisV, faCut, faAngleDoubleLeft, faAngleDoubleRight, faCaretDown, faDownload, faSync, faCheck, faCertificate, faChartBar, faEye, faUpload, faRetweet, faEdit, faCircle, faTrashAlt)
Vue.component('font-awesome-icon', FontAwesomeIcon)

sync(store, router)

Vue.use(Helpers)

const app = new Vue({
    router,
    store,
    ...App
})

export {app, router, store}
