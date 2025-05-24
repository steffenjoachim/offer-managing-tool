<template>
  <div class="register-container">
    <el-card class="register-card">
      <template #header>
        <div class="card-header">
          <el-icon><User /></el-icon>
          <span>Register</span>
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
          <el-input v-model="form.username" placeholder="Choose a username" />
        </el-form-item>

        <el-form-item label="Email" prop="email">
          <el-input v-model="form.email" placeholder="Enter your email" />
        </el-form-item>

        <el-form-item label="Password" prop="password">
          <el-input
            v-model="form.password"
            type="password"
            placeholder="Choose a password"
            show-password
          />
        </el-form-item>

        <el-form-item label="Confirm Password" prop="password2">
          <el-input
            v-model="form.password2"
            type="password"
            placeholder="Confirm your password"
            show-password
          />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" native-type="submit" :loading="loading">
            Register
          </el-button>
        </el-form-item>

        <div class="login-link">
          <span>Already have an account?</span>
          <router-link to="/login" class="link">Login here</router-link>
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
import { User } from "@element-plus/icons-vue";

export default {
  name: "Register",
  components: {
    User,
  },
  setup() {
    const store = useStore();
    const router = useRouter();
    const formRef = ref(null);
    const loading = ref(false);

    const form = reactive({
      username: "",
      email: "",
      password: "",
      password2: "",
    });

    const validatePass2 = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("Please confirm your password"));
      } else if (value !== form.password) {
        callback(new Error("Passwords do not match"));
      } else {
        callback();
      }
    };

    const rules = {
      username: [
        { required: true, message: "Please enter a username", trigger: "blur" },
        {
          min: 3,
          max: 150,
          message: "Length should be 3 to 150 characters",
          trigger: "blur",
        },
      ],
      email: [
        { required: true, message: "Please enter your email", trigger: "blur" },
        {
          type: "email",
          message: "Please enter a valid email address",
          trigger: "blur",
        },
      ],
      password: [
        { required: true, message: "Please enter a password", trigger: "blur" },
        {
          min: 8,
          message: "Password must be at least 8 characters long",
          trigger: "blur",
        },
      ],
      password2: [
        {
          required: true,
          message: "Please confirm your password",
          trigger: "blur",
        },
        { validator: validatePass2, trigger: "blur" },
      ],
    };

    const handleSubmit = async () => {
      if (!formRef.value) return;

      try {
        await formRef.value.validate();
        loading.value = true;

        await store.dispatch("auth/register", {
          username: form.username,
          email: form.email,
          password: form.password,
          password2: form.password2,
        });

        ElMessage.success("Registration successful! Please login.");
        router.push("/login");
      } catch (error) {
        console.error("Registration error:", error);
        if (error.response?.data) {
          const errorData = error.response.data;
          let errorMessage = "";

          if (typeof errorData === "object") {
            if (errorData.username) {
              errorMessage = `Username: ${errorData.username.join(", ")}`;
            } else if (errorData.email) {
              errorMessage = `Email: ${errorData.email.join(", ")}`;
            } else if (errorData.password) {
              errorMessage = `Password: ${errorData.password.join(", ")}`;
            } else if (errorData.password2) {
              errorMessage = `Password confirmation: ${errorData.password2.join(
                ", "
              )}`;
            } else {
              errorMessage = "Registration failed";
            }
          } else {
            errorMessage = errorData;
          }
          ElMessage.error(errorMessage);
        } else {
          ElMessage.error("Registration failed");
        }
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
.register-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
}

.register-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
}

.login-link {
  margin-top: 16px;
  text-align: center;
  font-size: 14px;
}

.login-link .link {
  margin-left: 4px;
  color: #409eff;
  text-decoration: none;
}

.login-link .link:hover {
  text-decoration: underline;
}
</style>
