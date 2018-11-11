import Vue from 'vue'
import Router from 'vue-router'
import Analyze from 'views/analyze/Analyze'
import Integrate from 'views/Integrate'
import NotFound from 'views/NotFound'
import Project from 'views/Project'

const New = () => import(/* webpackChunkName: "new" */  'views/New')

Vue.use(Router)

export default new Router({
	mode: 'hash',
	routes: [
		{
            path: '/',
            redirect: { name: 'analyze' }
        },
        {
            name: 'new',
            path: '/new',
            component: New
        },
        {
            name: 'analyze',
            path: '/analyze/:id',
            component: Analyze
        },
        {
            name: 'project',
            path: '/project/:id',
            component: Project
        },
        {
            path: '/integrate',
            component: Integrate
        },
        {
            name: 'notfound',
            path: '/notfound',
            component: NotFound
        },
        {
            path: '*',
            redirect: { name: 'notfound' }
        }
	]
})
