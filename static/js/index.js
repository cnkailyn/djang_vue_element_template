let app = new Vue({
    el: '#app',
    delimiters: ["${", "}"],
    data: {
        show: {
           loading: false
        },
        visible: false,
        word_group_list: [],
        request: {
            words: "",
            user_ids: "",
            blog_ids: "",
            word_groups: [],
            publish_date_begin: "",
            publish_date_end: "",
            date_begin: "",
            date_end: "",
            types: ["curation", "hot", "realtime"]
        },
        response: {
            sort: {
                user: [],
                wei_bo: []
            }
        }
    },
    created: function () {
        console.log("created")
    },
    beforeMount: function () {
        console.log("beforeMount")
    },
    mounted: function () {
        console.log("mounted")
//        this.onInit();
    },
    methods: {
        onInit: function() {
            let that = this;
            axios.get("/api/all-word-group").then(function (res) {
                that.word_group_list = res.data.data;
            })
        },
        exportCsv: function(tb) {
        if (tb == "user") {
            this.$refs.userTable.exportCsv({
                            filename: '用户排名'
                        });
        } else {
            this.$refs.wbTable.exportCsv({
                            filename: '微博排名'
                        });
    }

    },
        onSearch: function () {
            let that = this;
            that.show.loading = true;
            axios.post("/api/counter", that.request).then(function(res) {
                that.response = res.data.data;
                that.show.loading = false;
            }).catch(function (e) {
                that.show.loading = false;
            });
        }
    }
})
