<template>
<div>
    <div class="row top">
        <div class="col-7">
            <div class="btn-group btn-block">
                <button class="btn btn-secondary btn-block dropdown-toggle text-left" data-toggle="dropdown">
                    <span v-if="project">{{ project.name }}</span>
                </button>
                <div class="dropdown-menu">
                    <a class="dropdown-item" href="#" v-for="(project, i) in projects" :key="project.id"
                        @click="selectProject(i)">
                        <span>{{ project.name }}</span><br>
                        <small class="text-muted">{{ project.description}}</small>
                    </a>
                </div>
                <button class="btn btn-secondary" data-toggle="modal" data-target="#new-modal">
                    <span class="fa fa-plus"></span>
                </button>
            </div>
        </div>
        <div class="col-3">
            <div class="btn-group">
                <button class="btn btn-primary" style="border-top-width: 1px" 
                        @click="generateReport">
                    <span class="fa fa-book"></span>
                    Generate report
                </button>
                <button class="btn btn-secondary" data-toggle="modal" data-target="#export-modal"
                        :disabled="project && project.step < 4">
                    <span class="fa fa-download"></span>
                    Export modules
                </button>
            </div>
        </div>
        <div class="col-2">
            <router-link to="/integrate" class="btn btn-secondary float-right" tag="button">
                <span class="fa fa-compress"></span>
                Integrate
            </router-link>
        </div>
    </div>

    <div v-if="project || loading">
        <treshold 
            :project="project" 
            v-if="project.step > 0" 
            @done="tresholdDone">
        </treshold>
        <cluster 
            :project="project" 
            v-if="project.step > 1"
            @cutting="$store.commit('editProject', {step: 3})"
            @done="clusterDone">
        </cluster>
        <genotype
            :project="project" 
            @done="genotypeDone"
            v-if="project.step > 3">
        </genotype>
    </div>

    <!-- <export-modal :name="name" :step="step" :modules="modules" v-if="step > 3"></export-modal> -->
    <new-project-modal></new-project-modal>
</div>
</template>

<script>
import Treshold from 'components/Treshold'
import Cluster from 'components/Cluster'
import Genotype from 'components/Genotype'
import Annotation from 'components/Annotation'
import ExportModal from 'components/ExportModal'
import NewProjectModal from 'components/NewProjectModal'

export default {
    data() {
        return {
            modules: [],
            loading: false
        }
    },

    components: {
        Treshold,
        Cluster,
        Genotype,
        Annotation,
        ExportModal,
        NewProjectModal
    },

    methods: {
        generateReport() {
            // const url = `${ROOTURL}/report/${this.name}`
            // window.open(url)
        },
        tresholdDone(power) {
            this.$store.commit('editProject', {step: 2, power})
        },
        clusterDone() {
            this.$store.commit('editProject', {step: 4})
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
            return this.$store.getters.project
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
</style>