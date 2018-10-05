<template>
<svg :width="width + margin.left + margin.right" :height="height + margin.top + margin.bottom">
    <g :transform="`translate(${margin.left}, ${margin.top})`">
        <g id="axis-left" class="axis axis--y"></g>
        <g id="axis-bottom" class="axis axis--x" :transform="`translate(0, ${height})`"></g>
    </g>
</svg>
</template>

<script>
import { select } from 'd3-selection'
import { axisBottom, axisLeft } from 'd3-axis'
import { scalePoint, scaleLinear, scaleOrdinal } from 'd3-scale'
const d3 = { select, axisBottom, axisLeft, scalePoint, scaleLinear, scaleOrdinal }

export default {
    data() {
        return {
            height: 100,
            width: 100
        }
    },

    props: ['data'],

    methods: {
        resize() {
            const width = $(this.$el).parent().width() - this.margin.left - this.margin.right
            this.width = Math.min(this.data.columns.length * this.maxColHeight, width)
            const height = this.data.index.length * this.rowHeight
            this.height = height -  this.margin.top - this.margin.bottom
        },
        updatePlot() {
            // Scales
            this.x.domain(this.data.columns).rangeRound([0, this.width])
            this.y.domain(this.data.index).rangeRound([this.height, 0])
            this.r.range([0, Math.min(this.x.step(), this.y.step()) / 2])

            // Axes
            this.g.select('#axis-bottom')
                .transition()
                .call(d3.axisBottom(this.x).tickSizeInner(-this.height))
            this.g.select('#axis-left')
                .transition()
                .call(d3.axisLeft(this.y).tickSizeInner(-this.width))
            
            // Data
            const circle = this.g.selectAll('circle.corr').data(this.data.data)
            circle.exit().remove()
            circle.enter().append('circle')
                .classed('corr', true)
                .attr('cx', d => this.x(d.column))
                .attr('cy', d => this.y(d.index))
                .attr('fill', d => this.c(Math.sign(d.value)))
              .merge(circle).transition()
                .attr('r', d => this.r(Math.abs(d.value)))
        }
    },

    created() {
        this.margin = {top: 5, right: 5, bottom: 20, left: 100}
        this.rowHeight = 40
        this.maxColHeight = 85
        this.svg = null
        this.g = null
        this.x = d3.scalePoint().padding(.5)
        this.y = d3.scalePoint().padding(.5)
        this.r = d3.scaleLinear().domain([0, 1])
        this.c = d3.scaleOrdinal().domain([-1, 1]).range(['#0000e6', '#e60000'])
    },

    mounted() {
        this.svg = d3.select(this.$el)
        this.resize()
        this.g = this.svg.select('g')
        this.updatePlot()
    }
}
</script>

<style>
.axis .tick line {
  stroke: #000;
  stroke-opacity: 0.15;
}
</style>