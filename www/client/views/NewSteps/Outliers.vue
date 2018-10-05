<template>
<div class="card card-body block mt-3">
    <div class="d-flex justify-content-between align-items-start">
        <h6 class="block-title text-uppercase">
            Sample outliers
        </h6>
    </div>

    <div>
        <sample-tree
            :projectId="project"
            :cuttable="true"
            @loaded="building = false"
            @cutted="d => outlierSamples = d">
        </sample-tree>
        <font-awesome-icon icon="sync" spin v-if="building" />
    </div>

    <list-popover name="Outlier samples" :list="outlierSamples" v-if="outlierSamples.length"></list-popover>

    <div class="mt-3" v-if="!building">
        <button class="btn btn-primary" @click="done" :disabled="loading">
            <font-awesome-icon icon="check" />
            OK
        </button>
    </div>
</div>
</template>

<script>
import SampleTree from 'components/SampleTree'
import ListPopover from 'components/ListPopover'

export default {
    data() {
        return {
            loading: false,
            building: true,
            outlierSamples: []
        }
    },

    props: {
        project: String
    },

    components: {
        SampleTree,
        ListPopover
    },

    methods: {
        done() {
            this.loading = true
            const formData = new FormData()
            this.outlierSamples.forEach(sample => formData.append('samples[]', sample))
            this.$helpers.post(formData, this.project, 'clustersamples')
            .then(data => {
                this.$emit('done')
            }, () => {
                this.loading = false
                alert('fail')
            })
        }
    }
}
</script>
