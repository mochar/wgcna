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
            <option value="spearman">Spearman</option>
            <option value="pearson">Pearson</option>
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
        <button class="btn btn-light" @click="go" :disabled="loading">
            <font-awesome-icon icon="sync" spin fixed-width v-if="loading" />
            <font-awesome-icon icon="check" fixed-width v-else />
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
            method: 'spearman',
            ordinals: {},
            loading: false
        }
    },

    props: ['project'],

    components: {
        OrdinalTrait
    },

    methods: {
        ...mapActions(['getTraitData']),
        go() {
            this.loading = true
            const data = JSON.stringify(this.ordinals)
            this.$helpers.post(data, this.project.id, 'correlate')
            .then(() => {
                this.loading = false
                this.$emit('go')
            }, () => {
                this.loading = false
            })
        }
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
