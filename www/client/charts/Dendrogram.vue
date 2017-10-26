<template>
<svg :width="width" :height="height">
    <g :transform="`translate(${margin.left}, ${margin.top})`">
        <g class="axis axis--y"></g>
        <line id="cutline" stroke="red" opacity="0.8" x1="0" :x2="width"></line>
        <line id="cutlineset" stroke="red" stroke-width="2" v-if="cutHeight" x1="0" :x2="width"
            :y1="cutHeight" :y2="cutHeight"></line>
    </g>
</svg>
</template>

<script>
import * as d3 from 'd3'

export default {
    data() {
        return {
            svg: null,
            g: null,
            cutline: null,
            cutlineset:null,
            cutHeight: null,
            height: 100,
            width: 100,
            x: d3.scalePoint().range([0, this.width]).padding(.4),
            y: d3.scaleLinear().range([this.height, 0]),
            axis: d3.axisLeft(this.y),
            zoom: d3.zoom(),
            margin: {top: 10, right: 5, bottom: 15, left: 25},
            colors: d3.scaleOrdinal(d3.schemeCategory10),
            clusters: null
        }
    },

    props: ['clusterData', 'cuttable'],

    methods: {
        updateCutLine() {
            const ordered = this.clusterData.ordered
            const newHeight = d3.event.offsetY - this.margin.top
            this.cutline
                .attr('y1', newHeight)
                .attr('y2', newHeight)
        },
        cut(event) {
            this.cutHeight = d3.event.offsetY - this.margin.top
            const reverseY = d3.scaleLinear()
                .domain(this.y.range())
                .range(this.y.domain())
            const cutHeightTree = reverseY(this.cutHeight)

            const cutMerges = this.clusterData.merge.reduce((prevs, cur, i) => {
                if (this.clusterData.height[i] >= cutHeightTree) {
                    if (!prevs.includes(i + 1)) prevs.push(i + 1)
                    if (cur[0] > 0 && !prevs.includes(cur[0])) prevs.push(cur[0])
                    if (cur[1] > 0 && !prevs.includes(cur[1])) prevs.push(cur[1])
                }
                return prevs
            }, [])

            let mergeToClust = {}
            let labelClusters = this.clusterData.labels.map(d => 0)
            let mergeClusters = this.clusterData.merge.map(d => 0)
            let curClust = 0
            for (let i = this.clusterData.merge.length - 1; i >= 0; i--) {
                let cluster
                if (cutMerges.includes(i + 1)) {
                    cluster = ++curClust
                    mergeClusters[i] = curClust
                } else {
                    cluster = mergeClusters[i]
                }

                const merge = this.clusterData.merge[i]
                if (merge[0] < 0) {
                    labelClusters[-merge[0] - 1] = cluster
                } else if (this.clusterData.height[merge[0]-1] <= cutHeightTree) {
                    mergeClusters[merge[0] - 1] = cluster
                }
                if (merge[1] < 0) {
                    labelClusters[-merge[1] - 1] = cluster
                } else if (this.clusterData.height[merge[1]-1] <= cutHeightTree) {
                    mergeClusters[merge[1] - 1] = cluster
                }
            }

            this.clusters = {labelClusters, mergeClusters}
            this.updatePlot()
        },
        buildPositions() {
            const labels = this.clusterData.labels
            return this.clusterData.merge.reduce((prev, cur, i) => {
                const x1 = cur[0] < 0 ? this.x(labels[-cur[0]-1]) : prev[cur[0]-1]
                const x2 = cur[1] < 0 ? this.x(labels[-cur[1]-1]) : prev[cur[1]-1]
                prev.push(x1 + ((x2 - x1) / 2))
                return prev
            }, [])
        },
        resize() {
            this.width = $(this.$el).parent().width() - this.margin.left - this.margin.right
            this.height = (0.75 * this.width) - this.margin.top - this.margin.bottom
        },
        zoomed() {
            const yt = d3.event.transform.rescaleY(this.y)
            this.g.select('.axis--y').call(this.axis.scale(yt))
        },
        updatePlot() {
            this.x
                .domain(this.clusterData.ordered)
                .range([0, this.width-10])

            this.y
                .domain([Math.max(d3.min(this.clusterData.height)-5, 0), d3.max(this.clusterData.height)])
                // .domain([0, d3.max(this.clusterData.height)])
                .range([this.height, 0])
            
            this.axis.scale(this.y)
            this.g.select('.axis--y').call(this.axis)

            const labels = this.clusterData.labels
            const positions = this.buildPositions()

            const group = this.g.selectAll('.group')
                .data(this.clusterData.merge, d => `${d[0]}_${d[1]}`)
            group.exit().remove()
            const groupEnter = group.enter().append('g').classed('tree-line', true)
            groupEnter.append('line')
                .attr('x1', d => d[0] < 0 ? this.x(labels[-d[0]-1]) : positions[d[0]-1])
                .attr('x2', d => d[1] < 0 ? this.x(labels[-d[1]-1]) : positions[d[1]-1])
                .attr('y1', (d, i) => this.y(this.clusterData.height[i]))
                .attr('y2', (d, i) => this.y(this.clusterData.height[i]))
                .attr('stroke', (d, i) => {
                    if (!this.clusters) return 'black'
                    const leftCluster = d[0] < 0 ? this.clusters.labelClusters[-d[0] - 1] : 
                                                   this.clusters.mergeClusters[d[0] - 1]
                    const rightCluster = d[1] < 0 ? this.clusters.labelClusters[-d[1] - 1] : 
                                                    this.clusters.mergeClusters[d[1] - 1]
                    return leftCluster === rightCluster ? this.colors(leftCluster) : 'black'
                })
            // Left
            groupEnter.append('line')
                .attr('x1', d => d[0] < 0 ? this.x(labels[-d[0]-1]) : positions[d[0]-1])
                .attr('x2', d => d[0] < 0 ? this.x(labels[-d[0]-1]) : positions[d[0]-1])
                .attr('y1', (d, i) => this.y(this.clusterData.height[i]))
                .attr('y2', (d, i) => {
                    if (d[0] < 0) return this.y(this.clusterData.height[i])+5
                    return this.y(this.clusterData.height[d[0]-1])
                })
                .attr('stroke', (d, i) => {
                    if (!this.clusters) return 'black'
                    const cluster = d[0] < 0 ? this.clusters.labelClusters[-d[0] - 1] : 
                                               this.clusters.mergeClusters[d[0] - 1]
                    return this.colors(cluster)
                })
            groupEnter.append('text')
                .attr('transform', (d, i) => {
                    const x = d[0] < 0 ? this.x(labels[-d[0]-1]) : positions[d[0]-1]
                    const y = this.y(this.clusterData.height[i])
                    return `translate(${x-3},${y+10})rotate(90)`
                })
                .text((d, i) => {
                    if (d[0] > 0) return ''
                    return this.clusterData.labels[-d[0] - 1]
                })
            // Right
            groupEnter.append('line') 
                .attr('x1', d => d[1] < 0 ? this.x(labels[-d[1]-1]) : positions[d[1]-1])
                .attr('x2', d => d[1] < 0 ? this.x(labels[-d[1]-1]) : positions[d[1]-1])
                .attr('y1', (d, i) => this.y(this.clusterData.height[i]))
                .attr('y2', (d, i) => {
                    if (d[1] < 0) return this.y(this.clusterData.height[i])+5
                    return this.y(this.clusterData.height[d[1]-1])
                })
                .attr('stroke', (d, i) => {
                    if (!this.clusters) return 'black'
                    const cluster = d[1] < 0 ? this.clusters.labelClusters[-d[1] - 1] : 
                                               this.clusters.mergeClusters[d[1] - 1]
                    return this.colors(cluster)
                })
            groupEnter.append('text')
                .attr('transform', (d, i) => {
                    const x = d[1] < 0 ? this.x(labels[-d[1]-1]) : positions[d[1]-1]
                    const y = this.y(this.clusterData.height[i])
                    return `translate(${x-3},${y+10})rotate(90)`
                })
                .text((d, i) => {
                    if (d[1] > 0) return ''
                    return this.clusterData.labels[-d[1] - 1]
                })
        }
    },

    mounted() {
        this.svg = d3.select(this.$el)
        this.resize()
        this.g = this.svg.select('g')
        if (this.cuttable) {
            this.svg.on('mousemove', this.updateCutLine)
            this.svg.on('click', this.cut)
        }
        this.cutline = this.g.select('line#cutline')
        this.cutlineset = this.g.select('line#cutlineset')
        this.zoom
            .scaleExtent([1, 40])
            .extent([[0, 0], [this.width, this.height]])
            .on('zoom', this.zoomed)
        // this.svg.call(this.zoom)
        this.updatePlot()
    },

    watch: {
        clusterData() {
            if (!this.clusterData) return
            this.updatePlot()
        }
    }
}
</script>

<style>
text {
    font-size: 12px;
}

line {
    shape-rendering: crispEdges;
}
</style>