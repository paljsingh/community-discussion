<template>
    <v-col class="navigation">
        <v-card>
            <v-navigation-drawer permanent dark color="#123" >
                <v-list>
                    <router-link to="/communities" class="header item">
                        <v-list-item link>
                            <v-list-item-icon>
                                <v-icon>mdi-account-group</v-icon>
                            </v-list-item-icon>
                            <v-list-item-title>Communities</v-list-item-title>
                        </v-list-item>
                    </router-link>

                    <router-link to="/usergroups" class="header item">
                        <v-list-item link>
                            <v-list-item-icon>
                                <v-icon>mdi-account-multiple</v-icon>
                            </v-list-item-icon>
                            <v-list-item-title>User Groups</v-list-item-title>
                        </v-list-item>
                    </router-link>

                    <router-link to="/users" class="header item">
                        <v-list-item link>
                            <v-list-item-icon>
                                <v-icon>mdi-account</v-icon>
                            </v-list-item-icon>
                            <v-list-item-title>Users</v-list-item-title>
                        </v-list-item>
                    </router-link>

                </v-list>
            </v-navigation-drawer>
        </v-card>
    </v-col>
</template>

<script>

export default {
  name: 'navigation',
}
</script>

<style scoped>
.navigation {
    position: fixed;
    width: 200px;
    top: 60px;
}

</style>
