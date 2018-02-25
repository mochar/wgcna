<template>
<div class="card card-body block">
    <div class="d-flex justify-content-between align-items-start">
        <h6 class="block-title text-uppercase">
            Correlation with traits
        </h6>
    </div>
    <p class="card-text">
        Correlate the module eigengene to sample traits.
        The option is given between Pearson or Spearman correlation coefficients. 
        When ordinal traits are present, it is appropriate to make use of Spearman.
    </p>
    <div>
        <select class="custom-select" v-model="method">
            <option value="pearson">Pearson</option>
            <option value="spearman">Spearman</option>
            <option value="mixed">Mixed</option>
        </select>
    </div>
    <div class="mt-3" v-if="method !== 'pearson'">
        <p>
            Specify ordinal traits and the order of their variables.
        </p>
        <div v-if="traitData">
            <ordinal-trait 
                v-for="trait in nominalTraits" 
                :key="trait" 
                :trait="trait" 
                :variables="$helpers.unique(traitData.data[traitData.index.indexOf(trait)])"
                @nominal="$delete(ordinals, trait)"
                @ordinal="variables => $set(ordinals, trait, variables)">
            </ordinal-trait>
        </div>
    </div>
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
</template>

<script>
import OrdinalTrait from 'components/SignificanceTesting/OrdinalTrait'
import { mapActions, mapState, mapGetters } from 'vuex'

export default {
    data() {
        return {
            method: 'pearson',
            ordinals: {}
        }
    },

    components: {
        OrdinalTrait
    },

    methods: {
        ...mapActions(['getTraitData'])
    },

    computed: {
        ...mapState(['traitData']),
        ...mapGetters(['nominalTraits']),
    },

    created() {
        this.getTraitData().then(() => {
        })
    }
}
</script>
