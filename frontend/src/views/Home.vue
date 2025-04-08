<template>
  <v-container>
    <v-row>
      <v-col cols="12" md="4">
        <v-card
          class="mx-auto"
          max-width="400"
          @click="navigateTo('customers')"
        >
          <v-card-title class="text-h5"> Kundenverwaltung </v-card-title>
          <v-card-text>
            <v-icon size="64" color="primary">mdi-account-group</v-icon>
            <p class="text-body-1 mt-4">
              Verwalten Sie Ihre Kunden und deren Daten
            </p>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="4">
        <v-card class="mx-auto" max-width="400" @click="navigateTo('offers')">
          <v-card-title class="text-h5"> Angebotsverwaltung </v-card-title>
          <v-card-text>
            <v-icon size="64" color="primary">mdi-file-document</v-icon>
            <p class="text-body-1 mt-4">Erstellen und verwalten Sie Angebote</p>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="4">
        <v-card
          class="mx-auto"
          max-width="400"
          @click="navigateTo('templates')"
          v-if="isAdmin"
        >
          <v-card-title class="text-h5"> Angebotsbausteine </v-card-title>
          <v-card-text>
            <v-icon size="64" color="primary">mdi-puzzle</v-icon>
            <p class="text-body-1 mt-4">
              Verwalten Sie Angebotsbausteine und Vorlagen
            </p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: "Home",
  computed: {
    isAdmin() {
      return this.$store.getters.isAdmin;
    },
  },
  methods: {
    navigateTo(route) {
      this.$router.push(`/${route}`);
    },
  },
};
</script>

<style scoped>
.v-card {
  cursor: pointer;
  transition: transform 0.2s;
}

.v-card:hover {
  transform: translateY(-5px);
}
</style>
