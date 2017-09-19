<template>
<div class="card card-block block">
    <div class="row">
        <h5 class="card-title">Module Browser</h5>
        <ul>
            <li v-for="(module, key) in moduleinfo">
                {{ key }} - {{module.members}} - {{ module.pvalue}}
            </li>
        </ul>
    </div>
</div>
</template>

<script>
export default {
    data() {
        return {
            moduleinfo: {},
        }
    },

    props: ['name'],

    methods: {
        buildTree() {
            $.getJSON(`${ROOTURL}/moduletree/${this.name}`).then(data => {
                this.moduleinfo = data
            })
        },
    },

    watch: {
        name() {
            this.buildTree()
        }
    },
}
</script>
