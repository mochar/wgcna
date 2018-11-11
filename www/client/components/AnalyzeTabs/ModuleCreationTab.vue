<template>
<div>
    <threshold  @done="thresholdDone" />
    <cluster  v-if="project.power" @done="clusterDone" />
</div>
</template>

<script>
import Threshold from 'components/Threshold'
import Cluster from 'components/Cluster'

export default {
    props: ['project'],

    components: {
        Threshold,
        Cluster
    },

    methods: {
        thresholdDone(power) {
            this.$store.commit('editProject', { power, minModuleSize: null })
        },
        clusterDone(minModuleSize) {
            this.$store.commit('editProject', { minModuleSize })
        }
    }
}
</script>
