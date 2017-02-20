<template>
<div>
    <h3>Data</h3>
    <div class="row">
        <div class="col-xs-3">
            <div class="card card-block">
                <h5 class="card-title">Expression</h5>
                <form enctype="multipart/form-data" @submit.prevent="loadExpression">
                    <div class="form-group">
                        <input class="form-control" name="name" placeholder="Name">
                    </div>
                    <div class="form-group">
                        <input type="file" name="expression" style="width: 100%">
                    </div>
                    <button type="submit" class="btn btn-link float-xs-right">Load</button>
                </form>
            </div>
        </div>
    </div>

    <div v-show="name">
        <h3 style="margin-top: 1rem; display: inline-block">WGCNA</h3>

        <div class="btn-group float-xs-right">
            <button class="btn btn-primary">
                Generate report
            </button>
            <select v-model="name" id="name-select" class="custom-select btn btn-secondary">
                <option v-for="name in names">{{ name }}</option>
            </select>
        </div>

        <div class="row" v-if="false">
            <div class="col-xs-3">
                <div class="card card-block">
                    <h5 class="card-title">3. Module-genotype significance</h5>
                    <router-link 
                        tag="button" 
                        class="btn btn-link float-xs-right"
                        :to="{ path: `genotype/${name}` , params: { name: name } }"
                        :disabled="!name">Check
                    </router-link>
                </div>
            </div>

            <div class="col-xs-3">
                <div class="card card-block">
                    <h5 class="card-title">4. Module-trait associations</h5>
                    <router-link 
                        tag="button" 
                        class="btn btn-link float-xs-right"
                        :to="{ path: 'treshold' }"
                        :disabled="!name">Check
                    </router-link>
                </div>
            </div>
        </div>

        <treshold 
            :name="name" 
            :selected="power" 
            v-if="step > 0" 
            @done="x => { power = x; step = 2 }">
        </treshold>
        <cluster 
            :name="name" 
            :power="power"
            :step="step"
            v-if="step > 1"
            @cutting="step = 3"
            @done="step = 4">
        </cluster>
        <genotype
            :name="name" 
            :step="step"
            @done="step = 5"
            v-if="step > 3">
        </genotype>
<!--         <annotation
            v-if="step > 4">
        </annotation>
 -->    </div>
</div>
</template>

<script>
import Treshold from '../components/Treshold'
import Cluster from '../components/Cluster'
import Genotype from '../components/Genotype'
import Annotation from '../components/Annotation'

export default {
    data() {
        return {
            name: null,
            names: [],
            power: null,
            step: 0
        }
    },

    components: {
        Treshold,
        Cluster,
        Genotype,
        Annotation
    },

    methods: {
        loadExpression(event) {
            const formData = new FormData(event.srcElement)
            $.post({
                url: `${ROOTURL}/expression/`,
                data: formData,
                async: true,
                cache: false,
                contentType: false,
                processData: false
            }).then(data => {
                this.names.push(data.name)
                const to = { path: `/expression/${data.name}`, params: { name: data.name } }
                this.$router.push(to)
            })
        },
        loadTraits(event) {
            const formData = new FormData(event.srcElement)
            $.post({
                url: `${ROOTURL}/traits`,
                data: formData,
                async: true,
                cache: false,
                contentType: false,
                processData: false
            }).then(() => this.$router.push({ path: 'traits' }) )
        }
    },

    watch: {
        name() {
            this.step = 0
            $.getJSON(`${ROOTURL}/info/${this.name}`).then(data => {
                this.power = data.power
                this.step = data.step
            })
        }
    },

    created() {
        $.getJSON(`${ROOTURL}/expression/`).then(data => {
            this.names = data.names.sort((a, b) => a < b ? -1 : 1)
            if (this.names.length > 0) this.name = this.names[0]
        })
    }
}
</script>

<style>
#name-select:active:hover {
    background-color: white;
}
</style>