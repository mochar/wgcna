<template>
    <div class="row">
        <div class="col-6">
            <SemanticProjectSelect title="omic 1" :loading="loading" v-on:projectId="projectId1 = $event" v-on:id_type="id_type1 = $event"></SemanticProjectSelect>
        </div>
        <div class="col-6">
            <SemanticProjectSelect title="omic 2" :loading="loading" v-on:projectId="projectId2 = $event" v-on:id_type="id_type2 = $event"></SemanticProjectSelect>
        </div>
        <div class="col-12">
            <div class="card card-body block">
                <h6 class="block-title">
                    Semantic integration
                </h6>
                Annotation source:
                <select class="custom-select" v-model="annotation_type" :disabled="loading">
                    <option v-for="annotation_type in annotation_types" :key="annotation_type" :value="annotation_type">{{ annotation_type }}</option>
                </select>
                Minimum number of concepts connected to set:
                <input v-model.number="min_connected" type="number" :disabled=true>
                P-Value threshold for sets:
                <input v-model.number="pvalue_treshold" type="number" :disabled=true>
                <button class="btn btn-light" :disabled="loading" v-on:click="integrate"><span class="fa fa-check"> </span>Integrate</button>
            </div>
        </div>
        <div class="col-12">
        <h6><span class="fa fa-cog fa-spin" v-if="loading"></span></h6>
        </div>
        <div v-if=true>
            {{ status }}
        </div>
        <div class="col-12">
            <div class="card card-body block" v-if="overlap_list">
                <h6 class="block-title">
                    Overlap
                </h6>
                <table style="width:100%" border="0px">
                    <tr>
                        <th>omic 1</th>
                        <th>omic 2</th>
                        <th>overlap</th>
                    </tr>
                    <tr v-for="overlap in overlap_list">
                        <td>
                            <div class="dropdown ml-2">
                                <button class="btn btn-link text-muted pr-1 pt-0 pb-0" data-toggle="dropdown">
                                    {{ overlap[0] }}
                                </button>
                                <div class="dropdown-menu dropdown-menu-right">
                                    <h6 class="dropdown-header">Annotations</h6>
                                    <a class="dropdown-item" v-for="annotation in overlap[3]">
                                        {{ annotation }}
                                    </a>
                                </div>
                            </div>
                        </td>
                        <td>
                            <div class="dropdown ml-2">
                                <button class="btn btn-link text-muted pr-1 pt-0 pb-0" data-toggle="dropdown">
                                    {{ overlap[1] }}
                                </button>
                                <div class="dropdown-menu dropdown-menu-right">
                                    <h6 class="dropdown-header">Annotations</h6>
                                    <a class="dropdown-item" v-for="annotation in overlap[4]">
                                        {{ annotation }}
                                    </a>
                                </div>
                            </div>
                        </td>
                        <td>
                            <div class="dropdown ml-2">
                                <button class="btn btn-link text-muted pr-1 pt-0 pb-0" data-toggle="dropdown">
                                    {{ overlap[2] }} / {{ overlap[3].length + overlap[4].length - overlap[5].length}}
                                </button>
                                <div class="dropdown-menu dropdown-menu-right">
                                    <h6 class="dropdown-header">Annotations</h6>
                                    <a class="dropdown-item" v-for="annotation in overlap[5]">
                                        {{ annotation }}
                                    </a>
                                </div>
                            </div>
                        </td>
                    </tr>
                </table>
            </div>
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
            min_connected: 3,
            pvalue_treshold: 1,
            loading: false,
            projectId1: null,
            projectId2: null,
            id_type1: null,
            id_type2: null,
            overlap_list: null,
            status: null
        }
    },

    components: {
        SemanticProjectSelect
    },

    methods: {
        integrate() {
            var ref = this
            this.status = null
            this.loading = true
            this.overlap_list = null
            $.getJSON(`${ROOTURL}/integrate`,{"projectId1": this.projectId1,
                "projectId2": this.projectId2, "id_type1": this.id_type1,
                "id_type2": this.id_type2,
                "annotation_type": this.annotation_type})
            .then(data => {
                this.overlap_list = data
                this.loading = false
            })
            .fail(function(request, status, error) {
                ref.loading = false
                ref.status = status
            })
        }
    },

    created() {
        this.annotation_type = this.annotation_types[0]
    }
}
</script>
