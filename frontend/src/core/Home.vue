<template>
  <div class="home-container">
    <el-row :gutter="20">
      <el-col :span="24">
        <h1>Willkommen in der Angebotsverwaltung</h1>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="mt-4">
      <el-col :xs="24" :sm="12" :md="8" v-for="i in 3" :key="i">
        <el-card class="feature-card">
          <template #header>
            <div class="card-header">
              <el-icon><Document /></el-icon>
              <span>Funktion {{ i }}</span>
            </div>
          </template>
          <div class="card-content">Beschreibung der Funktion {{ i }}</div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { Document } from "@element-plus/icons-vue";

export default {
  name: "HomeView",
  components: {
    Document,
  },
};
</script>

<style scoped>
.home-container {
  padding: 20px;
}

.mt-4 {
  margin-top: 2rem;
}

.feature-card {
  margin-bottom: 20px;
  height: 200px;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
}

.card-content {
  color: #666;
}
</style>
