<template>
<div class="card card-body block">
    <div class="d-flex justify-content-between align-items-baseline">
        <h6 class="block-title text-uppercase">
            {{ name }}
        </h6>
        <button class="btn btn-light" @click="download">
            <font-awesome-icon icon="download" fixed-width />
            Download module
        </button>
    </div>
    <div class="chart-wrapper" :id="id"></div>
</div>
</template>

<script>
import makeDistroChart from '../external/distrochart'
import { scaleOrdinal } from 'd3-scale'
import { schemePastel1 } from 'd3-scale-chromatic'

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
                yRange: [-1, 1],
                color: scaleOrdinal(schemePastel1),
                constrainExtremes:true})
            this.chart.update()
            this.chart.renderBoxPlot()
            this.chart.renderDataPlots({showPlot: true, showbeanLines:true})
            this.chart.renderNotchBoxes({showNotchBox:false, showLines:false})
            // this.chart.renderViolinPlot({ bandWidth: .10 })
        },
        download() {

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
    },

    updated() {
        this.createChart()
    }
}
</script>
