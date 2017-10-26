<template>
<div>
    <svg :width="width + margin.left + margin.right" 
         :height="height + margin.top + margin.bottom">
        <g :transform="`translate(${margin.left},${margin.top})`">
            <text
                v-for="(yVal, i) in this.yData"
                :key="i"
                text-anchor="middle"
                :x="x(xData[i])"
                :y="y(yVal)"
                :font-weight="highlight == xData[i] ? 'bold' : 'normal'"
                :fill="highlight == xData[i] ? 'red' : 'black'"> {{ xData[i] }}
            </text>
        </g>
    </svg>
</div>
</template>

<script>
import * as d3 from 'd3'

export default {
    data() {
        return {
            svg: null,
            x: d3.scaleLinear(),
            y: d3.scaleLinear(),
            height: 100,
            width: 100,
            margin: {top: 20, right: 20, bottom: 30, left: 50},
        }
    },

    props: ['xData', 'yData', 'highlight'],

    mounted() {
        this.width = parseInt(d3.select(this.$el).style('width'), 10)
        this.width = this.width - this.margin.left - this.margin.right
        this.height = this.width * 2 * .9
        this.height = this.height - this.margin.top - this.margin.bottom
        this.svg = d3.select(this.$el).select('svg').select('g')

        this.x
            .domain([Math.min(...this.xData), Math.max(...this.xData)])
            .range([0, this.width])
            
        this.y
            .domain([Math.max(...this.yData), 0])
            .range([0, this.height])

        this.svg.append('g')
            .attr('transform', 'translate(0,' + this.height + ')')
            .call(d3.axisBottom(this.x));

        this.svg.append('g')
            .call(d3.axisLeft(this.y))
    }
}
    
</script>