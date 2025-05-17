<template>
  <div class="customers-container">
    <h1>Kundenverwaltung</h1>
    <base-card>
      <template #header>
        <div class="card-header">
          <el-icon><User /></el-icon>
          <span>Kundenliste</span>
        </div>
      </template>
      <p>Hier werden die Kunden angezeigt.</p>
    </base-card>
  </div>
</template>

<script>
import { User } from "@element-plus/icons-vue";
import BaseCard from "@/shared/components/BaseCard.vue";

export default {
  name: "CustomersView",
  components: {
    User,
    BaseCard,
  },
};
</script>

<style scoped>
.customers-container {
  padding: 20px;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
}
</style>
