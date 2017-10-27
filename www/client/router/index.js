import Vue from 'vue'
import Router from 'vue-router'
import Home from 'views/Home'
import Preprocess from 'views/Preprocess'
import Integrate from 'views/Integrate'

Vue.use(Router)

export default new Router({
	mode: 'hash',
	routes: [
		{
			path: '/',
            component: Home
		},
        {
            name: 'preprocess',
            path: '/preprocess/:id',
            component: Preprocess
        },
        {
            path: '/integrate',
            component: Integrate
        }
	]
})
