<template>
<div>  
    <span class="fa fa-refresh fa-spin" v-if="loading"></span>
    <div v-else>
        <span v-if="allOK">All OK</span>
        <div v-else>
        </div>
    </div>
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

    props: ['projectId', 'go'],

    created() {
        $.get(`${ROOTURL}/projects/${this.projectId}/goodsamplesgenes`).then(data => {
            this.allOK = data.allOK
            this.badSamples = data.badSamples
            this.badGenes = data.badGenes
            this.loading = false
            this.$emit('loaded')
        })
    },

    watch: {
        go() {
            if (this.go) this.$emit('done')
        }
    }
}
</script>
