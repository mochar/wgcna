import Vue from 'vue'
import Router from 'vue-router'
import Home from 'views/Home'
import Analyze from 'views/Analyze'
import Preprocess from 'views/Preprocess'
import Integrate from 'views/Integrate'

Vue.use(Router)

export default new Router({
	mode: 'hash',
	routes: [
		{
            name: 'home',
            path: '/',
            component: Home
        },
        {
            name: 'preprocess',
            path: '/preprocess/:id',
            component: Preprocess
        },
        {
            name: 'analyze',
            path: '/analyze',
            component: Analyze
        },
        {
            path: '/integrate',
            component: Integrate
        }
	]
})
