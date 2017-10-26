<template>
<div>
    <dendrogram 
        v-if="!loading" 
        :ratio="0.6"
        :labels="true"
        :cluster-data="clusterData"
        :cuttable="true"
        @cutted="d => outlierSamples = d">
    </dendrogram>
    <span class="fa fa-cog fa-spin fa-2x fa-fw" v-else></span>

    <button class="btn btn-primary" :disabled="loading" @click="done">
        <span class="fa fa-check"></span>
        Done
    </button>
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

    props: ['project'],

    methods: {
        getClusterData() {
            return $.get(`${ROOTURL}/projects/${this.project.id}/clustersamples`).then(data => {
                this.clusterData = data
            })
        },
        done() {
            this.loading = true
            const formData = new FormData()
            this.outlierSamples.forEach(sample => formData.append('samples[]', sample))
            $.post({
                url: `${ROOTURL}/projects/${this.project.id}/clustersamples`,
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