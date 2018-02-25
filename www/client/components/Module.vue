<template>
<div class="card card-body block">
    <span>{{ name }}</span>
    <div class="chart-wrapper" :id="`module-${name}`"></div>
</div>
</template>

<script>
import makeDistroChart from '../external/distrochart'

export default {
    props: ['name', 'data', 'samples', 'groups'],

    watch: {
        groups() {
            this.chart.update()
            this.chart.boxPlots.update()
            this.chart.dataPlots.update()
            this.chart.notchBoxes.update()
        }
    },

    mounted() {
        const data = this.data.map((d, i) => ({ group: this.groups[i], value: d}))
        this.chart = makeDistroChart({
            data: data,
            xName: 'group',
            yName: 'value',
            axisLabels: {xAxis: null, yAxis: 'Eigengene'},
            selector: `#module-${this.name}`,
            chartSize: {height:350, width:960},
            constrainExtremes:true})
        this.chart.update()
        this.chart.renderBoxPlot()
        this.chart.renderDataPlots({showPlot: true, showbeanLines:true})
        this.chart.renderNotchBoxes({showNotchBox:false, showLines:false})
        // this.chart.renderViolinPlot({ bandWidth: 1 })
    }
}
</script>
