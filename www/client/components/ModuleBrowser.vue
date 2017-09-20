<template>
<div class="card card-block block">
        <h5 class="card-title">Module Browser</h5>

        <table class="table table-hover table-sm">
            <thead>
                <th>Module name</th>
                <th>Members</th>
                <th>Module p-value</th>
            </thead>
            <tbody>
                <tr v-for="(module, key) in moduleinfo">
                    <td>{{ key }}</td>
                    <td>{{ module.members }}</td>
                    <td>{{ module.pvalue }}</td>
                </tr>
            </tbody>
        </table>
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
