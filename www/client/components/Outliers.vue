<template>
<div>
    <div v-if="!loading">
        <input placeholder="cut height" v-model="cutHeight" />
        <button class="btn btn-secondary" :disabled="!cutHeight || cutting" @click="cut">
            <span class="fa fa-cog fa-spin fa-fw" v-if="cutting"></span>
            Cut
        </button>
        <img v-if="imgSrc" :src="imgSrc" :class="{ 'cutting': cutting }" />

        <button class="btn btn-primary" id="done" @click="done">Done</button>
    </div>

    <span class="fa fa-cog fa-spin fa-2x fa-fw" v-else></span>
</div>
</template>

<script>
export default {
    data() {
        return {
            imgSrc: null,
            cutHeight: null,
            loading: true,
            cutting: false
        }
    },

    props: ['name'],

    methods: {
        cut() {
            this.cutting = true
            return $.get(`${ROOTURL}/cluster/${this.name}/${this.cutHeight}`).then(data => {
                this.imgSrc = `data:image/png;base64,${data.base64}`
                this.cutting = false
            })
        },
        done() {
            if (this.cutHeight) {
                $.get(`${ROOTURL}/cut/${this.name}/${this.cutHeight}`).then(() => { 
                    this.$emit('done')
                })
            } else {
                this.$emit('done')
            }
        }
    },

    created() {
        this.cut().then(() => this.loading = false)
    }
}
</script>

<style scoped>
img.cutting {
    opacity: .5;
}

#done {
    display: block;
    margin-top: 1rem;
}
</style>