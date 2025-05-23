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
        ref="registerForm"
        :model="registerData"
        :rules="rules"
        label-position="top"
        @submit.prevent="handleRegister"
      >
        <el-form-item label="Username" prop="username">
          <el-input
            v-model="registerData.username"
            placeholder="Enter username"
          />
        </el-form-item>

        <el-form-item label="Email" prop="email">
          <el-input
            v-model="registerData.email"
            placeholder="Enter email"
            type="email"
          />
        </el-form-item>

        <el-form-item label="First Name" prop="first_name">
          <el-input
            v-model="registerData.first_name"
            placeholder="Enter first name"
          />
        </el-form-item>

        <el-form-item label="Last Name" prop="last_name">
          <el-input
            v-model="registerData.last_name"
            placeholder="Enter last name"
          />
        </el-form-item>

        <el-form-item label="Phone" prop="phone">
          <el-input
            v-model="registerData.phone"
            placeholder="Enter phone number"
          />
        </el-form-item>

        <el-form-item label="Password" prop="password">
          <el-input
            v-model="registerData.password"
            type="password"
            placeholder="Enter password"
            show-password
          />
        </el-form-item>

        <el-form-item label="Confirm Password" prop="password2">
          <el-input
            v-model="registerData.password2"
            type="password"
            placeholder="Confirm password"
            show-password
          />
        </el-form-item>

        <el-form-item>
          <el-button
            type="primary"
            native-type="submit"
            :loading="loading"
            class="register-button"
          >
            Register
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
import { User } from "@element-plus/icons-vue";

export default {
  name: "RegisterView",
  components: {
    User,
  },
  setup() {
    const store = useStore();
    const router = useRouter();
    const registerForm = ref(null);
    const loading = ref(false);

    const registerData = reactive({
      username: "",
      email: "",
      first_name: "",
      last_name: "",
      phone: "",
      password: "",
      password2: "",
    });

    const validatePass = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("Please enter your password"));
      } else {
        if (registerData.password2 !== "") {
          registerForm.value?.validateField("password2");
        }
        callback();
      }
    };

    const validatePass2 = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("Please enter your password again"));
      } else if (value !== registerData.password) {
        callback(new Error("Passwords do not match!"));
      } else {
        callback();
      }
    };

    const rules = {
      username: [
        { required: true, message: "Please enter username", trigger: "blur" },
        {
          min: 3,
          message: "Username must be at least 3 characters",
          trigger: "blur",
        },
      ],
      email: [
        { required: true, message: "Please enter email", trigger: "blur" },
        {
          type: "email",
          message: "Please enter a valid email",
          trigger: "blur",
        },
      ],
      first_name: [
        { required: true, message: "Please enter first name", trigger: "blur" },
      ],
      last_name: [
        { required: true, message: "Please enter last name", trigger: "blur" },
      ],
      phone: [
        {
          required: false,
          message: "Please enter phone number",
          trigger: "blur",
        },
      ],
      password: [
        { required: true, validator: validatePass, trigger: "blur" },
        {
          min: 8,
          message: "Password must be at least 8 characters",
          trigger: "blur",
        },
        {
          pattern: /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*#?&]{8,}$/,
          message: "Password must contain at least one letter and one number",
          trigger: "blur",
        },
      ],
      password2: [
        { required: true, validator: validatePass2, trigger: "blur" },
        {
          required: true,
          message: "Please enter your password again",
          trigger: "blur",
        },
        { message: "Passwords do not match!", trigger: "blur" },
      ],
    };

    const handleRegister = async () => {
      if (!registerForm.value) return;

      try {
        await registerForm.value.validate();
        loading.value = true;

        const registrationData = {
          username: registerData.username,
          email: registerData.email,
          first_name: registerData.first_name,
          last_name: registerData.last_name,
          phone: registerData.phone || "",
          password: registerData.password,
          password2: registerData.password2,
        };

        await store.dispatch("auth/register", registrationData);

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
            } else if (errorData.non_field_errors) {
              errorMessage = errorData.non_field_errors.join(", ");
            } else {
              errorMessage = Object.entries(errorData)
                .map(
                  ([key, value]) =>
                    `${key}: ${Array.isArray(value) ? value.join(", ") : value}`
                )
                .join("; ");
            }
          } else {
            errorMessage = errorData.toString();
          }

          ElMessage.error(errorMessage || "Registration failed");
        } else {
          ElMessage.error("Registration failed");
        }
      } finally {
        loading.value = false;
      }
    };

    return {
      registerForm,
      registerData,
      rules,
      loading,
      handleRegister,
    };
  },
};
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f7fa;
}

.register-card {
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

.register-button {
  width: 100%;
}
</style>
