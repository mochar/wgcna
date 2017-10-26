<template>
<div class="card card-block block">
    <div class="row">
        <h5 class="card-title">2. Cluster genes</h5>

        <span class="fa fa-cog fa-spin fa-2x" v-if="loading"></span>

        <div v-else>
            <div class="float-right">
                <form class="form-inline" enctype="multipart/form-data" @submit.prevent="cut">
                    <div class="form-group">
                        <label>Minimum module size</label>
                        <input type="number" class="form-control" name="minModuleSize">
                    </div>
                    <div class="form-group">
                        <label>Deep split</label>
                        <input type="number" class="form-control" name="deepSplit" min="0" max="5" value="2">
                    </div>
                  <button type="submit" class="btn btn-primary" :disabled="cutting">Cut</button>
                </form>
            </div>

            <img v-if="imgSrc" :src="imgSrc" :class="{ 'cutting': cutting }" />
        </div>
    </div>
</div>
</template>

<script>
export default {
    data() {
        return {
            loading: true,
            imgSrc: null,
            cutting: false
        }
    },

    props: ['project'],

    methods: {
        cluster() {
            this.loading = true
            // const endpoint = this.step < 4 ? 'clustergenes' : 'cutgenes'
            // $.get(`${ROOTURL}/${endpoint}/${this.name}`).then(data => {
            //     this.imgSrc = `data:image/png;base64,${data.base64}`
            //     this.loading = false
            // })
        },
        cut(event) {
            this.cutting = true
            this.$emit('cutting')
            const formData = new FormData(event.srcElement)
            $.post({
                url: `${ROOTURL}/cutgenes/${this.name}`,
                data: formData,
                async: true,
                cache: false,
                contentType: false,
                processData: false
            }).then(data => {
                this.imgSrc = `data:image/png;base64,${data.base64}`
                this.cutting = false
                this.$emit('done')
            })
        }
    },

    watch: {
        power() {
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