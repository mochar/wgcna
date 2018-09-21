import svgDownload from './SvgDownload'

let helpers = {
    mode: function(arr) {
        // Return the most frequent item in an array.
        return arr.sort((a,b) =>
            arr.filter(v => v === a).length - arr.filter(v => v === b).length
        ).pop()
    },
    range: function(start, end, step) {
        const _end = end || start
        const _start = end ? start : 0
        const _step = step || 1
        return Array((_end - _start) / _step).fill(0).map((v, i) => _start + (i * _step))
    },
    unique: function(array) {
        return [...new Set(array)]
    },
    flatten: function(arr) {
        return Array.prototype.concat(...arr)
    },
    downloadSvg: function(svgEl, filename) {
        svgDownload(svgEl, filename)
    }
}

export default {
    install: (Vue, options) => {
        Vue.prototype.$helpers = helpers
    }
}