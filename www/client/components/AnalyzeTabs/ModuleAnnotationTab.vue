<template>
    <div>
        <div class="card card-body block">
            <h6 class="block-title">
                Annotation
            </h6>
            Id type:
            <select class="custom-select" v-model="id_type" :disabled="loading">
                <option v-for="id_type in id_types" :key="id_type" :value="id_type">{{ id_type }}</option>
            </select>
            Annotation source:
            <select class="custom-select" v-model="annotation_type" :disabled="loading">
                <option v-for="annotation_type in annotation_types" :key="annotation_type" :value="annotation_type">{{ annotation_type }}</option>
            </select>
            <button class="btn btn-light" :disabled="loading" v-on:click="annotate(true)"><span class="fa fa-check"> </span>Annotate</button>
        </div>

        <h6><span class="fa fa-cog fa-spin" v-if="loading"></span></h6>

        <div v-if=true>
            {{ status }}
        </div>

        <div class="card card-body block" v-for="(module_annotations, module_name) in annotations">
            <div>
                <h6 class="block-title">
                    {{ module_name }}
                </h6>
            </div>
            <table style="width:100%" border="0px">
                <tr>
                    <th>Name</th>
                    <th>Connected</th>
                    <th>P-Value</th>
                </tr>
                <tr v-for="module_annotation in module_annotations">
                    <td>{{ module_annotation[0] }}</td>
                    <td>{{ module_annotation[1] }}</td>
                    <td>{{ module_annotation[2] }}</td>
                </tr>
            </table>
        </div>

    </div>
</template>

<script>

export default {
    data() {
        return {
            loading: true,
            id_types: ["Entrez", "ENSG", "ChEBI", "Euretos synonym"],
            id_type: "",
            annotation_types: ['Pathway', 'Molecular Function'],
            annotation_type: "",
            annotations: {},
            status: null
        }
    },

    props: ['project', 'shouldUpdate'],

    watch: {
        project: function() {
            this.annotate(false)
        }
    },

    methods: {
        annotate(recalculate) {
            this.status = null
            this.loading = true
            this.annotations = {}
            var ref = this

            $.getJSON(`${ROOTURL}/projects/${this.project.id}/annotate`,{"id_type" :  this.id_type, "annotation_type" : this.annotation_type, "recalculate" : recalculate})
            .then(data => {
                this.annotations = data
                this.loading = false
            })
            .fail(function(request, status, error) {
                ref.loading = false
                ref.status = status
            })
        }
    },

    created() {
        this.id_type = this.id_types[0]
        this.annotation_type = this.annotation_types[0]
        this.annotate(false)
    }
}
</script>
