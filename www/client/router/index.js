import Vue from 'vue'
import Router from 'vue-router'
import Home from '../views/Home'
import Expression from '../views/Expression'

Vue.use(Router)

export default new Router({
	mode: 'hash',
	routes: [
		{
			path: '/',
            component: Home
		},
        {
            path: '/expression/:name',
            component: Expression
        }
	]
})
