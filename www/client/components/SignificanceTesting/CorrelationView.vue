<template>
<div class="card card-body block">
    <div class="d-flex justify-content-between align-items-start">
        <h6 class="block-title text-uppercase">
            Correlation with traits
        </h6>
    </div>
    <p class="card-text">
        View the correlations of module eigengenes with the traits.
    </p>

    <div class="d-flex justify-content-center">
        <correlations :data="data" v-if="!loading"></correlations>
    </div>

    <div class="mt-2">
        <button @click="$emit('back')" class="btn btn-light">
            <font-awesome-icon icon="angle-double-left" />
            Return
        </button>
    </div>
</div>
</template>

<script>
import Correlations from 'components/SignificanceTesting/Correlations'

export default {
    data() {
        return {
            loading: true
        }
    },

    components: {
        Correlations
    },

    props: ['project'],

    created() {
        $.getJSON(`${ROOTURL}/projects/${this.project.id}/correlate`).then(data => {
            let processed = []
            for (let i = 0; i < data.index.length; i++) {
                for (let j = 0; j < data.columns.length; j++) {
                    const d = {index: data.index[i], column: data.columns[j],
                               value: data.data[i][j]}
                    processed.push(d)
                }
            }
            data.data = processed
            this.data = data
            this.loading = false
        })
    }
}
</script>
