<template>
    <div class="row">
        <div class="col-6">
            <SemanticProjectSelect title="omic 1" v-on:projectId="projectId1 = $event" v-on:id_type="id_type1 = $event"></SemanticProjectSelect>
        </div>
        <div class="col-6">
                        <SemanticProjectSelect title="omic 2" v-on:projectId="projectId2 = $event" v-on:id_type="id_type2 = $event"></SemanticProjectSelect>
        </div>
        <div class="card card-body block">
            <h6 class="block-title">
                Semantic integration
            </h6>
            Annotation source:
            <select class="custom-select" v-model="annotation_type">
                <option v-for="annotation_type in annotation_types" :key="annotation_type" :value="annotation_type">{{ annotation_type }}</option>
            </select>
            <button class="btn btn-light" :disabled="loading" v-on:click="integrate"><span class="fa fa-check"> </span>Integrate</button>
        </div>
    </div>
</template>

<script>
import SemanticProjectSelect from 'components/SemanticProjectSelect'

export default {
    data() {
        return {
            annotation_types: ['Pathway', 'Molecular Function'],
            annotation_type: "",
            loading: false,
            projectId1: null,
            projectId2: null,
            id_type1: null,
            id_type2: null,
            results: null
        }
    },

    components: {
        SemanticProjectSelect
    },

    methods: {
        integrate() {
            console.log(this.projectId1)
            console.log(this.projectId2)
            console.log(this.id_type1)
            console.log(this.id_type2)
            console.log(this.annotation_type)

            this.loading = true
            this.results = null
            $.getJSON(`${ROOTURL}/integrate`,{"projectId1": this.projectId1,
                "projectId2": this.projectId2, "id_type1": this.id_type1,
                "id_type2": this.id_type2,
                "annotation_type": this.annotation_type}).then(data => {
                this.results = data
                this.loading = false
            })
        }
    },

    created() {
        this.annotation_type = this.annotation_types[0]
    }
}
</script>
