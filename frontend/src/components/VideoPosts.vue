<template>
    <v-col class="content">
        <v-card dark>
            <v-label dark>
                <h1>{{ this.community[0].name }}</h1>
                <hr/>
            </v-label>
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
                :server-items-length="total"

                class="elevation-1"
                loading
                loading-text="Loading... Please wait"
                dense
                dark
            >
                <template v-slot:[`item.file`]="{item}">
                    <vue-player :src="'http://localhost:5002/api/v1/video/' + item._id" v-model="playing"></vue-player>
                </template>
            </v-data-table>
        </v-card>
    </v-col>
</template>

<script>
    import axiosInstance from '../helpers/interceptor';
    import vuePlayer  from  '@algoz098/vue-player';

    export default {
        name: 'Posts',
        props: ['community'],
        components: {
			vuePlayer
		},
        watch: {
            options: {
                handler() {
                    this.fetchData();
                },
                deep: true
            },
            community: {
                handler() {
                    this.options.page = 1;
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
                        text: "#",
                        value: 'rowid',
                    },
                    {
                        text: 'User',
                        value: 'created_by',
                    },
                    {
                        text: 'File',
                        value: 'file',
                    },
                    {
                        text: 'File Name',
                        value: 'name',
                    },

                ],
                apiUrl: process.env.VUE_APP_COMMUNITIES_VIDEOS_API_ENDPOINT,
                usersApiUrl: process.env.VUE_APP_USERS_API_ENDPOINT,
                search: "",
                total: 0,
                page: 1,
                perPage: 10,
                options: {}
            }
        },
        methods: {
            async fetchData () {
                let apiUrl = this.apiUrl.replace('community_id', this.community[0]._id)
                let params = Object.assign({}, this.options, {'name': this.search});
                let response = (await axiosInstance.get(apiUrl, {params: params})).data;
                this.items = response.data;

                this.total = response.pagination.total;
                this.size = (response.pagination.total-1) / response.pagination.page + 1;

                // transform data (set ids, set user name instead of id)
                for (let i=0; i< this.items.length; i++) {
                    let response = (await axiosInstance.get(this.usersApiUrl + "/" + this.items[i].created_by)).data;
                    this.items[i].created_by = response.name;

                    this.items[i].rowid = i+1;
                }
            },
            handleClick(selectedPost) {
                this.selected = [selectedPost];
            },
        }
    };

</script>
