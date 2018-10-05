<template>
<page :requirement="Boolean($store.getters.project)" class="card card-body mb-5">
    <div class="d-flex justify-content-between align-items-start">
        <h6 class="block-title">
            PROJECT
        </h6>

        <div class="text-muted d-flex align-items-center">
            <div class="dropdown ml-2">
                <button class="btn btn-link text-muted pr-1 pt-0 pb-0" data-toggle="dropdown">
                    <font-awesome-icon icon="ellipsis-v" />
                </button>
                <div class="dropdown-menu dropdown-menu-right">
                    <a class="dropdown-item" href="#" @click.prevent="">
                        <font-awesome-icon icon="edit" fixed-width />
                        Edit
                    </a>
                    <a class="dropdown-item" href="#" @click.prevent="del">
                        <font-awesome-icon :icon="['far', 'trash-alt']" fixed-width />
                        Delete
                    </a>
                    <h6 class="dropdown-header">Download plot</h6>
                    <a class="dropdown-item" href="#" @click.prevent="downloadPlot">
                        Sample tree
                    </a>
                </div>
            </div>
        </div>
    </div>

    <div class="mb-3 ml-3 mr-3">
        <form class="mb-5 mt-4" id="update-form" enctype="multipart/form-data" @submit.prevent="submit">
            <div class="form-row">
                <div class="col-5">
                    <input type="text" :value="project.name" name="name" class="form-control" placeholder="name">
                </div>
                <div class="col-7">
                    <input type="text" :value="project.description" name="description" class="form-control" placeholder="description">
                </div>
            </div>
            <div class="form-row pl-2 mt-3">
                <div class="form-check form-check-inline" v-for="omic in ['transcriptomics', 'lipidomics', 'metabolomics']" :key="omic">
                    <input class="form-check-input" type="radio" name="omic" :id="omic" :value="omic" :checked="omic == project.omic">
                    <label class="form-check-label" :for="omic">{{ omic }}</label>
                </div>
            </div>
            <button class="btn btn-primary mt-3" type="submit" :disabled="updating">
                Update
            </button>
        </form>
        <div class="mt-4">
            <strong class="text-main">Samples and traits</strong>
            <span v-if="loading" class="d-block">loading...</span>
            <sample-tree :projectId="project.id" :cuttable="false" @loaded="loading = false" v-show="!loading">
            </sample-tree>
        </div>
    </div>

    <div>
        <button @click.prevent="$router.go(-1)" class="btn btn-light">
            <font-awesome-icon icon="angle-double-left" />
            Return
        </button>
    </div>
</page>
</template>

<script>
import SampleTree from 'components/SampleTree'
import Page from './Page'
import { mapState, mapActions, mapGetters } from 'vuex'

export default {
    name: 'project', 

    data() {
        return {
            project: null,
            loading: true,
            updating: false
        }
    },

    components: {
        SampleTree,
        Page
    },

    methods: {
        ...mapActions(['selectProjectById']),
        loadProject() {
            if (!this.projectIds.includes(this.$route.params.id)) next({ name: 'notfound' })
            this.selectProjectById(this.$route.params.id)
            this.project = this.$store.getters.project
        },
        downloadPlot() {
            const svgEl = $(this.$el).find('svg')[0]
            this.$helpers.downloadSvg(svgEl, 'sample_clusters')
        },
        del() {
            this.$helpers.delete(this.project.id)
            .then(() => {
                this.$store.commit('removeProject', this.projectIndex)
                if (this.projectIndex === null)
                    this.$router.push({ name: 'new' })
                else
                    this.$router.push({ name: 'analyze' , params: { id: this.$store.getters.project.id }})
            }, () => {
            })
        },
        submit(event) {
            this.updating = true
            const formData = new FormData(event.target)
            this.$helpers.put(formData, this.project.id)
            .then(data => {
                this.updating = false
            }, () => {
                this.updating = false
            })
        }
    },

    computed: {
        ...mapState(['projectIndex', 'projects', 'projectLoading']),
        ...mapGetters(['projectIds']),
    },

    created() {
        if (!this.projectLoading) this.loadProject()
    },

    watch: {
        'projectLoading'() {
            if (!this.projectLoading) this.loadProject()
        }
    }
}
</script>

<style>
#project-name {
}
</style>
