<template>
  <div class="templates-container">
    <h1>Vorlagenverwaltung</h1>
    <base-card>
      <template #header>
        <div class="card-header">
          <el-icon><Files /></el-icon>
          <span>Vorlagenliste</span>
        </div>
      </template>
      <p>Hier werden die Vorlagen angezeigt.</p>
    </base-card>
  </div>
</template>

<script>
import { Files } from "@element-plus/icons-vue";
import BaseCard from "@/shared/components/BaseCard.vue";

export default {
  name: "TemplatesView",
  components: {
    Files,
    BaseCard,
  },
};
</script>

<style scoped>
.templates-container {
  padding: 20px;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
}
</style>
