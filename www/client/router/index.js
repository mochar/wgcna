import Vue from 'vue'
import Router from 'vue-router'
import store from '../store'
import Analyze from 'views/Analyze'
import Integrate from 'views/Integrate'
import NotFound from 'views/NotFound'
import Project from 'views/Project'

const Home = () => import(/* webpackChunkName: "home" */  'views/Home')
const New = () => import(/* webpackChunkName: "new" */  'views/New')

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
            name: 'new',
            path: '/new',
            component: New
        },
        {
            name: 'analyze',
            path: '/analyze/:id',
            component: Analyze,
            beforeEnter: (to, from, next) => {
                if (to.params.id == 'undefined' || to.params.id == 'null') next({ name: 'new' })
                else next()
            }
        },
        {
            name: 'project',
            path: '/project/:id',
            component: Project
        },
        {
            path: '/integrate',
            component: Integrate,
            beforeEnter: (to, from, next) => {
                if (from.name === null) {
                    next({ name: 'analyze' })
                } else if (store.state.projects.length < 2) {
                    next(false)
                } else {
                    next()
                }
            }
        },
        {
            name: 'notfound',
            path: '/notfound',
            component: NotFound
        }
	]
})
