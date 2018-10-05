<template>
<page :requirement="Boolean($store.getters.project)">
    <div class="row">
        <div class="col-6">
            <ul class="nav nav-tabs top position-relative">
                <li class="nav-item">
                    <a 
                        class="nav-link" 
                        :class="{ active: tab == 'ModuleCreationTab' }" 
                        href="#" 
                        @click.prevent="tab = 'ModuleCreationTab'">
                        <font-awesome-icon icon="certificate" fixed-width size="sm" />
                        Generate
                    </a>
                </li>
                <li class="nav-item">
                    <a 
                        class="nav-link" 
                        :class="{ disabled: !hasModules, active: tab == 'ModuleSignificanceTab' }" 
                        href="#" 
                        @click.prevent="tab = 'ModuleSignificanceTab'">
                        <font-awesome-icon icon="chart-bar" fixed-width size="sm" />
                        Significance
                    </a>
                </li>
                <li class="nav-item">
                    <a 
                        class="nav-link" 
                        :class="{ disabled: !hasModules, active: tab == 'ModuleInspectionTab' }" 
                        href="#" 
                        @click.prevent="tab = 'ModuleInspectionTab'">
                        <font-awesome-icon :icon="['far', 'eye']" fixed-width size="sm" />
                        Inspection
                    </a>
                </li>
            </ul>
        </div>
        <div class="col-6">
            <div class="btn-group btn-block" id="project-select">
                <div class="w-100">
                    <button class="btn btn-light btn-block dropdown-toggle text-left d-flex justify-content-between align-items-center" 
                            style="margin-right: -1px" data-toggle="dropdown">
                        <span v-if="!$store.state.projectLoading && project">
                            <font-awesome-icon icon="circle" fixed-width :class="`text-${project.omic}`" />
                            <span>{{ project.name }}</span>
                            <span v-show="project.description" class="text-muted">- {{ project.description }}</span>
                        </span>
                        <font-awesome-icon icon="cog" spin v-else />
                    </button>
                    <div class="dropdown-menu w-100">
                        <!-- <span class="m-3">Projects</span> -->
                        <a class="dropdown-item" href="#" v-for="(project, i) in projects" :key="project.id"
                            @click.prevent="selectProject(project, i)">
                            <div class="d-flex justify-content-between align-items-center">
                                <span>{{ project.name }}</span>
                                <span class="badge badge-pill badge-light bg-main" :class="`bg-${project.omic}`">
                                    {{ project.omic }}
                                </span>
                            </div>
                            <div class="d-flex justify-content-between align-items-center">
                                <small class="text-secondary">{{ project.description}}</small>
                            </div>
                        </a>
                    </div>
                </div>
                <router-link tag="button" class="btn btn-light" style="margin-left: -1px" :to="{ name: 'project', params: { id: $route.params.id }}">
                    <font-awesome-icon icon="edit" size="sm" />
                </router-link>
            </div>
        </div>
    </div>

    <keep-alive>
    <transition name="component-fade" mode="out-in">
        <component
            :is="tab"
            :project="project" 
            :should-update="shouldUpdate || project.step == 4">
        </component>
    </transition>
    </keep-alive>

    <!-- <export-modal :name="name" :step="step" :modules="modules" v-if="step > 3"></export-modal> -->
</page>
</template>

<script>
import Annotation from 'components/Annotation'
import ExportModal from 'components/ExportModal'
import ModuleCreationTab from 'components/AnalyzeTabs/ModuleCreationTab'
import ModuleInspectionTab from 'components/AnalyzeTabs/ModuleInspectionTab'
import ModuleSignificanceTab from 'components/AnalyzeTabs/ModuleSignificanceTab'
import Page from './Page'
import { mapState, mapActions, mapGetters } from 'vuex'

export default {
    data() {
        return {
            modules: [],
            loading: false,
            previousProject: null,
            shouldUpdate: true,
            tab: 'ModuleCreationTab'
        }
    },

    components: {
        Annotation,
        ExportModal,
        ModuleCreationTab,
        ModuleInspectionTab,
        ModuleSignificanceTab,
        Page
    },

    methods: {
        ...mapActions(['selectProjectById']),
        generateReport() {
            // const url = `${ROOTURL}/report/${this.name}`
            // window.open(url)
        },
        getColors() {
            // if (this.name && this.step > 3) {
            //     $.getJSON(`${ROOTURL}/export/${this.name}`).then(data => {
            //         this.modules = data.modules
            //     })
            // }
        },
        selectProject(project, index) {
            this.tab = 'ModuleCreationTab'
            this.$router.push({ name: 'analyze', params: { id: project.id }})
        }
    },

    computed: {
        ...mapState(['projectIndex', 'projects']),
        ...mapGetters(['projectIds']),
        project() {
            const project = this.$store.getters.project
            this.shouldUpdate = !this.previousProject || this.previousProject.id != project.id
            this.previousProject = project
            return project
        },
        hasModules() {
            return this.project && this.project.step > 3
        }
    },

    beforeRouteUpdate(to, from, next) {
        if (!this.projectIds.includes(to.params.id)) next({ name: 'notfound' })
        this.selectProjectById(to.params.id)
        if (from.name === 'analyze') next()
        else next({ name: 'analyze', params: { id: this.projectIndex }})
    },

    created() {
        this.selectProjectById(this.$store.state.route.params.id)
    },
    
    watch: {
        '$store.state.projectLoading'() {
            if (!this.$store.state.projectLoading) {
                if (!this.projectIds.includes(this.$route.params.id)) next({ name: 'notfound' })
                this.selectProjectById(this.$route.params.id)
            }
        }
    }
}
</script>

<style>
#name-select:active:hover {
    background-color: white;
}

.block {
    margin-bottom: 1rem;
}

.top {
    margin-bottom: 1rem;
}

.block-action-div {
    /* border-top: 1px dashed #ccc; */
    padding-top: 1rem;
    /* margin-top: .5rem; */
}

#project-select {
    box-shadow: 0 1px 1px 0 rgba(0,0,0,0.12),0 0 0 1px rgba(0,0,0,0.08);
    transition: box-shadow 150ms cubic-bezier(0.4, 0.0, 0.2, 1);
}
#project-select:hover {
    box-shadow: 0 2px 2px 0 rgba(0,0,0,0.14),0 0 0 1px rgba(0,0,0,0.08);
}

#project-select button {
    background-color: #f8f9fa !important;
    /* border-color: #f8f9fa !important; */
    /* border: 1px solid #e2e6ea4d !important; */
    border: 0;
}
#project-select button:focus {
    z-index: initial;
    box-shadow: initial;
    -webkit-box-shadow: initial;
}

#project-select .dropdown-item:hover {
    background-color: #f8f9fa !important;
}
</style>

<style scoped>
.nav-link {
    color: #999;
}
.component-fade-enter-active, .component-fade-leave-active {
  transition: opacity .05s ease;
}
.component-fade-enter, .component-fade-leave-to
/* .component-fade-leave-active below version 2.1.8 */ {
  opacity: 0;
}
</style>
