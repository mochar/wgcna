<template>
<page class="mb-5" :show="!loading" v-if="!loading && datas !== null">
    <no-modules v-if="!hasModules" />
    <div v-else>
        <div class="d-flex justify-content-between align-items-baseline mb-3">
            <div>
                <span class="align-baseline">
                    Showing {{ itemList.length }} of {{ datas.data.index.length }} modules
                </span>
                <button class="btn btn-light btn-sm pl-3 pr-3 ml-2">
                    <font-awesome-icon icon="compress" />
                    Merge modules
                </button>
                <button class="btn btn-light btn-sm pl-3 pr-3 ml-0">
                    <font-awesome-icon icon="download" />
                    Export modules
                </button>
            </div>
            <select class="custom-select col-4" v-model="trait">
                <option v-for="trait in nominalTraits" :key="trait" :value="trait">{{ trait }}</option>
            </select>
        </div>

        <dendro
            selector="modules-tree"
            :cluster-data="datas.tree" 
            :cuttable="false"
            :axis="false"
            :selectable="true"
            @selected="d => selected = d"
            :ratio="0.1">
        </dendro>

        <div class="row m-0 mt-1">
            <module 
                v-for="(module, i) in itemList" 
                :key="module" 
                :name="module"
                :data="datas.data.data[i]"
                :groups="traitData.data[traitData.index.indexOf(trait)]"
                :samples="datas.data.columns">
            </module>
        </div>
    </div>
</page>  
</template>

<script>
import Module from 'components/Module'
import Page from 'views/Page'
import NoModules from './NoModules'
import { mapActions, mapState, mapGetters } from 'vuex'
import Dendro from 'charts/Dendro'

export default {
    data() {
        return {
            trait: null,
            selected: null,
            shouldUpdate: false,
            datas: null,
            loading: true,
            active: false
        }
    },

    props: ['project'],

    components: {
        Module,
        Dendro,
        NoModules,
        Page
    },

    methods: {
        ...mapActions(['getTraitData']),
        setUp() {
            this.loading = true
            this.selected = null
            this.getTraitData().then(() => {
                this.trait = this.nominalTraits[0]
                $.getJSON(`${ROOTURL}/projects/${this.project.id}/eigengenes`).then(data => {
                    this.datas = data
                    this.loading = false
                })
            })
        }
    },

    computed: {
        ...mapState(['traitData']),
        ...mapGetters(['nominalTraits', 'hasModules']),
        itemList() {
            if (this.datas === null) return []
            if (this.selected === null) return this.datas.data.index
            return this.datas.data.index.filter((d, i) => this.selected.includes(i))
        }
    },

    watch: {
        project(val, oldVal) {
            this.loading = true
            // this.datas = null
            // this.trait = null
            // this.selected = null
            if (this.hasModules) this.shouldUpdate = true
        },
        hasModules() {
            this.loading = true
            // this.datas = null
            // this.trait = null
            // this.selected = null
            if (this.hasModules) this.shouldUpdate = true
        },
        loading() {
            console.log('Inspection loading ' + this.loading)
        },
        datas() {
            console.log('data? ', !this.datas === null)
        },
        traitData() {
            console.log('trait? ', !this.traitData === null)
        }
    },

    activated() {
        console.log('activated')
        if (this.shouldUpdate) {
            this.setUp()
            this.shouldUpdate = false
        }
    },

    deactivated() {
    },

    created() {
        if (this.hasModules) this.setUp()
    }
}
</script>
