import Vue from 'vue'
import Router from 'vue-router'
import store from '../store'
import Home from 'views/Home'
import Analyze from 'views/Analyze'
import Integrate from 'views/Integrate'
import SemanticIntegrate from 'views/SemanticIntegrate'
import NotFound from 'views/NotFound'
import Project from 'views/Project'
import New from 'views/New'

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
            path: '/semanticintegrate',
            component: SemanticIntegrate
        },
        {
            name: 'notfound',
            path: '/notfound',
            component: NotFound
        }
	]
})
