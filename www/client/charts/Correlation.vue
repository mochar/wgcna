<template>
<svg :width="width" :height="height">
    <g :transform="`translate(${width/2}, ${height/2})`">
        <defs>
        </defs>
    </g>
</svg>
</template>

<script>
import * as d3 from 'd3'

export default {
    data() {
        return {
            svg: null,
            height: 100,
            width: 100,

            radius: null,
            arc: d3.arc().cornerRadius(20),
            symbol: d3.symbol().size(400)
        }
    },

    props: ['data', 'names'],

    methods: {
        resize() {
            this.width = $(this.$el).parent().width()
            this.height = this.width * .7
            this.radius = this.height / 2
            this.arc.outerRadius(this.radius - 5).innerRadius(this.radius - 55)
        },
        arcsToDefPaths(arcs) {
            const defPaths = arcs.reduce((d, arc, i) => {
                if (d.current.group == arc.data.group) {
                    d.current.endAngle = arc.endAngle
                } else {
                    if (d.current.group != 'dummies')
                        d.all.push(Object.assign({}, d.current))
                    d.current.group = arc.data.group
                    d.current.name = arc.data.group.replace(/\s+/g, '')
                    d.current.startAngle = arc.startAngle
                    d.current.endAngle = arc.endAngle
                }
                return d
            }, {all: [], current: {group: null}}).all
            defPaths.splice(0, 1)
            return defPaths
        },
        updatePlot() {
            const arcs = d3.pie()
                .sort(null)
                .sortValues(null)
                .padAngle(.03)
                .value(d => 1)
                (this.data.nodes)

            // Line
            const arcsMap = d3.map(arcs, d => `${d.data.name}_${d.data.group}`)
            const ribbon = d3.ribbon().radius(this.radius - 50)
            // const widthScale = d3.scaleLinear().domain([0.5, 1]).range([2, 3]) // 3,5
            // const opScale = d3.scaleLinear().domain([0.5, 1]).range([.5, .9])
            const widthScale = d3.scaleLinear().domain([0, 1]).range([2, 3]) // 3,5
            const opScale = d3.scaleLinear().domain([0, 1]).range([.5, .9])
            const line = this.svg.selectAll('.line').data(this.data.links)
            line.enter().append('path')
                .classed('line', true)
                .attr('stroke', d => d.value > 0 ? 'red' : 'blue')
                .attr('stroke-width', d => widthScale(Math.abs(d.value)))
                .attr('opacity', d => opScale(Math.abs(d.value)))
                .attr("d", d => {
                    const source = arcsMap.get(`${d.source.name}_${d.source.group}`)
                    const target = arcsMap.get(`${d.target.name}_${d.target.group}`)
                    const sourceAngle = source.startAngle + ((source.endAngle - source.startAngle) / 2)
                    const targetAngle = target.startAngle + ((target.endAngle - target.startAngle) / 2)
                    return ribbon({
                        source: { startAngle: sourceAngle, endAngle: sourceAngle },
                        target: { startAngle: targetAngle, endAngle: targetAngle }
                    })
                })

            // Def paths
            const defPaths = this.arcsToDefPaths(arcs)
            const path = this.svg.select('defs').selectAll('path').data(defPaths, d => d.group)
            path.enter().append('path')
                .attr('id', d => `path-${d.name}`)
                .attr('d', this.arc.outerRadius(this.radius - 20))
            
            // Def names
            const name = this.svg.selectAll('.name').data(defPaths, d => d.group)
            name.enter().append('text')
                .classed('name', true)
                .attr('dx', 65)
                .attr('dy', -5)
              .append('textPath')
                .attr('xlink:href', d => `#path-${d.name}`)
                .text(d => d.group)

            // Node
            const node = this.svg.selectAll('.node').data(arcs)
            node.enter().append('path')
                .classed('node', true)
                .on('mouseover', d => { 
                    console.log(`${d.data.group}: ${d.data.name}`)
                })
                .on('click', function(d) {
                    d3.select(this).attr('fill', 'white').attr('stroke', 'black')
                })
                .attr('title', d => d.data.name)
                .attr('d', d => this.symbol.type(d3.symbolCircle)())
                .attr('transform', d => {
                    const centroid = this.arc.centroid(d)
                    return `translate(${centroid[0]},${centroid[1]})`
                })
                .attr('fill', d => d.data.group === 'dummies' ? 'transparent' : 'black')
        }
    },

    mounted() {
        this.svg = d3.select(this.$el).select('g')
        this.resize()
    },

    watch: {
        data() {
            if (this.data) this.updatePlot()
        }
    }
}
</script>

<style>
.name {
    font-size: 1.2rem;
}
</style>
