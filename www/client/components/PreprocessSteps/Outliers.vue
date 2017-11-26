<template>
<div>
    <sample-tree
        :projectId="projectId"
        :cuttable="true"
        @loaded="loaded"
        @cutted="d => outlierSamples = d">
    </sample-tree>
    <span class="fa fa-refresh fa-spin" v-if="loading"></span>
</div>
</template>

<script>
import SampleTree from 'components/SampleTree'

export default {
    data() {
        return {
            loading: true,
            outlierSamples: []
        }
    },

    components: {
        SampleTree
    },

    props: ['projectId', 'go'],

    methods: {
        done() {
            this.loading = true
            const formData = new FormData()
            this.outlierSamples.forEach(sample => formData.append('samples[]', sample))
            $.post({
                url: `${ROOTURL}/projects/${this.projectId}/clustersamples`,
                data: formData,
                async: true,
                cache: false,
                contentType: false,
                processData: false
            }).then(data => {
                this.$emit('done')
            }, () => {
                alert('fail')
            }).then(() => this.loading = false)
        },
        loaded() {
            this.loading = false
            this.$emit('loaded')
        }
    },

    watch: {
        go() {
            if (this.go) this.done()
        }
    }
}
</script>