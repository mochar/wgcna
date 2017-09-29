<template>
<div class="card card-block block">
    <h5 class="card-title">Module Browser</h5>
    <div class="row">
        <div class="col-4">
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
                        @click="pickModule(key)">
                        <td>{{ key }}</td>
                        <td>{{ module.members }}</td>
                        <td>{{ module.pvalue }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
        <div class="col-8">
            <ul v-if="displayedmodulemembers.length > 0">
                <button class="btn btn-primary" v-on:click="changepage(-1)"
			:disabled="displaypage < 2">
                    <span class="fa fa-chevron-left"></span>
                </button>
                {{ displaypage }} / {{ maxdisplaypage }}
                <button class="btn btn-primary" v-on:click="changepage(1)"
			:disabled="displaypage >= maxdisplaypage">
                    <span class="fa fa-chevron-right"></span>
                </button>
                <li v-for="member in displayedmodulemembers">
                    {{ member | truncate('85') }}
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
            pickedmodulemembers: "",
            displayedmodulemembers: "",
            displaypage: 1
        }
    },

    props: ['name'],

    methods: {
        getModuleNames() {
            $.getJSON(`${ROOTURL}/moduletree/${this.name}`).then(data => {
                this.moduleinfo = data
            })
        },
        getModuleMembers() {
            $.getJSON(`${ROOTURL}/moduletree/${this.name}/${this.pickedmodule}`).then(data => {
                this.pickedmodulemembers = data
            })

        },
        pickModule(module) {
            this.pickedmodule = module
        },
        changepage(change){
            if(this.displaypage + change > 0 && this.displaypage + change <= this.maxdisplaypage){
                this.displaypage += change
            }
        },
        updatepage(){
            if(this.displaypage == 0){
                this.displaypage = 1
            }
            var displayed = []
            for(var i=(this.displaypage-1)*20;i<this.displaypage*20;i++) {
                if(this.pickedmodulemembers[i]){
                    displayed.push(this.pickedmodulemembers[i])
                }
            }
            this.displayedmodulemembers = displayed
        }
    },

    watch: {
        name(){
            this.getModuleNames()
            this.pickedmodule = ""
        },
        pickedmodule() {
            this.pickedmodulemembers = ""
            if(this.pickedmodule){
                this.getModuleMembers()
            }
            this.displaypage = 1
        },
        displaypage() {
            this.updatepage()
        },
        pickedmodulemembers() {
            this.updatepage()
        }
    },

    computed: {
       maxdisplaypage: function () {
            return Math.ceil(this.pickedmodulemembers.length / 20)
        }
    },

    filters: {
        truncate: function(string, value) {
            var maxlength = 85
            if (string.length > value){
                return string.substring(0, value-2) + '...'
            } else {
                return string
            }
        }
    },
}
</script>

<style scoped>
    .table > tbody {
        cursor: pointer;
    }
</style>
