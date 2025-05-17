<template>
  <div class="login-container">
    <el-card class="login-card">
      <template #header>
        <div class="card-header">
          <el-icon><UserFilled /></el-icon>
          <span>Anmelden</span>
        </div>
      </template>

      <el-form
        ref="loginForm"
        :model="loginData"
        :rules="rules"
        label-position="top"
        @submit.prevent="handleLogin"
      >
        <el-form-item label="Benutzername" prop="username">
          <el-input
            v-model="loginData.username"
            placeholder="Benutzername eingeben"
          />
        </el-form-item>

        <el-form-item label="Passwort" prop="password">
          <el-input
            v-model="loginData.password"
            type="password"
            placeholder="Passwort eingeben"
            show-password
          />
        </el-form-item>

        <el-form-item>
          <el-button
            type="primary"
            native-type="submit"
            :loading="loading"
            class="login-button"
          >
            Anmelden
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import { ref, reactive } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";
import { ElMessage } from "element-plus";
import { UserFilled } from "@element-plus/icons-vue";

export default {
  name: "LoginView",
  components: {
    UserFilled,
  },
  setup() {
    const store = useStore();
    const router = useRouter();
    const loginForm = ref(null);
    const loading = ref(false);

    const loginData = reactive({
      username: "",
      password: "",
    });

    const rules = {
      username: [
        {
          required: true,
          message: "Bitte Benutzername eingeben",
          trigger: "blur",
        },
      ],
      password: [
        { required: true, message: "Bitte Passwort eingeben", trigger: "blur" },
      ],
    };

    const handleLogin = async () => {
      if (!loginForm.value) return;

      try {
        await loginForm.value.validate();
        loading.value = true;

        const response = await store.dispatch("auth/login", loginData);
        console.log("Login response:", response); // Debug-Log

        if (response) {
          ElMessage.success("Erfolgreich angemeldet!");
          await router.push("/");
        }
      } catch (error) {
        console.error("Login error:", error);
        ElMessage.error(
          error.response?.data?.detail || "Anmeldung fehlgeschlagen"
        );
      } finally {
        loading.value = false;
      }
    };

    return {
      loginForm,
      loginData,
      rules,
      loading,
      handleLogin,
    };
  },
};
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f7fa;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
    "Helvetica Neue", Arial, sans-serif;
}

.login-card {
  width: 100%;
  max-width: 400px;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 1.2em;
  font-weight: 500;
}

.login-button {
  width: 100%;
}
</style>
