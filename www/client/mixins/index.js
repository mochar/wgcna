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

export { PaginatedListMixin }