<template>
<div class="dendro" id="tree">
    <canvas class="main"></canvas>
    <canvas v-if="cuttable" class="cut"></canvas>
    <svg v-if="selectable"></svg>
</div>
</template>

<script>
import dendrogram from 'charts/Dendrogram.js'


export default {
    props: {
        clusterData: Object,
        cuttable: Boolean,
        selectable: {
            type: Boolean,
            default: false
        },
        axis: {
            type: Boolean,
            default: true
        },
        labels: Boolean,
        ratio: Number,
        colors: Object
    },

    data() {
        return {
            selected: null
        }
    },

    methods: {
        findChildren(index, children) {
            const row = this.clusterData.merge[index] 
            if (row[0] < 0) children.push(-row[0] - 1)
            else this.findChildren(row[0] - 1, children)
            if (row[1] < 0) children.push(-row[1] - 1)
            else this.findChildren(row[1] - 1, children)
        }
    },

    mounted() {
        const chart = dendrogram({
            selector: '#tree',
            data: this.clusterData,
            cuttable: this.cuttable,
            axis: this.axis,
            labels: this.labels,
            ratio: this.ratio,
            colors: this.colors,
            onSelect: d => this.selected = d
        })
        chart.update()
    },

    computed: {
        children() {
            if (this.selected === null) return []
            let c = []
            this.findChildren(this.selected, c)
            return c
        }
    }
}
</script>

<style>
.dendro {
    position: relative;
}

.dendro canvas {
}

.dendro canvas.main {
    z-index: 1;
}
.dendro canvas.cut {
    position: absolute;
    z-index: 2;
    left: 0;
}
.dendro svg {
    position: absolute;
    z-index: 3;
    left: 0;
    top: 0;
}
</style>
