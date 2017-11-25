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
import { min, max } from 'd3-array'
import { scaleSequential, scaleOrdinal } from 'd3-scale'
import { interpolateReds, schemeReds } from 'd3-scale-chromatic'

export default {
    data() {
        return {
            imgSrc: null,
            cutHeight: null,
            loading: true,
            cutting: false,
            clusterData: null,
            colors: null,
            outlierSamples: [],
            twoColorPal: schemeReds[3].filter((x, i) => i !== 1)
        }
    },

    components: {
        Dendrogram
    },

    props: ['projectId', 'go'],

    methods: {
        getClusterData() {
            return $.get(`${ROOTURL}/projects/${this.projectId}/clustersamples`).then(data => {
                this.clusterData = data.clusterData
                if (data.colors) {
                    for (let x in data.colors) {
                        let colors = [], scale
                        const uniqColors = [...new Set(data.colors[x])]
                        if (data.types[x] === 'N') {
                            let palette = schemeReds[uniqColors.length]
                            if (uniqColors.length === 2) palette = this.twoColorPal
                            scale = scaleOrdinal(palette).domain(uniqColors)
                        } else {
                            scale = scaleSequential(interpolateReds).domain([min(uniqColors), max(uniqColors)])
                        }

                        data.clusterData.order.forEach((index, i) => {
                            colors[i] = scale(data.colors[x][index])
                        })
                        data.colors[x] = colors
                    }
                    this.colors = data.colors
                }
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