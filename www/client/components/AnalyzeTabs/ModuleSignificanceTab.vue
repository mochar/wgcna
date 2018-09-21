<template>
<div>
    <genotype
        :project="project" 
        :update="shouldUpdate || project.step == 4"
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
</template>

<script>
import Genotype from 'components/Genotype'
import CorrelationSetup from 'components/SignificanceTesting/CorrelationSetup'
import GenotypeSetup from 'components/SignificanceTesting/GenotypeSetup'
import CorrelationView from 'components/SignificanceTesting/CorrelationView'
import { mapGetters } from 'vuex'

export default {
    data() {
        return {
            showCorrs: false,
            showSig: false
        }
    },

    props: ['project', 'shouldUpdate'],

    components: {
        Genotype,
        CorrelationSetup,
        CorrelationView,
        GenotypeSetup
    },
    
    computed: {
        ...mapGetters(['nominalTraits'])
    },

    watch: {
        project() {
            if (this.shouldUpdate) {
                this.showCorrs = false
                this.showSig = false
            }
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