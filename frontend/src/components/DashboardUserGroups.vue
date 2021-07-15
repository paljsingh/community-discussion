<template>
    <div class="dashboard-usergroups">
        <h4>User Groups</h4>
        <label for="text-usergroups">How many user groups to create?</label>
        <input type="text" id="text-usergroups" v-model="num_usergroups" placeholder=num_communities />
        <button id="button-usergroups" class="ui primary button" role="button" v-on:click="create_usergroups()" >
            Go
        </button>

        <div class="field" id="alert">
            <v-alert dense text type="success">
                Created "usergroups.length" user groups.
            </v-alert>
        </div>
    </div>
</template>