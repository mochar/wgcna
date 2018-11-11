<template>
<div class="mb-5">
    <no-modules v-if="!hasModules" />
    <div v-else>
    <div class="mb-2 d-flex">
        <select class="custom-select mr-1" v-model="trait">
            <option v-for="trait in nominalTraits" :key="trait" :value="trait">{{ trait }}</option>
        </select>
    </div>
    <div class="row" v-if="traitData && data && trait">
        <dendro
            selector="modules-tree"
            :cluster-data="tree" 
            :cuttable="false"
            :axis="false"
            :selectable="true"
            @selected="d => selected = d"
            :ratio="0.1">
        </dendro>
        <module 
            v-for="(module, i) in itemList" 
            :key="module" 
            :name="module"
            :data="data.data[i]"
            :groups="traitData.data[traitData.index.indexOf(trait)]"
            :samples="data.columns">
        </module>
    </div>
    </div>
</div>  
</template>

<script>
import Module from 'components/Module'
import NoModules from './NoModules'
import { mapActions, mapState, mapGetters } from 'vuex'
import Dendro from 'charts/Dendro'

export default {
    data() {
        return {
            data: null,
            trait: null,
            selected: null,
            shouldUpdate: true
        }
    },

    props: ['project'],

    components: {
        Module,
        Dendro,
        NoModules
    },

    methods: {
        ...mapActions(['getTraitData']),
        setUp() {
            this.selected = null
            this.getTraitData().then(() => {
                this.trait = this.nominalTraits[0]
                $.getJSON(`${ROOTURL}/projects/${this.project.id}/eigengenes`).then(data => {
                    data.index = data.data.index.map(x => x.replace(/^ME/g, ''))
                    this.data = data.data
                    this.tree = data.tree
                })
            })
        }
    },

    computed: {
        ...mapState(['traitData']),
        ...mapGetters(['nominalTraits', 'hasModules']),
        itemList() {
            if (this.data === null) return []
            if (this.selected == null) return this.data.index
            return this.data.index.filter((d, i) => this.selected.includes(i))
        }
    },

    watch: {
        project(val, oldVal) {
            this.data = null
            this.trait = null
            if (this.hasModules) this.shouldUpdate = true
        },
        hasModules() {
            this.data = null
            this.trait = null
            if (this.hasModules) this.shouldUpdate = true
        }
    },

    activated() {
        if (this.shouldUpdate) {
            this.setUp()
            this.shouldUpdate = false
        }
    },

    created() {
        if (this.hasModules) this.setUp()
    }
}
</script>
