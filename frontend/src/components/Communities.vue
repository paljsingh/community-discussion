<template>
    <div class="content">
        <v-data-table
            :items="items"
            :headers="headers"
            :options.sync="options"
            :server-items-length="total"
            class="elevation-1"
            loading
            loading-text="Loading... Please wait"
            dense
            :search="search"
            :footer-props="{
                'items-per-page-text':'',
                'items-per-page-options': []
            }"
            @update:pagination="handlePageChange"
            dark
        >
        </v-data-table>
    </div>
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
            }
        },
        data: function() {
            return {
                items: [],
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
                options: {},
                total: 0,
                size: 0,
                page: 0,
            }
        },
        methods: {
            async fetchData () {
                let response = (await axios.get(this.apiUrl, {params: this.options})).data;
                this.items = response.data;
                this.page = response.pagination.page;
                this.total = response.pagination.total;
                this.size = (response.pagination.total-1) / response.pagination.page + 1;
                console.log(this.items, this.total, this.size)
            },
            handlePageChange(value) {
                this.page = value;
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