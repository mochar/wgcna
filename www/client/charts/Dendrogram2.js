import * as d3 from 'd3'
import { drawAxis, scaleRadial } from 'charts/Functions'

function dendrogram(settings) {

    let chart = {}

    chart.settings = {
        data: null,
        names: null,
        ratio: null,
        selector: null
    }
    for (var setting in settings) {
        chart.settings[setting] = settings[setting]
    }

    chart.data = chart.settings.data

    function toX(d, i) {
        return chart.x[i](chart.data[i].labels[-d - 1]) + (chart.x[i].bandwidth() / 2)
        return chart.x[i](chart.data[i].labels[-d - 1])
    }

    function buildPositions(z) {
        return chart.data[z].merge.reduce((prev, cur, i) => {
            const x1 = cur[0] < 0 ? toX(cur[0], z) : prev[cur[0]-1]
            const x2 = cur[1] < 0 ? toX(cur[1], z) : prev[cur[1]-1]
            prev.push(x1 + ((x2 - x1) / 2))
            return prev
        }, [])
    }

    !function init() {
        console.log('init')
        chart.container = d3.select(chart.settings.selector)

        chart.canvas = chart.container.select('canvas.main').node()
        chart.context = chart.canvas.getContext('2d')

        chart.height = 100
        chart.width = 100
        chart.margin = {top: 10, right: 5, bottom: 5, left: 10}
        chart.innerRadius = 275
        chart.outerRadius = 400

        chart.x = chart.data.map(d => d3.scaleBand().paddingOuter(.5))
        chart.y = chart.data.map(d => d3.scaleLinear().interpolate(d3.interpolateRound))

        resize()
        updateScales()
        initCanvas()
    }()

    function initCanvas() {
        // After resize, canvas is clear. Therefore setup again every resize
        chart.canvas.width = chart.width_
        chart.canvas.height = chart.height_
        chart.context.translate(chart.margin.left + .5, chart.margin.top + .5)
        chart.context.translate(chart.width / 2, chart.height / 2)
        chart.context.font = 'normal 12px sans-serif'
        chart.context.lineWidth = 1.5
    }

    function resize() {
        chart.width_ = Math.round($(chart.settings.selector).parent().width())
        chart.width = chart.width_ - chart.margin.left - chart.margin.right
        chart.height_ = Math.round(chart.settings.ratio * chart.width_)
        chart.height = chart.height_ - chart.margin.top - chart.margin.bottom
        chart.outerRadius = Math.min(chart.width, chart.height) * .45
    }

    function updateScales() {
        // const heights = Array.prototype.concat(...chart.data.map(d => d.height))
        // const heightMin = d3.min(heights)
        // const heightMax = d3.max(heights)

        for (let i = 0; i < chart.data.length; i++) {
            chart.x[i]
                .domain(chart.data[i].ordered)
                .range([0, chart.width])
            let heightMin = d3.min(chart.data[i].height)
            let heightMax = d3.max(chart.data[i].height)
            chart.y[i]
                .domain([Math.max(heightMin - .1 * (heightMax - heightMin), 0), heightMax])
                .range([chart.height, 0])
        }
    }

    function divide() {
        const data = chart.data.map(d => d.labels.length)
        const arcs = d3.pie().padAngle(.1)(data)
        return arcs
    }

    chart.update = function() {
        let x = d3.scaleLinear()
            .domain([0, chart.width])
        let y = d3.scaleLinear()
            .range([chart.innerRadius, chart.outerRadius])
        let line = d3.lineRadial()
            .angle(d => x(d[0]) + Math.PI * .5)
            .radius(d => y(d[1]))
            .context(chart.context)

        const arcs = divide()
        for (let z = 0; z < arcs.length; z++) {
            x.range([arcs[z].startAngle, arcs[z].endAngle])
            y.domain(chart.y[z].range())

            let positions = buildPositions(z)
            let locations = chart.data[z].merge.map((d, i) => {
                // Element:
                //                    top
                //      left        -------------- right
                //      bottomleft  |            | 
                //                               | bottomright
                let left = d[0] < 0 ? toX(d[0], z) : positions[d[0]-1],
                    top = chart.y[z](chart.data[z].height[i]),
                    right = d[1] < 0 ? toX(d[1], z) : positions[d[1]-1],
                    // bottomLeft = d[0] < 0 ? chart.y(chart.data.height[i])+5 :
                    //                     chart.y(chart.data.height[d[0]-1]),
                    // bottomRight = d[1] < 0 ? chart.y(chart.data.height[i])+5 :
                    //                     chart.y(chart.data.height[d[1]-1])
                    bottomLeft = d[0] < 0 ? chart.y[z].range()[0] :
                                        chart.y[z](chart.data[z].height[d[0]-1]),
                    bottomRight = d[1] < 0 ? chart.y[z].range()[0] :
                                        chart.y[z](chart.data[z].height[d[1]-1])

                return {left, top, right, bottomLeft, bottomRight}
            })

            // draw
            
            for (let i = 0; i < locations.length; i++) {
                const location = locations[i]

                // Horizontal line
                chart.context.beginPath()
                let start_ = x(location.left), 
                    startShifted = start_ - Math.PI / 2,
                    start = startShifted < 0 ? 2 * Math.PI + startShifted : startShifted,
                    end_ = x(location.right), 
                    endShifted = end_ - Math.PI / 2,
                    end = endShifted < 0 ? 2 * Math.PI + endShifted : endShifted,
                    top = y(location.top)
                chart.context.arc(0, 0, top, start_, end_)
                chart.context.stroke()

                chart.context.beginPath()
                // Left line
                line([
                    [location.left, location.top],
                    [location.left, location.bottomLeft]
                ])
                // Right line
                line([
                    [location.right, location.top],
                    [location.right, location.bottomRight]
                ])
                chart.context.stroke()
            }
        }

        return chart
    }

    return chart
}

export default dendrogram