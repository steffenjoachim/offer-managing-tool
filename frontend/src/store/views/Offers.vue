<template>
  <div class="offers-container">
    <h1>Angebotsverwaltung</h1>
    <base-card>
      <template #header>
        <div class="card-header">
          <el-icon><Document /></el-icon>
          <span>Angebotsliste</span>
        </div>
      </template>
      <p>Hier werden die Angebote angezeigt.</p>
    </base-card>
  </div>
</template>

<script>
import { Document } from "@element-plus/icons-vue";
import BaseCard from "@/shared/components/BaseCard.vue";

export default {
  name: "OffersView",
  components: {
    Document,
    BaseCard,
  },
};
</script>

<style scoped>
.offers-container {
  padding: 20px;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
}
</style>
