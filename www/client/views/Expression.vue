<template>
<div>
    <div style="display: inline">
        <h3 style="display: inline-block">
            <span :class="current === 'Reformat' ? 'text-primary' : 'text-muted'">
                1. Edit expression matrix
            </span>
            <span> | </span>
            <span :class="current === 'GoodGenes' ? 'text-primary' : 'text-muted'">
                2. Good samples &amp; genes 
            </span>
            <span> | </span>
            <span :class="current === 'Outliers' ? 'text-primary' : 'text-muted'">
                3. Remove outliers
            </span>
        </h3>

        <router-link to="/" class="float-xs-right" style="display: inline-block">
            Cancel
        </router-link>
    </div>
    <component 
        :is="current" 
        :name="$route.params.name" 
        @done="next" 
        style="margin-top: 1rem">
    </component>
</div>
</template>

<script>
import Reformat from '../components/Reformat'
import GoodGenes from '../components/GoodGenes'
import Outliers from '../components/Outliers'

export default {
    data() {
        return {
            current: 'Reformat'
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
    }
}
</script>