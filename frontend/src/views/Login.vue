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
        ref="formRef"
        :model="form"
        :rules="rules"
        label-position="top"
        @submit.prevent="handleSubmit"
      >
        <el-form-item label="Username" prop="username">
          <el-input v-model="form.username" placeholder="Enter your username" />
        </el-form-item>

        <el-form-item label="Password" prop="password">
          <el-input
            v-model="form.password"
            type="password"
            placeholder="Enter your password"
            show-password
          />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" native-type="submit" :loading="loading">
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
  name: "Login",
  components: {
    UserFilled,
  },
  setup() {
    const store = useStore();
    const router = useRouter();
    const formRef = ref(null);
    const loading = ref(false);

    const form = reactive({
      username: "",
      password: "",
    });

    const rules = {
      username: [
        {
          required: true,
          message: "Please enter your username",
          trigger: "blur",
        },
      ],
      password: [
        {
          required: true,
          message: "Please enter your password",
          trigger: "blur",
        },
      ],
    };

    const handleSubmit = async () => {
      if (!formRef.value) return;

      try {
        await formRef.value.validate();
        loading.value = true;

        await store.dispatch("auth/login", {
          username: form.username,
          password: form.password,
        });

        ElMessage.success("Login successful!");
        router.push("/");
      } catch (error) {
        console.error("Login error:", error);
        ElMessage.error(error.response?.data?.detail || "Login failed");
      } finally {
        loading.value = false;
      }
    };

    return {
      formRef,
      form,
      rules,
      loading,
      handleSubmit,
    };
  },
};
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
}

.login-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
}

.register-link {
  margin-top: 16px;
  text-align: center;
  font-size: 14px;
}

.register-link .link {
  margin-left: 4px;
  color: #409eff;
  text-decoration: none;
}

.register-link .link:hover {
  text-decoration: underline;
}
</style>
