<template>
<div class="card card-block block">
    <div class="row">
        <h5 class="card-title">Module Browser</h5>
    </div>
</div>
</template>

<script>
export default {
    data() {
        return {
        }
    },

    props: ['name'],

    methods: {
        buildTree() {
            $.getJSON(`${ROOTURL}/moduletree/${this.name}`).then(data => {
                console.log(data)
            })
        },
    },

    watch: {
        name() {
            this.buildTree()
        }
    },

    created() {
        this.buildTree()
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
