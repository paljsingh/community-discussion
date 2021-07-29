<template>
    <div class="usergroups">
        <vuetable ref="vuetable"
            class="new-users"
            :api-url="'http://127.0.0.1:5000/api/v1/usergroups'"
            :fields="fields"
            :current-page="0"
            :per-page="20"
            filter=""
            data-path="usergroups"
            pagination-path=""
            >
        </vuetable>
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
    position: relative;
    float: left;
    width: 80%;
}
</style>