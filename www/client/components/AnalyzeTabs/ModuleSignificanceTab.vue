<template>
<div>
    <!-- <genotype
        :project="project" 
        :update="shouldUpdate || project.step == 4"
        @done="genotypeDone"
        v-if="project.step > 3">
    </genotype> -->

    <div id="significance-container" class="d-flex align-items-start">
        <div class="card card-body block mr-1" style="flex: 1">
            <div class="d-flex justify-content-between align-items-start">
                <h6 class="block-title text-uppercase">
                    Differential expression
                </h6>
            </div>
            <p class="card-text">
                Use the module eigengene to find a statistically significant difference between sample groups.
            </p>
            <select class="custom-select" v-model="trait">
                <option v-for="trait in nominalTraits" :key="trait" :value="trait">{{ trait }}</option>
            </select>
            <div class="mt-3">
                <button class="btn btn-light">
                    <span class="fa fa-check"></span>
                    Go
                </button>
                <button class="btn btn-light" disabled>
                    View previous result
                </button>
            </div>
        </div>

        <correlation-setup class="ml-1" style="flex: 1"></correlation-setup>
    </div>
</div>
</template>

<script>
import Genotype from 'components/Genotype'
import CorrelationSetup from 'components/SignificanceTesting/CorrelationSetup'
import { mapGetters } from 'vuex'

export default {
    data() {
        return {
            trait: null,
        }
    },

    props: ['project', 'shouldUpdate'],

    components: {
        Genotype,
        CorrelationSetup
    },
    
    methods: {
        genotypeDone() {
            this.$store.commit('editProject', {step: 5})
        }
    },

    computed: {
        ...mapGetters(['nominalTraits'])
    },

    created() {
        this.trait = this.nominalTraits[0]
    }
}
</script>

<style>
#significance-container {
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-gap: 20px;
}
</style>