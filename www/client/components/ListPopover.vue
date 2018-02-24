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
            <h5 class="text-capitalize">{{ name }}</h5>
            <input type="text" placeholder="Search" class="bg-light w-100 p-1" v-model="searchTerm" />
            <div class="d-flex flex-column p-1">
                <div v-for="(item, i) in paginatedList" :key="item" class="d-flex align-items-center">
                    <div class="reformat-item w-100">
                        {{ item }}
                    </div>
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

    props: ['list', 'name'],

    methods: {
        prevPage() {
            if (this.canPrev) this.page = this.page - 1
        },
        nextPage() {
            if (this.canNext) this.page = this.page + 1
        },
        toAbsoluteIndex(i) {
            return ((this.page - 1) * this.items) + i
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
</style>