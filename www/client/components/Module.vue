<template>
<div class="card card-body block">
    <span>{{ name }}</span>
    <div class="chart-wrapper" :id="id"></div>
</div>
</template>

<script>
import makeDistroChart from '../external/distrochart'

export default {
    props: ['name', 'data', 'samples', 'groups'],

    methods: {
        processData() {
            return this.data.map((d, i) => ({ group: this.groups[i], value: d}))
        },
        createChart() {
            $(`#${this.id}`).empty()
            this.chart = makeDistroChart({
                data: this.processData(),
                xName: 'group',
                yName: 'value',
                axisLabels: {xAxis: null, yAxis: 'Eigengene'},
                selector: `#${this.id}`,
                chartSize: {height:350, width:960},
                constrainExtremes:true})
            this.chart.update()
            this.chart.renderBoxPlot()
            this.chart.renderDataPlots({showPlot: true, showbeanLines:true})
            this.chart.renderNotchBoxes({showNotchBox:false, showLines:false})
            // this.chart.renderViolinPlot({ bandWidth: .10 })
        }
    },

    computed: {
        id() {
            return `module-${this.name}`
        }
    },

    watch: {
        groups() {
            this.createChart()
        }
    },

    mounted() {
        this.createChart()
    }
}
</script>
