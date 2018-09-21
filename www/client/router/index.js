import Vue from 'vue'
import Router from 'vue-router'
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
