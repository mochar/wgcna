<template>
<div>
    <treshold 
        :project="project" 
        :update="shouldUpdate"
        v-if="project.step > 0" 
        @done="tresholdDone">
    </treshold>
    <cluster 
        :project="project" 
        :update="shouldUpdate || project.step == 2"
        v-if="project.step > 1"
        @cutting="$store.commit('editProject', {step: 3})"
        @done="clusterDone">
    </cluster>
</div>
</template>

<script>
import Treshold from 'components/Treshold'
import Cluster from 'components/Cluster'

export default {
    props: ['project', 'shouldUpdate'],

    components: {
        Treshold,
        Cluster
    },

    methods: {
        tresholdDone(power) {
            this.$store.commit('editProject', {step: 2, power})
        },
        clusterDone(minModuleSize) {
            this.$store.commit('editProject', {step: 4, minModuleSize })
        }
    }
}
</script>
