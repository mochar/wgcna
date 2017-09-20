<template>
<div class="card card-block block">
    <h5 class="card-title">Module Browser</h5>
    <div class="row">
        <div class="col">
            <table class="table table-hover table-sm">
                <thead>
                    <th>Module name</th>
                    <th>Members</th>
                    <th>Module p-value</th>
                </thead>
                <tbody>
                    <tr v-for="(module, key) in moduleinfo"
                        :style="{ 'font-weight': pickedmodule == key ? 'bold' : 'normal',
                                  'color': pickedmodule == key ? 'red' : 'black' }"
                        @click="pick(key)">
                        <td>{{ key }}</td>
                        <td>{{ module.members }}</td>
                        <td>{{ module.pvalue }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
        <div class="col">
            <ul>
                <li v-for="member in pickedmodulemembers">
                    {{ member }}
                </li>
            </ul>
        </div>
    </div>
</div>
</template>

<script>
export default {
    data() {
        return {
            moduleinfo: {},
            pickedmodule: "",
            pickedmodulemembers: null
        }
    },

    props: ['name'],

    methods: {
        buildTree() {
            $.getJSON(`${ROOTURL}/moduletree/${this.name}`).then(data => {
                this.moduleinfo = data
            })
        },
        getModuleMembers() {
            $.getJSON(`${ROOTURL}/moduletree/${this.name}/${this.pickedmodule}`).then(data => {
                this.pickedmodulemembers = data
            })
        },
        pick(module) {
            this.pickedmodule = module
            this.getModuleMembers()
        }
    },

    watch: {
        name() {
            this.buildTree()
            this.pickedmodule = ""
            this.pickedmodulemembers = null
        }
    },
}
</script>
