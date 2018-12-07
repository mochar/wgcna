// Define the variable `itemList`
const PaginatedListMixin = {
    data() {
        return {
            page: 1,
            items: 5,
        }
    },

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
        pages() {
            return Math.ceil(this.itemList.length / this.items)
        },
        offset() {
            return (this.page - 1) * this.items
        },
        pageList() {
            return this.itemList.slice(this.offset, this.offset + this.items)
        },
        canPrev() {
            return this.page > 1
        },
        canNext() {
            return this.page < this.pages
        },
        pageItemIndices() {
            return this.$helpers.range(this.items).map(x => (this.page - 1) * this.items + x)
        }
    }
}

// The components in the analyze page should only update when the project changes
// AND when the component is active.
const AnalyzeTabMixin = {
    data() {
        return {
            active: false,
            projectChanged: false,
            projectUpdated: false
        }
    },
    
    methods: {
        projectUpdate() {console.log('PROJECT UPDATE')},
        projectChange() {console.log('PROJECT CHANGE')},
    },
    
    watch: {
        project(val, oldVal) {
            this.projectChanged = val.id !== oldVal.id
            this.projectUpdated = val.id === oldVal.id
            
            if (this.active) {
                this.projectChanged ? this.projectChange() : this.projectUpdate()
            }
        }
    },
    
    activated() {
        this.active = true
        if (this.projectChanged) {
            this.projectChange()
            this.projectChanged = false
        }
        if (this.projectUpdated) {
            this.projectUpdate()
            this.projectUpdated = false
        }
    },
    
    deactivated() {
        this.active = false
    }
}

export { PaginatedListMixin, AnalyzeTabMixin }
