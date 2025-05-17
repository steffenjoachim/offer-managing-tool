<template>
  <el-container class="app-container">
    <el-header v-if="isLoggedIn">
      <el-menu mode="horizontal" :router="true" class="main-menu">
        <el-menu-item index="/">Home</el-menu-item>
        <el-menu-item index="/customers">Kunden</el-menu-item>
        <el-menu-item index="/offers">Angebote</el-menu-item>
        <el-menu-item index="/templates" v-if="isAdmin">Vorlagen</el-menu-item>

        <div class="flex-grow" />

        <el-sub-menu>
          <template #title>
            <el-icon><User /></el-icon>
            {{ username }}
          </template>
          <el-menu-item @click="logout">Abmelden</el-menu-item>
        </el-sub-menu>
      </el-menu>
    </el-header>

    <el-main>
      <router-view />
    </el-main>
  </el-container>
</template>

<script>
import { computed, onMounted } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";
import { User } from "@element-plus/icons-vue";

export default {
  name: "App",
  components: {
    User,
  },
  setup() {
    const store = useStore();
    const router = useRouter();

    const isLoggedIn = computed(() => store.getters["auth/isLoggedIn"]);
    const username = computed(() => store.getters["auth/username"]);
    const isAdmin = computed(() => store.getters["auth/isAdmin"]);

    const logout = async () => {
      await store.dispatch("auth/logout");
      router.push("/login");
    };

    onMounted(() => {
      store.dispatch("auth/checkAuth");
    });

    return {
      isLoggedIn,
      username,
      isAdmin,
      logout,
    };
  },
};
</script>

<style>
/* Globale Styles */
:root {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
    "Helvetica Neue", Arial, sans-serif;
}

/* Element Plus Overrides */
.el-menu {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
    "Helvetica Neue", Arial, sans-serif !important;
}

.el-menu-item {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
    "Helvetica Neue", Arial, sans-serif !important;
}

.el-sub-menu__title {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
    "Helvetica Neue", Arial, sans-serif !important;
}

/* App Container Styles */
.app-container {
  min-height: 100vh;
}

.el-header {
  padding: 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.main-menu {
  display: flex;
  align-items: center;
  height: 60px;
}

.flex-grow {
  flex-grow: 1;
}

.el-main {
  padding: 20px;
  background-color: #f5f7fa;
}
</style>
