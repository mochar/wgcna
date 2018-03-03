function drawAxis(scale, context, linear = true, label = '', tickCount = 10, tickSize = 6) {
    let tickPadding = 3,
        ticks = linear ? scale.ticks(tickCount) : scale.domain(),
        tickFormat = linear ? scale.tickFormat(tickCount) : d => d
    
    context.beginPath()
    ticks.forEach(d => {
        context.moveTo(0, scale(d))
        context.lineTo(-6, scale(d))
    })
    context.stroke()

    context.beginPath()
    context.moveTo(-tickSize, scale.range()[1])
    context.lineTo(0, scale.range()[1])
    context.lineTo(0, scale.range()[0])
    context.lineTo(-tickSize, scale.range()[0])
    context.stroke()

    context.save()

    context.textAlign = 'right'
    context.textBaseline = 'middle'
    ticks.forEach(d => {
        const y = linear ? scale(d) : scale(d) + scale.bandwidth() / 2
        context.fillText(tickFormat(d), -tickSize - tickPadding, y)
    })

    const halfWay = (scale.range()[1] - scale.range()[0]) / 2
    context.translate(-55, scale.range()[0] + halfWay)
    context.rotate(-Math.PI / 2)
    context.textAlign = 'right'
    context.textBaseline = 'top'
    context.font = 'normal 15px sans-serif'
    context.fillText(label, 0, 0)

    context.restore()
}

export { drawAxis }