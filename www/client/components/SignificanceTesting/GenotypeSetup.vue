<template>
<div class="card card-body block">
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
        <button class="btn btn-light" @click="go" :disabled="loading">
            <font-awesome-icon icon="check" v-if="!loading" />
            <font-awesome-icon icon="sync" spin v-else />
            Go
        </button>
        <button class="btn btn-light" disabled>
            View previous result
        </button>
    </div>
</div>
</template>

<script>
export default {
    data() {
        return {
            trait: null,
            loading: false
        }
    },
    
    props: ['nominalTraits', 'project'],

    methods: {
        go() {
            this.loading = true
            const data = JSON.stringify({ trait: this.trait })
            this.$helpers.post(data, this.project.id, 'genotype')
            .then(() => {
                this.loading = false
                this.$store.commit('editProject', {step: 5})
                this.$emit('go')
            }, () => {
                this.loading = false
            })
        }
    },

    created() {
        this.trait = this.nominalTraits[0]
    }
}
</script>
