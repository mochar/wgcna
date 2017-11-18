<template>
<div class="card card-body">
    <h6 class="block-title text-uppercase">
        Good Samples &amp; Genes 
    </h6>

    <div v-if="!loading">
        <h5>All OK</h5>
        <span>{{ allOK }}</span>

        <h5 style="margin-top: 2rem">Bad samples</h5>
        <div v-if="badSamples.length">
            <div class="row p-3">
                <div v-for="i in rangeSamples" :key="badSamples[i]" class="col-2">
                    <span style="display: list-item">{{ badSamples[i] }}</span>
                </div>
            </div>
            <button class="btn btn-link" @click="showAllSamples = !showAllSamples">
                <span v-if="showAllSamples">Show less</span>
                <span v-else>Show all ({{ badSamples.length }} total)</span>
            </button>
        </div>
        <span class="text-muted" v-else>None</span>

        <h5 style="margin-top: 2rem">Bad genes</h5>
        <div v-if="badGenes.length">
            <div class="row p-3">
                <div class="col-2" v-for="i in rangeGenes" :key="badGenes[i]">
                    <span style="display: list-item">{{ badGenes[i] }}</span>
                </div>
            </div>
            <button class="btn btn-link" @click="showAllGenes = !showAllGenes">
                <span v-if="showAllGenes">Show less</span>
                <span v-else>Show all ({{ badGenes.length }} total)</span>
            </button>
        </div>
        <span class="text-muted" v-else>None</span>

        <div class="block-action-div">
            <button class="btn btn-primary" @click="done">
                <span class="fa fa-check"></span>
                Done
            </button>
        </div>
    </div>

    <span class="fa fa-cog fa-spin fa-2x fa-fw" v-else></span>
</div>
</template>

<script>
export default {
    data() {
        return {
            allOK: null,
            badSamples: null,
            badGenes: null,
            loading: true,
            showAllGenes: false,
            showAllSamples: false
        }
    },

    props: ['projectId'],

    created() {
        $.get(`${ROOTURL}/projects/${this.projectId}/goodsamplesgenes`).then(data => {
            this.allOK = data.allOK
            this.badSamples = data.badSamples
            this.badGenes = data.badGenes
            this.loading = false
        })
    },

    methods: {
        done() {
            this.$emit('done')
        }
    },

    computed: {
        rangeGenes() {
            if (!this.badGenes) return null
            const end = this.showAllGenes ? this.badGenes.length : 30
            return this.$helpers.range(end)
        },
        rangeSamples() {
            if (!this.badSamples) return null
            const end = this.showAllSamples ? this.badSamples.length : 30
            return this.$helpers.range(end)
        }
    }
}
</script>