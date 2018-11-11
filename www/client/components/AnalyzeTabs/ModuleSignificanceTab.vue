<template>
<div>
    <no-modules v-if="!hasModules" />
    <div v-else>
    <genotype
        :project="project" 
        @back="showSig = false"
        v-if="showSig">
    </genotype>
    
    <correlation-view 
        :project="project" 
        @back="showCorrs = false"
        v-if="showCorrs">
    </correlation-view>

    <div id="significance-container" class="d-flex align-items-start" v-if="!showCorrs && !showSig">
        <genotype-setup
            :project="project" 
            :nominal-traits="nominalTraits"
            @go="showSig = true"
            class="mr-1"
            style="flex: 1">
        </genotype-setup>

        <correlation-setup 
            :project="project" 
            @go="showCorrs = true"
            class="ml-1" 
            style="flex: 1">
        </correlation-setup>
    </div>
    </div>
</div>
</template>

<script>
import Genotype from 'components/Genotype'
import CorrelationSetup from 'components/SignificanceTesting/CorrelationSetup'
import GenotypeSetup from 'components/SignificanceTesting/GenotypeSetup'
import CorrelationView from 'components/SignificanceTesting/CorrelationView'
import NoModules from './NoModules'
import { mapGetters } from 'vuex'

export default {
    data() {
        return {
            showCorrs: false,
            showSig: false
        }
    },

    props: ['project'],

    components: {
        Genotype,
        CorrelationSetup,
        CorrelationView,
        GenotypeSetup,
        NoModules
    },
    
    computed: {
        ...mapGetters(['nominalTraits', 'hasModules'])
    },

    watch: {
        project(val, oldVal) {
            this.showCorrs = false
            this.showSig = false
        },
        hasModules() {
            this.showCorrs = false
            this.showSig = false
        }
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