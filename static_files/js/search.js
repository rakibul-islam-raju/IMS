
const sellSearch = {
    data(){
        return{
            searchedData: false,
            showTable: true,
            showPagination: true,
            noData: false,
            data: [],
            url: ''
        }
    },
    methods: {
        searchSellProdyct(){
            this.url = window.location.host
            const pagination = document.getElementById('pagination')
            const searchValue = document.getElementById('searchSellProduct').value
            if (searchValue.trim().length > 0){
                fetch("/sells/search", {
                    body: JSON.stringify({ searchSells: searchValue }),
                    method: "POST",
                })
                .then((res) => res.json())
                .then((data) => {
                    this.showTable = false
                    this.showPagination = false
                    this.searchedData = true
                    if (data.length === 0) {
                        this.noData = true
                    }else{
                        this.data = data
                    }
                })
            }else{
                this.showTable = true
                this.showPagination = true
                this.searchedData = false
            }
        }
    },
    delimiters: ['[[', ']]']
}


Vue.createApp(sellSearch).mount('#sell-search')