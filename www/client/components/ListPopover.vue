<template>
<div style="display: inline-block">
    <button class="btn btn-light">
        <span class="text-lowercase">
            {{ list.length }} {{ name }}
            <font-awesome-icon icon="caret-down" />
        </span>
    </button>
    <div class="webui-popover-content">
        <div class="popover-body">
            <h5 class="text-capitalize">{{ name }}</h5>
            <input type="text" placeholder="Search" class="bg-light w-100 p-1" v-model="searchTerm" />
            <div class="d-flex flex-column p-1">
                <div v-for="(item, i) in pageList" :key="item" class="d-flex align-items-center">
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
import { PaginatedListMixin } from 'mixins'

export default {
    mixins: [PaginatedListMixin],

    data() {
        return {
            searchTerm: '',
            items: 12,
        }
    },

    props: ['list', 'name'],

    computed: {
        itemList() {
            if (this.searchTerm === '') 
                return this.list
            else 
                return this.list.filter(item => item.search(this.searchTerm) > -1)
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