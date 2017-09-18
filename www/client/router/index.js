import Vue from 'vue'
import Router from 'vue-router'
import Home from '../views/Home'
import New from '../views/New'
import Annotate from '../views/Annotate'
import Annotatenew from '../views/Annotatenew'

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
            path: '/Annotate',
            component: Annotate
        },
        {
            path: '/Annotatenew',
            component: Annotatenew
        }
	]
})
