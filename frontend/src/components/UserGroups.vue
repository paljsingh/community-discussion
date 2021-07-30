<template>
    <div class="usergroups">
        <v-data-table
            :items="items"
            :headers="headers"
            :options.sync="options"
            :server-items-length="total"
            hide-default-header
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

    export default {
        name: 'UserGroups',
        props: ['token', 'usertype'],
        data: function() {
            return {
                all_users: [],
                fields: [
                    {
                      name: 'name',
                      title: 'User Group Name'
                    },
                    {
                      name: 'created_by',
                      title: 'Created By'
                    },
                    {
                      name: 'created_on',
                      title: 'Created On'
                    }
                ]
            }
        }
    };

</script>

<style scoped>
.usergroups {
    position: fixed;
    width: 250px;
    left: 200px;
    top: 60px;
    font-size: 12px;
    /* background: #000; */
}
</style>