<template>
        <v-expansion-panels>
            <v-expansion-panel>
                <v-expansion-panel-header>
                    <template v-slot>
                        <v-row no-gutters>
                            <v-col cols="4" class="text--secondary">
                                <v-fade-transition leave-absolute>
                                      <v-icon>mdi-account-search</v-icon>
                                </v-fade-transition>
                            </v-col>
                        </v-row>
                    </template>
                </v-expansion-panel-header>
                <v-expansion-panel-content>
                    <v-text-field v-model="user.name" placeholder="foo"></v-text-field>
                </v-expansion-panel-content>
            </v-expansion-panel>
        </v-expansion-panels>
</template>

<script>
    export default {
        name: 'UserSearch',
        open: true,
        data : function() {
            return {
                'user': {
                    'name': 'foo'
                },
                'foo': 'bar'
            }
        },
        methods: {
            open1: function() {
                return true;
            }
        }

    }
</script>
