<template>
    <v-col class="content">
        <v-card dark>
            <v-card-title dark>
                <v-text-field
                    v-model="search"
                    append-icon="mdi-magnify"
                    label="Search"
                    single-line
                    hide-details
                    dark
                ></v-text-field>
            </v-card-title>
            <v-data-table
                :items="items"
                :headers="headers"
                :options.sync="options"

                item-key="name"
                v-model="selected"
                @click:row="handleClick"
                
                :footer-props="{
                    'items-per-page-text':'',
                    'items-per-page-options': []
                }"
                @update:pagination="handlePageChange"
                :server-items-length="total"

                class="elevation-1"
                loading
                loading-text="Loading... Please wait"
                dense
                dark
            >
            </v-data-table>
        </v-card>
    </v-col>
</template>

<script>
    import axios from '../helpers/interceptor';

    export default {
        name: 'Communities',
        watch: {
            options: {
                handler() {
                    this.fetchData();
                },
                deep: true
            },
            search: {
                handler() {
                    this.fetchData();
                }
            }
        },
        data: function() {
            return {
                items: [],
                selected: [],
                singleSelect: false,

                headers: [
                    {
                        text: 'Community',
                        value: 'name',
                    },
                    {
                        text: 'Tags',
                        value: 'tags',
                    },
                ],
                apiUrl: process.env.VUE_APP_COMMUNITIES_API_ENDPOINT,
                search: "",
                total: 0,
                page: 1,
                perPage: 10,
                options: {}
            }
        },
        // created() {
        //     this.fetchData()
        // },
        methods: {
            async fetchData () {
                let params = Object.assign({}, this.options, {'name': this.search});
                let response = (await axios.get(this.apiUrl, {params: params})).data;
                this.items = response.data;

                console.log(this.items)
                this.total = response.pagination.total;
                this.size = (response.pagination.total-1) / response.pagination.page + 1;

                // let search = this.search.trim().toLowerCase();
                // if (search) {
                //     this.items = this.items.filter(item => {
                //         return Object.values(item)
                //             .join(",")
                //             .toLowerCase()
                //             .includes(search);
                //     });
                // }

                // let response = (await axios.get(this.apiUrl, {params: this.options})).data;
                // this.items = response.data;
                // this.page = response.pagination.page;
                // this.total = response.pagination.total;
                // this.size = (response.pagination.total-1) / response.pagination.page + 1;
                // console.log(this.items, this.total, this.size)
            },
            handlePageChange(value) {
                this.page = value;
            },
            handleClick(selected) {
                this.selected = [selected];
            },

        }
    };

</script>

<style scoped>
.content {
    position: relative;
    width: 500px;
    left: 10px;
}
</style>