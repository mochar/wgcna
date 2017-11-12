<template>
<div>
    <div class="row">
        <div class="col-6">
            <ul class="nav nav-tabs top position-relative">
                <li class="nav-item">
                    <a class="nav-link active" href="#">Module creation</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="#">Module inspection</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="#">Module significance</a>
                </li>
            </ul>
        </div>
        <div class="col-6">
            <div class="btn-group btn-block" id="project-select">
                <button class="btn btn-light btn-block dropdown-toggle text-left d-flex justify-content-between align-items-center" 
                        style="margin-right: -1px" data-toggle="dropdown">
                    <span v-if="project">
                        {{ project.name }}
                        <span v-show="project.description" class="text-muted">- {{ project.description }}</span>
                    </span>
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

    <div v-if="project || loading">
        <treshold 
            :project="project" 
            :update="shouldUpdate"
            v-if="project.step > 0" 
            @done="tresholdDone">
        </treshold>
        <cluster 
            :project="project" 
            :update="shouldUpdate || project.step == 2"
            v-if="project.step > 1"
            @cutting="$store.commit('editProject', {step: 3})"
            @done="clusterDone">
        </cluster>
        <genotype
            :project="project" 
            :update="shouldUpdate || project.step == 4"
            @done="genotypeDone"
            v-if="project.step > 3">
        </genotype>
    </div>

    <!-- <export-modal :name="name" :step="step" :modules="modules" v-if="step > 3"></export-modal> -->
</div>
</template>

<script>
import Treshold from 'components/Treshold'
import Cluster from 'components/Cluster'
import Genotype from 'components/Genotype'
import Annotation from 'components/Annotation'
import ExportModal from 'components/ExportModal'

export default {
    data() {
        return {
            modules: [],
            loading: false,
            previousProject: null,
            shouldUpdate: true
        }
    },

    components: {
        Treshold,
        Cluster,
        Genotype,
        Annotation,
        ExportModal
    },

    methods: {
        generateReport() {
            // const url = `${ROOTURL}/report/${this.name}`
            // window.open(url)
        },
        tresholdDone(power) {
            this.$store.commit('editProject', {step: 2, power})
        },
        clusterDone(minModuleSize) {
            this.$store.commit('editProject', {step: 4, minModuleSize })
        },
        genotypeDone() {
            this.$store.commit('editProject', {step: 5})
            // this.getColors()
        },
        getColors() {
            // if (this.name && this.step > 3) {
            //     $.getJSON(`${ROOTURL}/export/${this.name}`).then(data => {
            //         this.modules = data.modules
            //     })
            // }
        },
        selectProject(index) {
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