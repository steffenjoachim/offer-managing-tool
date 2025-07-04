<template>
  <el-container class="app-container">
    <el-header>
      <div class="content-wrapper">
        <el-menu
          mode="horizontal"
          :router="true"
          class="main-menu"
          :ellipsis="false"
        >
          <el-menu-item index="/">Home</el-menu-item>

          <div class="flex-grow" />

          <template v-if="isLoggedIn">
            <el-dropdown @command="handleCommand">
              <span class="el-dropdown-link username-dropdown-trigger">
                {{ username }}
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="createListing"
                    >Create Listing</el-dropdown-item
                  >
                  <el-dropdown-item command="myMessages"
                    >My Messages</el-dropdown-item
                  >
                  <el-dropdown-item command="myListings"
                    >My Listings</el-dropdown-item
                  >
                  <el-dropdown-item command="myWatchlist"
                    >My Watchlist</el-dropdown-item
                  >
                  <el-dropdown-item command="logout">Logout</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </template>
          <template v-else>
            <el-menu-item index="/login" class="auth-menu-item"
              >Login/Register</el-menu-item
            >
          </template>
        </el-menu>
      </div>
    </el-header>

    <el-main>
      <div class="content-wrapper">
        <router-view />
      </div>
    </el-main>
  </el-container>
</template>

<script>
import { computed, onMounted } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";

export default {
  name: "App",
  setup() {
    const store = useStore();
    const router = useRouter();

    const isLoggedIn = computed(() => store.getters["auth/isLoggedIn"]);
    const username = computed(() => store.getters["auth/username"]);

    const handleCommand = async (command) => {
      if (command === "logout") {
        await store.dispatch("auth/logout");
        router.push("/login");
      } else if (command === "createListing") {
        router.push("/create-listing");
      } else if (command === "myListings") {
        router.push("/my-listings");
      } else if (command === "myMessages") {
        router.push("/my-messages");
      } else if (command === "myWatchlist") {
        router.push("/my-watchlist");
      }
    };

    onMounted(() => {
      store.dispatch("auth/checkAuth");
    });

    return {
      isLoggedIn,
      username,
      handleCommand,
    };
  },
};
</script>

<style>
/* Global Styles */
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

/* Remove default underline/border from dropdown trigger */
.username-dropdown-trigger {
  cursor: pointer;
  outline: none;
}

.auth-menu-item .el-tooltip__trigger {
  border: none !important;
  cursor: pointer;
}

.el-main {
  padding: 0;
  background-color: #f5f7fa;
}

.content-wrapper {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}
</style>
