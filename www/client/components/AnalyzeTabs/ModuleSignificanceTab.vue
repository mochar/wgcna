<template>
<div>
    <genotype
        :project="project" 
        :update="shouldUpdate || project.step == 4"
        @done="genotypeDone"
        v-if="project.step > 3">
    </genotype>
</div>
</template>

<script>
import Genotype from 'components/Genotype'

export default {
    props: ['project', 'shouldUpdate'],

    components: {
        Genotype
    },
    
    methods: {
        genotypeDone() {
            this.$store.commit('editProject', {step: 5})
        }
    }
}
</script>
