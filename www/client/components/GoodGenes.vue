<template>
<div>
    <div v-if="!loading">
        <h5>All OK</h5>
        <span>{{ allOK }}</span>

        <h5 style="margin-top: 2rem">Bad samples</h5>
        <div class="row" v-if="badSamples.length">
            <span v-for="sample in badSamples" :key="sample" style="display: list-item" class="col-2">
                {{ sample }}
            </span>
        </div>
        <span class="text-muted" v-else>None</span>

        <h5 style="margin-top: 2rem">Bad genes</h5>
        <div class="row" v-if="badGenes.length">
            <span v-for="gene in badGenes" :key="gene" style="display: list-item" class="col-2">
                {{ gene }}
            </span>
        </div>
        <span class="text-muted" v-else>None</span>

        <button class="btn btn-primary" id="done" @click="done">Done</button>
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
            loading: true
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
    }
}
</script>

<style scoped>
#done {
    display: block;
    margin-top: 1rem;
}
</style>