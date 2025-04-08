<template>
  <v-app>
    <v-app-bar app color="primary" dark v-if="isLoggedIn">
      <v-app-bar-title>Angebotsverwaltung</v-app-bar-title>
      <v-spacer></v-spacer>
      <v-btn icon @click="goHome">
        <v-icon>mdi-home</v-icon>
      </v-btn>
      <v-menu offset-y>
        <template v-slot:activator="{ on, attrs }">
          <v-btn icon v-bind="attrs" v-on="on">
            <v-icon>mdi-account</v-icon>
          </v-btn>
        </template>
        <v-list>
          <v-list-item>
            <v-list-item-title>{{ username }}</v-list-item-title>
          </v-list-item>
          <v-divider></v-divider>
          <v-list-item @click="logout">
            <v-list-item-title>Abmelden</v-list-item-title>
            <v-list-item-icon>
              <v-icon>mdi-logout</v-icon>
            </v-list-item-icon>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-app-bar>

    <v-main>
      <router-view></router-view>
    </v-main>
  </v-app>
</template>

<script>
export default {
  name: "App",
  computed: {
    isLoggedIn() {
      return this.$store.getters.isLoggedIn;
    },
    username() {
      return this.$store.getters.currentUser?.username || "";
    },
  },
  methods: {
    goHome() {
      this.$router.push("/");
    },
    logout() {
      this.$store.dispatch("logout");
      this.$router.push("/login");
    },
  },
  created() {
    // Beim Start der Anwendung prüfen, ob der Benutzer bereits angemeldet ist
    this.$store.dispatch("checkAuth");
  },
};
</script>
