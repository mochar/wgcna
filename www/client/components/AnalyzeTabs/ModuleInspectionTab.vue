<template>
<div class="mb-5">
    <div class="mb-2 d-flex">
        <select class="custom-select mr-1" v-model="trait">
            <option v-for="trait in nominalTraits" :key="trait" :value="trait">{{ trait }}</option>
        </select>
        <input type="text" placeholder="Search module" class="bg-light p-1 ml-2 mr-2" v-model="searchTerm" />
        <button class="btn btn-light" @click="prevPage" :disabled="!canPrev">
            <font-awesome-icon icon="chevron-left" fixed-width />
        </button>
        <div class="pl-1"></div>
        <button class="btn btn-light" @click="nextPage" :disabled="!canNext">
            <font-awesome-icon icon="chevron-right" fixed-width />
        </button>
    </div>
    <div v-if="traitData && data && trait">
        <module 
            v-for="(module, i) in pageList" 
            :key="module" 
            :name="module"
            :data="data.data[pageItemIndices[i]]"
            :groups="traitData.data[traitData.index.indexOf(trait)]"
            :samples="data.columns">
        </module>
    </div>
    <div class="d-flex flex-row-reverse">
        <button class="btn btn-light" @click="nextPage" :disabled="!canNext">
            <font-awesome-icon icon="chevron-right" fixed-width />
        </button>
        <div class="pl-1"></div>
        <button class="btn btn-light" @click="prevPage" :disabled="!canPrev">
            <font-awesome-icon icon="chevron-left" fixed-width />
        </button>
    </div>
</div>  
</template>

<script>
import Module from 'components/Module'
import { PaginatedListMixin } from 'mixins'
import { mapActions, mapState, mapGetters } from 'vuex'

export default {
    mixins: [PaginatedListMixin],

    data() {
        return {
            data: null,
            trait: null,
            items: 5,
            searchTerm: ''
        }
    },

    props: ['project', 'shouldUpdate'],

    components: {
        Module
    },

    methods: {
        ...mapActions(['getTraitData']),
        setUp() {
            this.getTraitData().then(() => {
                this.trait = this.nominalTraits[0]
                $.getJSON(`${ROOTURL}/projects/${this.project.id}/eigengenes`).then(data => {
                    data.index = data.index.map(x => x.replace(/^ME/g, ''))
                    this.data = data
                })
            })
        }
    },

    computed: {
        ...mapState(['traitData']),
        ...mapGetters(['nominalTraits']),
        itemList() {
            if (this.data === null) return []
            if (this.searchTerm === '') return this.data.index
            return this.data.index.filter(item => item.search(this.searchTerm) > -1)
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
