<template>
<div class="mb-5">
    <div class="mb-2 d-flex">
        <select class="custom-select mr-1" v-model="trait">
            <option v-for="trait in nominalTraits" :key="trait" :value="trait">{{ trait }}</option>
        </select>
    </div>
    <div class="row" v-if="traitData && data && trait">
        <dendro
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
</template>

<script>
import Module from 'components/Module'
import { mapActions, mapState, mapGetters } from 'vuex'
import Dendro from 'charts/Dendro'

export default {
    data() {
        return {
            data: null,
            trait: null,
            selected: null
        }
    },

    props: ['project', 'shouldUpdate'],

    components: {
        Module,
        Dendro
    },

    methods: {
        ...mapActions(['getTraitData']),
        setUp() {
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
        ...mapGetters(['nominalTraits']),
        itemList() {
            if (this.data === null) return []
            if (this.selected == null) return this.data.index
            return this.data.index.filter((d, i) => this.selected.includes(i))
        }
    },

    watch: {
        project() {
            if (this.shouldUpdate) {
                this.data = null
                this.trait = null
                this.setUp()
            }
        },
        searchTerm() {
            this.page = 1
        }
    },

    created() {
        this.setUp()
    }
}
</script>
