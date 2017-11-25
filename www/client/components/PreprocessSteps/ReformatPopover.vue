<template>
<div style="display: inline-block">
    <button class="btn btn-light">
        <span class="text-lowercase">
            {{ list.length }} {{ name }}
            <span class="fa fa-caret-down"></span>
        </span>
    </button>
    <div class="webui-popover-content">
        <div class="popover-body">
            <h5>{{ name }}</h5>
            <input type="text" placeholder="Search" class="bg-light w-100 p-1"
                v-model="searchTerm" />
            <div class="d-flex flex-column p-1">
                <div v-for="(item, i) in paginatedList" :key="item" class="d-flex align-items-center">
                    <div class="reformat-item w-100">
                        {{ item }}
                    </div>
                    <button class="btn btn-link pb-0 pt-0" @click="$emit('selected', toAbsoluteIndex(i))">
                        <span class="fa fa-trash" :class="trashClass(i)"></span>
                    </button>
                    <button class="btn btn-link pb-0 pt-0 pl-0 text-primary" @click="setContinues(i)" v-if="trait">
                        <strong v-if="isContinues(i)">C</strong>
                        <strong v-else>N</strong>
                    </button>
                </div>
            </div>
            <div style="border-top: 1px solid #eee" class="w-100">
                <button class="btn btn-link" @click="prevPage" :disabled="!canPrev">Previous</button>
                <button class="btn btn-link float-right" @click="nextPage" :disabled="!canNext">Next</button>
            </div>
        </div>
    </div>
</div>   
</template>

<script>
import webuiPopover from 'webui-popover'

export default {
    data() {
        return {
            searchTerm: '',
            items: 12,
            page: 1
        }
    },

    props: ['list', 'removedIndices', 'continuesIndices', 'name', 'trait'],

    methods: {
        prevPage() {
            if (this.canPrev) this.page = this.page - 1
        },
        nextPage() {
            if (this.canNext) this.page = this.page + 1
        },
        toAbsoluteIndex(i) {
            return ((this.page - 1) * this.items) + i
        },
        trashClass(i) {
            const isRemoved = this.removedIndices.includes(this.toAbsoluteIndex(i))
            return isRemoved ? 'text-danger' : 'text-secondary'
        },
        isContinues(i) {
            return this.continuesIndices.includes(this.toAbsoluteIndex(i))
        },
        setContinues(i) {
            this.$emit('traitSelected', this.toAbsoluteIndex(i))
        }
    },

    computed: {
        searchedList() {
            if (this.searchTerm === '') 
                return this.list
            else 
                return this.list.filter(item => item.search(this.searchTerm) > -1)
        },
        pages() {
            return Math.ceil(this.searchedList.length / this.items)
        },
        offset() {
            return (this.page - 1) * this.items
        },
        paginatedList() {
            return this.searchedList.slice(this.offset, this.offset + this.items)
        },
        canPrev() {
            return this.page > 1
        },
        canNext() {
            return this.page < this.pages
        }
    },

    mounted() {
        const els = $(this.$el).find('div')
        $(this.$el).find('button').first().webuiPopover({placement: 'bottom'})
    }
}	
</script>

<style>
.popover-body {
    display: inline;
    padding: 0;
}

.reformat-item {
    cursor: pointer;
}
.reformat-item:hover {
    background-color: #eee;
}
</style>