<template>
  <div class="login-container">
    <el-card class="login-card">
      <template #header>
        <div class="card-header">
          <el-icon><UserFilled /></el-icon>
          <span>Login</span>
        </div>
      </template>

      <el-form
        ref="loginForm"
        :model="loginData"
        :rules="rules"
        label-position="top"
        @submit.prevent="handleLogin"
      >
        <el-form-item label="Username" prop="username">
          <el-input v-model="loginData.username" placeholder="Enter username" />
        </el-form-item>

        <el-form-item label="Password" prop="password">
          <el-input
            v-model="loginData.password"
            type="password"
            placeholder="Enter password"
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
            Login
          </el-button>
        </el-form-item>

        <div class="register-link">
          <span>No account yet?</span>
          <router-link to="/register" class="link">Register now</router-link>
        </div>
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
          message: "Please enter username",
          trigger: "blur",
        },
      ],
      password: [
        { required: true, message: "Please enter password", trigger: "blur" },
      ],
    };

    const handleLogin = async () => {
      if (!loginForm.value) return;

      try {
        await loginForm.value.validate();
        loading.value = true;

        const response = await store.dispatch("auth/login", loginData);
        console.log("Login response:", response);

        if (response) {
          ElMessage.success("Login successful!");
          await router.push("/");
        }
      } catch (error) {
        console.error("Login error:", error);
        ElMessage.error(error.response?.data?.detail || "Login failed");
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

.register-link {
  text-align: center;
  margin-top: 1rem;
  color: #606266;
}

.register-link .link {
  color: #409eff;
  text-decoration: none;
  margin-left: 0.5rem;
}

.register-link .link:hover {
  text-decoration: underline;
}
</style>
