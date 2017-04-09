<template>
<div id="new">
    <div class="d-flex justify-content-between align-items-center top">
        <h3>WGCNA</h3>

        <h5 v-if="name">
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
        </h5>

        <div id="upload-form" class="card" v-else>
            <form class="d-flex align-items-center" enctype="multipart/form-data" @submit.prevent="loadExpression">
                <input type="text" class="form-control" name="name" placeholder="Name">
                <input type="file" name="expression" style="width: 100%">
                <button type="submit" class="btn btn-primary" :disabled="loading">Load</button>
            </form>
        </div>

        <router-link to="/" class="btn btn-secondary">
            Cancel
        </router-link>
    </div>

    <component 
        v-if="name"
        :is="current" 
        :name="name"
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
            current: 'Reformat',
            name: null,
            loading: false
        }
    },

    components: {
        Reformat,
        GoodGenes,
        Outliers
    },

    methods: {
        loadExpression() {
            this.loading = true
            const formData = new FormData(event.srcElement)
            $.post({
                url: `${ROOTURL}/expression/`,
                data: formData,
                async: true,
                cache: false,
                contentType: false,
                processData: false
            }).then(data => {
                this.name = data.name
                this.loading = false
            })
        },
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

<style>
#new {
    
}

#upload-form {
    padding: .15rem;
}

#upload-form input[type="file"] {
    margin: 0 .25rem;
}
</style>