<template>
<div class="card card-block block">
    <h6 class="block-title">
        GENE CLUSTERING
        <span class="fa fa-cog fa-spin" v-if="loading"></span>
    </h6>

    <div style="position: absolute; right: 1rem" class="">
        <form class="form-inline" enctype="multipart/form-data" @submit.prevent="cut">
            <div class="form-group">
                <label>Minimum module size</label>
                <input type="number" class="form-control" name="minModuleSize">
            </div>
            <div class="form-group" style="display: none">
                <label>Deep split</label>
                <input type="number" class="form-control" name="deepSplit" min="0" max="5" value="2">
            </div>
            <button type="submit" class="btn btn-primary" :disabled="cutting">Cut</button>
        </form>
    </div>

    <dendrogram :cluster-data="clusterData" :ratio="0.4" :colors="colors" v-if="!loading"></dendrogram>
</div>
</template>

<script>
import Dendrogram from 'charts/Dendrogram'

export default {
    data() {
        return {
            loading: true,
            cutting: false,
            clusterData: null,
            colors: null
        }
    },

    components: {
        Dendrogram
    },

    props: ['project'],

    methods: {
        cluster() {
            this.loading = true
            this.clusterData = null
            this.colors = null
            $.get(`${ROOTURL}/projects/${this.project.id}/clustergenes`).then(data => {
                this.clusterData = data
                this.loading = false
            })
        },
        cut(event) {
            this.cutting = true
            this.$emit('cutting')
            const formData = new FormData(event.srcElement)
            $.post({
                url: `${ROOTURL}/projects/${this.project.id}/clustergenes`,
                data: formData,
                async: true,
                cache: false,
                contentType: false,
                processData: false
            }).then(data => {
                console.log(data)
                this.colors = data
                this.cutting = false
                this.$emit('done')
            }, () => {
                this.cutting = false
            })
        }
    },

    watch: {
        project() {
            this.cluster()
        }
    },

    created() {
        this.cluster()
    }
}
</script>

<style scoped>
img {
    width: 100%;
}

img.cutting {
    opacity: .5;
}
</style>