<template>
<svg id="cross-plot"></svg>
</template>

<script>
import dendrogram from 'charts/Dendrogram3.js'

export default {
    props: {
        data: Array,
        names: Array,
        Ratio: Number
    },

    mounted() {
        const chart = dendrogram({
            selector: '#cross-plot',
            data: this.data,
            names: this.names,
            ratio: this.ratio
        })
        chart.update()
    }

}
</script>

<style>

</style>
