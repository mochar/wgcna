<template>
<div>
    <div class="preprocess-component">
        <sample-tree
            :projectId="project.id"
            :cuttable="true"
            @loaded="loading = false"
            @cutted="d => outlierSamples = d">
        </sample-tree>
        <span class="fa fa-refresh fa-spin" v-if="loading"></span>
    </div>
    <div class="mt-2" v-show="!loading">
        <button class="btn btn-light" :disabled="busy" @click="go">
            <span class="fa fa-check"></span>
            OK
        </button>
    </div>
</div>
</template>

<script>
import SampleTree from 'components/SampleTree'

export default {
    data() {
        return {
            loading: true,
            busy: false,
            outlierSamples: []
        }
    },

    components: {
        SampleTree
    },

    props: ['project'],

    methods: {
        go() {
            this.busy = true
            const formData = new FormData()
            this.outlierSamples.forEach(sample => formData.append('samples[]', sample))
            $.post({
                url: `${ROOTURL}/projects/${this.project.id}/clustersamples`,
                data: formData,
                async: true,
                cache: false,
                contentType: false,
                processData: false
            }).then(data => {
                this.$emit('done')
            }, () => {
                this.busy = false
                alert('fail')
            }).then(() => this.loading = false)
        }
    }
}
</script>