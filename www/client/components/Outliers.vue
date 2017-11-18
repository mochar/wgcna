<template>
<div class="card card-body">
    <h6 class="block-title text-uppercase">
        Outlier removal
    </h6>

    <dendrogram 
        v-if="!loading" 
        :ratio="0.6"
        :labels="true"
        :cluster-data="clusterData"
        :cuttable="true"
        @cutted="d => outlierSamples = d">
    </dendrogram>
    <span class="fa fa-cog fa-spin fa-2x fa-fw" v-else></span>

    <div class="block-action-div">
        <button class="btn btn-light" :disabled="loading" @click="done">
            <span class="fa fa-check"></span>
            Done
        </button>
    </div>
</div>
</template>

<script>
import Dendrogram from 'charts/Dendrogram'

export default {
    data() {
        return {
            imgSrc: null,
            cutHeight: null,
            loading: true,
            cutting: false,
            clusterData: null,
            outlierSamples: []
        }
    },

    components: {
        Dendrogram
    },

    props: ['projectId'],

    methods: {
        getClusterData() {
            return $.get(`${ROOTURL}/projects/${this.projectId}/clustersamples`).then(data => {
                this.clusterData = data
            })
        },
        done() {
            this.loading = true
            const formData = new FormData()
            this.outlierSamples.forEach(sample => formData.append('samples[]', sample))
            $.post({
                url: `${ROOTURL}/projects/${this.projectId}/clustersamples`,
                data: formData,
                async: true,
                cache: false,
                contentType: false,
                processData: false
            }).then(data => {
                console.log('success')
                this.loading = false
                this.$emit('done')
            }, () => {
                console.log('fail')
                this.loading = false
            })
        }
    },

    created() {
        this.getClusterData().then(() => this.loading = false)
    }
}
</script>

<style scoped>
img.cutting {
    opacity: .5;
}

#done {
    display: block;
    margin-top: 1rem;
}
</style>