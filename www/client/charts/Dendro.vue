<template>
<div class="dendro" id="tree">
    <canvas class="main"></canvas>
    <canvas class="cut"></canvas>
</div>
</template>

<script>
import dendrogram from 'charts/Dendrogram.js'

export default {
    props: {
        clusterData: Object,
        cuttable: Boolean,
        labels: Boolean,
        ratio: Number,
        colors: Object
    },

    mounted() {
        const chart = dendrogram({
            selector: '#tree',
            data: this.clusterData,
            cuttable: this.cuttable,
            labels: this.labels,
            ratio: this.ratio,
            colors: this.colors
        })
        chart.update()
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
</style>
