<script>
let helpers = {
    mode: function(arr) {
        // Return the most frequent item in an array.
        return arr.sort((a,b) =>
            arr.filter(v => v === a).length - arr.filter(v => v === b).length
        ).pop()
    },
    range: n => Array.from(Array(n).keys())
}

export default {
    install: (Vue, options) => {
        Vue.prototype.$helpers = helpers
    }
}
</script>