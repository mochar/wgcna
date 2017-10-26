<template>
<div id="new">
    <div class="d-flex justify-content-between align-items-center top">
        <h3>WGCNA</h3>

        <h5 v-if="project">
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

        <router-link to="/" class="btn btn-secondary">
            Cancel
        </router-link>
    </div>

    <div id="upload-form" class="card" v-if="!project" style="margin-top: 1rem">
        <form enctype="multipart/form-data" @submit.prevent="loadExpression">
            <div class="row">
                <div class="col-2">
                    <input type="text" class="form-control" name="name" placeholder="Name">
                </div>
                <div class="col-6">
                    <input type="text" class="form-control" name="description" placeholder="Short description">
                </div>
                <div class="col-3 d-flex align-items-center">
                    <input type="file" name="expression" style="width: 100%">
                </div>
                <div class="col-1">
                    <button type="submit" class="btn btn-primary" :disabled="loading">Load</button>
                </div>
            </div>
        </form>
    </div>

    <component 
        v-else
        :is="current" 
        :project="project"
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
        loadExpression() {
            this.loading = true
            const formData = new FormData(event.srcElement)
            $.post({
                url: `${ROOTURL}/projects/`,
                data: formData,
                async: true,
                cache: false,
                contentType: false,
                processData: false
            }).then(data => {
                this.project = data.project
                this.loading = false
            }, () => {
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
#upload-form .row > div {
    padding-right: 0;
}
</style>