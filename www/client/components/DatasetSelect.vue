<template>
<div class="card card-block block">
    <h5 class="card-title">Select datasets</h5>
    <div v-for="(item, index) in datasetnames" class="row">
        <div  class="col">
            Dataset name:
            <select v-model="item.name" id="name-select" class="btn btn-secondary">
                <option v-for="name in alldatasetnames">{{ name }}</option>
            </select>
            Omics type:
            <select v-model="item.type" id="name-select" class="btn btn-secondary">
                <option v-for="omicstype in omicstypes">{{ omicstype }}</option>
            </select>
            <button class="btn btn-primary" style="border-top-width: 1px" 
                        @click="removeDataset(index)">
                <i class="fa fa-times" aria-hidden="true"></i>
            </button>
        </div>
    </div>
    <div class="row">
        <button class="btn btn-primary" style="border-top-width: 1px" 
                        @click="addDataset">
            <i class="fa fa-plus" aria-hidden="true"></i> Add dataset
        </button>
        <button class="btn btn-secondary" style="border-top-width: 1px">
            Save
        </button>
        <button class="btn btn-secondary" style="border-top-width: 1px">
            Revert
        </button>
        <button class="btn btn-primary" style="border-top-width: 1px">
            Continue
        </button>
    </div>
    <div class="row">
    </div>
</div>
</template>

<script>
export default {
    data() {
        return {
            omicstypes:['Genes','Lipids','Metabolites','Proteins'],
            datasetnames: [{}],
            alldatasetnames: ['abc','def','ghi','123','456','789']
        }
    },

    props: ['name'],

    methods: {
        addDataset() {
            this.datasetnames.push({})
        },
        removeDataset(index) {
            this.datasetnames.splice(index, 1);
        }
    }
}
</script>
