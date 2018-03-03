<template>
<div class="card card-body block">
    <div class="d-flex justify-content-between align-items-start">
        <h6 class="block-title">
            FEATURE CLUSTERING
            <span class="fa fa-lg fa-cog fa-spin float-right" v-if="loading"></span>
        </h6>
        <div class="text-muted d-flex align-items-center">
            <span class="fa fa-info text-muted"></span>
            <div class="dropdown ml-2">
                <button class="btn btn-link text-muted pr-1 pt-0 pb-0" data-toggle="dropdown">
                    <span class="fa fa-ellipsis-v"></span>
                </button>
                <div class="dropdown-menu  dropdown-menu-right">
                    <h6 class="dropdown-header">Download plot</h6>
                    <a class="dropdown-item" href="#" @click.prevent="downloadPlot">
                        Gene tree
                    </a>
                </div>
            </div>
        </div>
    </div>

    <p class="card-text">
        Features are hierarchically clustered and subsequently grouped based on a given minimum module size.
    </p>

    <div v-if="!loading">
        <dendro
            :cluster-data="clusterData" 
            :ratio="0.35" 
            :colors="colors">
        </dendro>
        <div class="block-action-div">
            <form class="form-inline" enctype="multipart/form-data" @submit.prevent="cut">
                <label class="mr-2">Minimum module size</label>

                <div class="form-group mr-2">
                    <input type="number" class="form-control" name="minModuleSize" :placeholder="project.minModuleSize">
                </div>

                <!-- <div class="form-group" style="display: none">
                    <label>Deep split</label>
                    <input type="number" class="form-control" name="deepSplit" min="0" max="5" value="2">
                </div> -->

                <button type="submit" class="btn btn-light mr-2" :disabled="cutting">
                    <span class="fa fa-scissors"></span>
                    Cut
                </button>
            </form>
        </div>
    </div>
</div>
</template>

<script>
import Dendro from 'charts/Dendro'

export default {
    data() {
        return {
            loading: true,
            cutting: false,
            // clusterData: null,
            // colors: null
        }
    },

    components: {
        Dendro
    },

    props: ['project', 'update'],

    methods: {
        cluster() {
            this.loading = true
            this.clusterData = null
            this.colors = null
            $.get(`${ROOTURL}/projects/${this.project.id}/clustergenes`).then(data => {
                this.clusterData = data.clusterData
                if (data.colors)
                    this.colors = {Modules: data.colors.hex}
                this.loading = false
            })
        },
        cut(event) {
            this.cutting = true
            this.$emit('cutting')
            const formData = new FormData(event.target)
            const minModuleSize = parseInt(formData.get('minModuleSize'))
            $.post({
                url: `${ROOTURL}/projects/${this.project.id}/clustergenes`,
                data: formData,
                async: true,
                cache: false,
                contentType: false,
                processData: false
            }).then(data => {
                this.colors = data
                this.cutting = false
                this.$emit('done', minModuleSize)
            }, () => {
                this.cutting = false
            })
        },
        downloadPlot() {
            const svgEl = $(this.$el).find('svg')[0]
            this.$helpers.downloadSvg(svgEl, 'gene_clusters')
        }
    },

    watch: {
        project() {
            if (this.update) this.cluster()
        }
    },

    created() {
        this.cluster()
    }
}
</script>

<style scoped>
img {
    width: 100%;
}

img.cutting {
    opacity: .5;
}
</style>
