import Vue from 'vue'
import Router from 'vue-router'
import Home from 'views/Home'
import Analyze from 'views/Analyze'
import Preprocess from 'views/Preprocess'
import Integrate from 'views/Integrate'
import SemanticIntegrate from 'views/SemanticIntegrate'
import NotFound from 'views/NotFound'
import Project from 'views/Project'

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
