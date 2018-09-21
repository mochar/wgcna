<template>
<div>
    <dendrogram 
        v-if="colors" 
        :ratio="0.3"
        :labels="true"
        :cluster-data="clusterData"
        :cuttable="cuttable"
        :colors="colors"
        @cutted="d => $emit('cutted', d)">
    </dendrogram>
    <!-- <dendro
        v-if="colors" 
        :ratio="0.3"
        :labels="true"
        :cluster-data="clusterData"
        :cuttable="cuttable"
        :colors="colors"
        @cutted="d => $emit('cutted', d)">
    </dendro> -->
</div>
</template>

<script>
import Dendrogram from 'charts/Dendrogram.vue'
import Dendro from 'charts/Dendro'
import { min, max } from 'd3-array'
import { scaleSequential, scaleOrdinal } from 'd3-scale'
import { interpolateReds, schemeReds } from 'd3-scale-chromatic'

export default {
    data() {
        return {
            clusterData: null,
            colors: null,
            twoColorPal: schemeReds[3].filter((x, i) => i !== 1)
        }
    },

    props: ['projectId', 'cuttable'],

    components: {
        Dendrogram,
        // Dendro
    },

    created() {
        $.get(`${ROOTURL}/projects/${this.projectId}/clustersamples`).then(data => {
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
            console.log('loaded')
            this.$emit('loaded')
        }, () => {
            console.log('nani?1')
        })
    }
}
</script>
