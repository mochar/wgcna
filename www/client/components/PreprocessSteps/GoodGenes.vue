<template>
<div>  
    <div class="preprocess-component">
        <span class="fa fa-refresh fa-spin" v-if="loading"></span>
        <div v-else>
            <span v-if="allOK">All OK</span>
            <div v-else>
                <list-popover name="bad samples" :list="badSamples"></list-popover>
                <list-popover name="bad genes" :list="badGenes"></list-popover>
            </div>
        </div>
    </div>
    <div class="mt-2">
        <button class="btn btn-light" :disabled="loading" @click="$emit('done')">
            <span class="fa fa-check"></span>
            OK
        </button>
    </div>
</div>
</template>

<script>
import ListPopover from 'components/ListPopover'

export default {
    data() {
        return {
            loading: true,
            showAllGenes: false,
            showAllSamples: false
        }
    },

    props: ['project'],

    components: {
        ListPopover
    },

    created() {
        $.get(`${ROOTURL}/projects/${this.project.id}/goodsamplesgenes`).then(data => {
            this.allOK = data.allOK
            this.badSamples = data.badSamples
            this.badGenes = data.badGenes
            this.loading = false
        })
    }
}
</script>
