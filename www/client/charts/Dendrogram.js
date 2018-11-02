import { drawAxis } from 'charts/Functions'

import { select, event } from 'd3-selection'
import { scaleBand, scaleLinear } from 'd3-scale'
import { interpolateRound } from 'd3-interpolate'
import { min, max } from 'd3-array'
const d3 = { select, event, scaleBand, scaleLinear, interpolateRound, min, max }

function dendrogram(settings) {

    let chart = {}

    chart.settings = {
        data: null,
        cuttable: false,
        labels: false,
        axis: true,
        selectable: true,
        ratio: null,
        colors: null,
        selector: null
    }
    for (var setting in settings) {
        chart.settings[setting] = settings[setting]
    }

    chart.data = chart.settings.data
    chart.colors = chart.settings.colors

    /* Calculates x position based on label index. */
    function toX(d) {
        return chart.x(chart.data.labels[-d - 1]) + (chart.x.bandwidth() / 2)
    }

    /* Calculates positions of every split ("merge") in the tree. 
     * The merge matrix contains rows of size 2. If the element in
     * row is negative, then it is the index of the leaf. If positive,
     * it refers to a merge, which is a row in the merge matrix.
     */
    function buildPositions() {
        return chart.data.merge.reduce((acc, cur, i) => {
            const x1 = cur[0] < 0 ? toX(cur[0]) : acc[cur[0]-1]
            const x2 = cur[1] < 0 ? toX(cur[1]) : acc[cur[1]-1]
            acc.push(x1 + ((x2 - x1) / 2))
            return acc
        }, [])
    }

    !function init() {
        chart.container = d3.select(chart.settings.selector)

        chart.canvas = chart.container.select('canvas.main').node()
        chart.context = chart.canvas.getContext('2d')

        chart.height = 100
        chart.width = 100
        chart.colorHeight = chart.colors ? 20 : 0
        chart.colorsHeight = 0
        chart.colorsMargin = chart.colors ? 50 : 0
        chart.margin = {top: 10, right: 5, bottom: 5, left: chart.settings.axis ? 100 : 10 }

        chart.x = d3.scaleBand().paddingOuter(.5)
        chart.y = d3.scaleLinear().interpolate(d3.interpolateRound)
        chart.yReverse = d3.scaleLinear().interpolate(d3.interpolateRound)

        if (chart.settings.cuttable) {
            chart.cutCanvas = chart.container.select('canvas.cut').node()
            chart.cutContext = chart.cutCanvas.getContext('2d')
            chart.cutHeight = null
            initCut()
        }

        if (chart.settings.selectable) {
            chart.selectSvg = d3.select(chart.settings.selector).select('svg')
            initSelect()
        }

        resize()
        updateScales()
        initCanvas()
    }()

    function initCanvas() {
        // After resize, canvas is clear. Therefore setup again every resize
        chart.canvas.width = chart.width_
        chart.canvas.height = chart.height_
        chart.context.translate(chart.margin.left + .5, chart.margin.top + .5)
        chart.context.font = 'normal 12px sans-serif'

        if (chart.settings.cuttable) {
            chart.cutCanvas.width = chart.width_
            chart.cutCanvas.height = chart.y.range()[0]
            chart.cutContext.translate(chart.margin.left + .5, chart.margin.top + .5)
            chart.cutContext.lineWidth = 2
            chart.cutContext.strokeStyle = 'red'
        }
    }

    function initSelect() {
        chart.selectSvg.append('g')
            .attr('transform', `translate(${chart.margin.left + .5},${chart.margin.top + .5})`)
    }

    function initCut() {
        d3.select(chart.cutCanvas).on('mousemove', () => {
            const newHeight = d3.event.offsetY - chart.margin.top
            chart.cutContext.clearRect(-.5, -.5 - chart.margin.top, 
                chart.cutCanvas.width, chart.cutCanvas.height + chart.margin.top)
            chart.cutContext.beginPath()
            chart.cutContext.moveTo(0, newHeight)
            chart.cutContext.lineTo(chart.cutCanvas.width, newHeight)
            if (chart.cutHeight) {
                chart.cutContext.moveTo(0, chart.cutHeight)
                chart.cutContext.lineTo(chart.cutCanvas.width, chart.cutHeight)
            }
            chart.cutContext.stroke()
        }).on('click', () => {
            chart.cutHeight = d3.event.offsetY - chart.margin.top
            chart.cutContext.moveTo(0, chart.cutHeight)
            chart.cutContext.lineTo(chart.cutCanvas.width, chart.cutHeight)
        })
    }

    function resize() {
        chart.width_ = Math.round($(chart.settings.selector).parent().width())
        chart.width = chart.width_ - chart.margin.left - chart.margin.right
        if (chart.colors)
            chart.colorsHeight = Object.keys(chart.colors).length * chart.colorHeight
        chart.height_ = Math.round(chart.settings.ratio * chart.width_)
        chart.height_ += chart.colorsHeight  + chart.colorsMargin
        chart.height = chart.height_ - chart.margin.top - chart.margin.bottom

        if (chart.settings.selectable) {
            chart.recSize = Math.floor(chart.width / chart.data.ordered.length * .07)
            chart.selectSvg.attr('width', chart.width_).attr('height', chart.height_)
        }
    }

    function updateScales() {
        chart.x
            .domain(chart.data.ordered)
            .range([0, chart.width-25])

        const heightMin = d3.min(chart.data.height)
        const heightMax = d3.max(chart.data.height)
        chart.y
            .domain([Math.max(heightMin - 0.1 * (heightMax - heightMin), 0), heightMax])
            .range([chart.height - chart.colorsHeight - chart.colorsMargin, 0])
        chart.yReverse
            .domain(chart.y.range())
            .range(chart.y.domain())
    }

    function updateColors() {
        const yCluster = d3.scaleBand()
            .domain(Object.keys(chart.colors))
            .range([chart.height, chart.height - chart.colorsHeight])

        drawAxis(yCluster, chart.context, false)

        chart.context.beginPath()
        Object.keys(chart.colors).forEach((d, i) => {
            let values = chart.colors[d],
                y = yCluster(d)
            values.forEach((val, j) => {
                let x = chart.x(chart.data.ordered[j]),
                    width = chart.x.bandwidth() + chart.x.padding() * 2 + 1,
                    height = chart.colorHeight
                chart.context.fillStyle = val
                chart.context.fillRect(x, y, width, height)
            })
        })
        chart.context.fill()
    }

    function updateLabels(locations) {
        chart.context.save()
        chart.context.rotate(-Math.PI / 2)
        chart.context.textAlign = 'right'
        chart.context.textBaseline = 'top'
        chart.context.font = 'normal 15px sans-serif'
        for (let i = 0; i < chart.data.merge.length; i++) {
            let d = chart.data.merge[i],
                location = locations[i]
            chart.context.translate(location.x, location.y)
            if (chart.settings.labels && d[0] <= 0) {
                const x = d[0] < 0 ? toX(d[0]) : positions[d[0]-1]
                const y = chart.y(chart.data.height[i])
                chart.context.fillText(chart.data.labels[-d[0] - 1], 0, 0)
            }
        }
        chart.context.restore()
    }

    chart.update = function() {
        chart.context.clearRect(0, 0, chart.width, chart.height)

        const positions = buildPositions()
        const locations = chart.data.merge.map((d, i) => {
            // Element:
            //                    top
            //      left        -------------- right
            //      bottomleft  |            | 
            //                               | bottomright
            let left = d[0] < 0 ? toX(d[0]) : positions[d[0]-1],
                top = chart.y(chart.data.height[i]),
                right = d[1] < 0 ? toX(d[1]) : positions[d[1]-1],
                bottomLeft = d[0] < 0 ? chart.y(chart.data.height[i])+5 :
                                    chart.y(chart.data.height[d[0]-1]),
                bottomRight = d[1] < 0 ? chart.y(chart.data.height[i])+5 :
                                    chart.y(chart.data.height[d[1]-1])
            // Avoid anti aliasing effects
            left = Math.round(left)
            right = Math.round(right)
            return {left, top, right, bottomLeft, bottomRight}
        })

        // draw
        if (chart.settings.axis) drawAxis(chart.y, chart.context, true, 'Height')

        chart.context.beginPath()
        for (let i = 0; i < locations.length; i++) {
            const location = locations[i]

            // Horizontal line
            chart.context.moveTo(location.left, location.top)
            chart.context.lineTo(location.right, location.top)
            
            // Left line
            chart.context.moveTo(location.left, location.top)
            chart.context.lineTo(location.left, location.bottomLeft)

            // Right line
            chart.context.moveTo(location.right, location.top)
            chart.context.lineTo(location.right, location.bottomRight)
        }
        chart.context.stroke()

        if (chart.settings.selectable) {
            chart.selectSvg.select('g').selectAll('rect').data(positions)
                .enter().append('rect')
                .attr('x', d => d - (chart.recSize * .5))
                .attr('y', (d, i) => chart.y(chart.data.height[i]) - (chart.recSize * .5))
                .attr('width', chart.recSize)
                .attr('height', chart.recSize)
                .attr('fill', 'white')
                .attr('stroke', 'black')
                .style('cursor', 'pointer')
                .on('mouseover', function() { d3.select(this).attr('fill', 'red')})
                .on('mouseout', function() { d3.select(this).attr('fill', 'white')})
                .on('click', function(d, i) {
                    chart.settings.onSelect(i)
                })
        }

        if (chart.settings.labels) updateLabels(locations)
        if (chart.colors) updateColors()

        return chart
    }

    return chart
}

export default dendrogram