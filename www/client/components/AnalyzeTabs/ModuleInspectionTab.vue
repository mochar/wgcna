<template>
<div>
    <select class="custom-select" v-model="trait">
        <option v-for="trait in nominalTraits" :key="trait" :value="trait">{{ trait }}</option>
    </select>
    <div v-if="traitData && data && trait">
        <module 
            v-for="(module, i) in data.index" 
            :key="module" 
            :name="module"
            :data="data.data[i]"
            :groups="traitData.data[nominalTraits.indexOf(trait)]"
            :samples="data.columns">
        </module>
    </div>
</div>  
</template>

<script>
import Module from 'components/Module'
import { mapActions, mapState, mapGetters } from 'vuex'

export default {
    data() {
        return {
            data: null,
            trait: null
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
    },

    watch: {
        project() {
            if (this.shouldUpdate) {
                this.data = null
                this.trait = null
                this.setUp()
            }
        }
    },

    created() {
        this.setUp()
    }
}
</script>
