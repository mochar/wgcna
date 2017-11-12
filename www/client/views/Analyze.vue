<template>
<div>
    <div class="row">
        <div class="col-6">
            <ul class="nav nav-tabs top position-relative">
                <li class="nav-item">
                    <a 
                        class="nav-link" 
                        :class="{ active: tab == 'ModuleCreationTab' }" 
                        href="#" 
                        @click.prevent="tab = 'ModuleCreationTab'">
                        Module creation
                    </a>
                </li>
                <li class="nav-item">
                    <a 
                        class="nav-link" 
                        :class="{ disabled: !hasModules, active: tab == 'ModuleInspectionTab' }" 
                        href="#" 
                        @click.prevent="tab = 'ModuleInspectionTab'">
                        Module inspection
                    </a>
                </li>
                <li class="nav-item">
                    <a 
                        class="nav-link" 
                        :class="{ disabled: !hasModules, active: tab == 'ModuleSignificanceTab' }" 
                        href="#" 
                        @click.prevent="tab = 'ModuleSignificanceTab'">
                        Module significance
                    </a>
                </li>
            </ul>
        </div>
        <div class="col-6">
            <div class="btn-group btn-block" id="project-select">
                <button class="btn btn-light btn-block dropdown-toggle text-left d-flex justify-content-between align-items-center" 
                        style="margin-right: -1px" data-toggle="dropdown">
                    <span v-if="!$store.state.projectLoading && project">
                        {{ project.name }}
                        <span v-show="project.description" class="text-muted">- {{ project.description }}</span>
                    </span>
                    <span class="fa fa-cog fa-spin" v-else></span>
                </button>
                <div class="dropdown-menu">
                    <a class="dropdown-item" href="#" v-for="(project, i) in projects" :key="project.id"
                        @click.prevent="selectProject(i)">
                        <span>{{ project.name }}</span><br>
                        <small class="text-muted">{{ project.description}}</small>
                    </a>
                </div>
                <button class="btn btn-light" style="margin-left: -1px">
                    <span class="fa fa-edit"></span>
                </button>
            </div>
        </div>
    </div>

    <div v-if="project">
        <keep-alive>
            <component
                :is="tab"
                :project="project" 
                :should-update="shouldUpdate || project.step == 4">
            </component>
        </keep-alive>
    </div>

    <!-- <export-modal :name="name" :step="step" :modules="modules" v-if="step > 3"></export-modal> -->
</div>
</template>

<script>
import Annotation from 'components/Annotation'
import ExportModal from 'components/ExportModal'
import ModuleCreationTab from 'components/AnalyzeTabs/ModuleCreationTab'
import ModuleInspectionTab from 'components/AnalyzeTabs/ModuleInspectionTab'
import ModuleSignificanceTab from 'components/AnalyzeTabs/ModuleSignificanceTab'

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
        ModuleSignificanceTab
    },

    methods: {
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
        selectProject(index) {
            this.tab = 'ModuleCreationTab'
            this.$store.commit('setProjectIndex', index)
        }
    },

    computed: {
        projects() {
            return this.$store.state.projects
        },
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

    watch: {
    },

    created() {
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

.block-title {
    color: #01549b;
    letter-spacing: 1px;
    font-weight: bold;
    margin-bottom: 1rem;
}

.block-action-div {
    border-top: 1px dashed #ccc;
    padding-top: 1rem;
    margin-top: 1rem;
}

#project-select button {
    background-color: #f8f9fa !important;
    border-color: #f8f9fa !important;
    border: 1px solid #e2e6ea4d !important;
}
</style>