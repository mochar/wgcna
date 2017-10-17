import Vue from 'vue'
import Router from 'vue-router'
import Home from '../views/Home'
import New from '../views/New'
import Integrate from '../views/Integrate'

Vue.use(Router)

export default new Router({
	mode: 'hash',
	routes: [
		{
			path: '/',
            component: Home
		},
        {
            path: '/new',
            component: New
        },
        {
            path: '/integrate',
            component: Integrate
        }
	]
})
