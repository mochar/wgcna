<template>
<div class="card card-body mb-5">
    <div class="d-flex justify-content-between align-items-start">
        <h6 class="block-title">
            PROJECT
        </h6>

        <div class="text-muted d-flex align-items-center">
            <div class="dropdown ml-2">
                <button class="btn btn-link text-muted pr-1 pt-0 pb-0" data-toggle="dropdown">
                    <span class="fa fa-ellipsis-v"></span>
                </button>
                <div class="dropdown-menu dropdown-menu-right">
                    <a class="dropdown-item" href="#" @click.prevent="">
                        <span class="fa fa-edit fa-fw"></span>
                        Edit
                    </a>
                    <a class="dropdown-item" href="#" @click.prevent="del">
                        <span class="fa fa-trash fa-fw"></span>
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

    <div class="mb-3 ml-3 mr-3" v-if="project">
        <div>
            <strong class="text-main">Info</strong>
            <div class="d-flex flex-column p-3 pt-0">
                <span>{{ project.name }}</span>
                <span>{{ project.description }}</span>
                <span>{{ project.omic }}</span>
            </div>
        </div>
        <div class="mt-4">
            <strong class="text-main">Samples and traits</strong>
            <sample-tree :projectId="project.id" :cuttable="false">
            </sample-tree>
        </div>
    </div>
    <loading v-else></loading>

    <div>
        <button @click.prevent="$router.go(-1)" class="btn btn-light">
            <span class="fa fa-angle-double-left"></span>
            Return
        </button>
    </div>
</div>
</template>

<script>
import SampleTree from 'components/SampleTree'
import Loading from 'components/Loading'
import { mapState, mapMutations, mapGetters } from 'vuex'

export default {
    data() {
        return {
            project: null
        }
    },

    components: {
        SampleTree,
        Loading
    },

    methods: {
        ...mapMutations(['setProjectById']),
        loadProject() {
            if (!this.projectIds.includes(this.$route.params.id)) next({ name: 'notfound' })
            this.setProjectById(this.$route.params.id)
            this.project = this.$store.getters.project
        },
        downloadPlot() {
            const svgEl = $(this.$el).find('svg')[0]
            this.$helpers.downloadSvg(svgEl, 'sample_clusters')
        },
        del() {
            $.ajax({
                type: 'DELETE',
                url: `${ROOTURL}/projects/${this.project.id}`
            }).then(() => {
                this.$router.push({ name: 'home' })
            }, () => {
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
