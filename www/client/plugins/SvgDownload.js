// From:
// https://bitbucket.org/mas29/public_resources/raw/b9bafa002053b4609bd5186010d19e959cba33d4/scripts/js/svg_download/downloadSVG.js

const prefix = {
    xmlns: 'http://www.w3.org/2000/xmlns/',
    xlink: 'http://www.w3.org/1999/xlink',
    svg: 'http://www.w3.org/2000/svg'
}

function download(svgEl, filename) {
    const source = getSource(svgEl)
    const url = window.URL.createObjectURL(new Blob(source.source, { 'type' : 'text\/xml' }))
    const a = document.createElement('a')
    document.body.appendChild(a)
    a.setAttribute('class', 'svg-crowbar')
    a.setAttribute('download', filename + '.svg')
    a.setAttribute('href', url)
    a.style['display'] = 'none'
    a.click()
    setTimeout(() => window.URL.revokeObjectURL(url), 10)
}

function getSource(svg) {
    const styles = getStyles()

    svg.setAttribute('version', '1.1')
    const defsEl = document.createElement('defs')
    svg.insertBefore(defsEl, svg.firstChild); //TODO   .insert('defs', ':first-child')
    // defsEl.setAttribute('class', 'svg-crowbar');

    const styleEl = document.createElement('style')
    defsEl.appendChild(styleEl)
    styleEl.setAttribute('type', 'text/css')

    // removing attributes so they aren't doubled up
    svg.removeAttribute('xmlns')
    svg.removeAttribute('xlink')

    // These are needed for the svg
    if (!svg.hasAttributeNS(prefix.xmlns, 'xmlns')) {
        svg.setAttributeNS(prefix.xmlns, 'xmlns', prefix.svg)
    }
    if (!svg.hasAttributeNS(prefix.xmlns, 'xmlns:xlink')) {
        svg.setAttributeNS(prefix.xmlns, 'xmlns:xlink', prefix.xlink)
    }

    const source = (new XMLSerializer()).serializeToString(svg).replace('</style>', '<![CDATA[' + styles + ']]></style>')
    const rect = svg.getBoundingClientRect()
    const doctype = '<?xml version="1.0" standalone="no"?><!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">'
    return {
        top: rect.top,
        left: rect.left,
        width: rect.width,
        height: rect.height,
        class: svg.getAttribute('class'),
        id: svg.getAttribute('id'),
        childElementCount: svg.childElementCount,
        source: [doctype + source]
    }
}

function getStyles() {
    let styles = ''
    const styleSheets = document.styleSheets

    if (styleSheets) {
        for (var i = 0; i < styleSheets.length; i++) {
            processStyleSheet(styleSheets[i])
        }
    }

    function processStyleSheet(ss) {
        if (ss.cssRules) {
            for (var i = 0; i < ss.cssRules.length; i++) {
                var rule = ss.cssRules[i]
                if (rule.type === 3) {
                    // Import Rule
                    processStyleSheet(rule.styleSheet)
                } else {
                    // hack for illustrator crashing on descendent selectors
                    if (rule.selectorText) {
                        if (rule.selectorText.indexOf(">") === -1) {
                            styles += "\n" + rule.cssText
                        }
                    }
                }
            }
        }
    }

    return styles
}

export default download