<template>
<div>
    <dendrogram 
        v-if="!loading" 
        :ratio="0.3"
        :labels="true"
        :cluster-data="clusterData"
        :cuttable="true"
        :colors="colors"
        @cutted="d => outlierSamples = d">
    </dendrogram>
    <span class="fa fa-refresh fa-spin" v-else></span>
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
            colors: null,
            outlierSamples: []
        }
    },

    components: {
        Dendrogram
    },

    props: ['projectId', 'go'],

    methods: {
        getClusterData() {
            return $.get(`${ROOTURL}/projects/${this.projectId}/clustersamples`).then(data => {
                this.clusterData = data
                // this.colors = {Kek: this.clusterData.ordered.map(d => Math.random() > 0.5 ? 'red' : 'white')}
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
                this.$emit('done')
            }, () => {
                alert('fail')
            }).then(() => this.loading = false)
        }
    },

    watch: {
        go() {
            if (this.go) this.done()
        }
    },

    created() {
        this.getClusterData().then(() => {
            this.loading = false
            this.$emit('loaded')
        })
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