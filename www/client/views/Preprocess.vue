<template>
<div>
    <div class="d-flex justify-content-between align-items-center top">
        <h3>WGCNA</h3>

        <h5>
            <span :class="current === 'Reformat' ? 'text-primary' : 'text-muted'">
                1. Define data
            </span>
            <span> | </span>
            <span :class="current === 'GoodGenes' ? 'text-primary' : 'text-muted'">
                2. Good samples &amp; genes 
            </span>
            <span> | </span>
            <span :class="current === 'Outliers' ? 'text-primary' : 'text-muted'">
                3. Remove outliers
            </span>
        </h5>

        <router-link to="/" class="btn btn-secondary">
            Cancel
        </router-link>
    </div>

    <component 
        v-if="this.$route.params.id"
        :is="current" 
        :projectId="this.$route.params.id"
        @done="next" 
        style="margin-top: 1rem">
    </component>
</div>
</template>

<script>
import Reformat from 'components/Reformat'
import GoodGenes from 'components/GoodGenes'
import Outliers from 'components/Outliers'

export default {
    data() {
        return {
            current: 'Reformat',
            project: null,
            loading: false
        }
    },

    components: {
        Reformat,
        GoodGenes,
        Outliers
    },

    methods: {
        next() {
            switch(this.current) {
                case 'Reformat':
                    this.current = 'GoodGenes'
                    break;
                case 'GoodGenes':
                    this.current = 'Outliers'
                    break;
                case 'Outliers':
                    this.$router.push('/')
            }
        }
    },

    watch: {
        '$route'(to, from) {
            console.log(to)
            console.log(from)
            console.log(this.$route.params)
        }
    },

    created() {
    }
}
</script>

<style>
</style>