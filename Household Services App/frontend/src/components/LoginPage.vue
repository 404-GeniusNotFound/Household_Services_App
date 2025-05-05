<template>
  <div class="login-container">
    <h2 class="title">Login</h2>
    <form @submit.prevent="login" class="login-form">
      <input
        type="email"
        v-model="email"
        placeholder="Email"
        required
        class="input-field"
      />
      <input
        type="password"
        v-model="password"
        placeholder="Password"
        required
        class="input-field"
      />
      <button type="submit" class="submit-button">Login</button>
    </form>
    <div class="signup-options">
      <p class="no-account-text">No account?</p>
      <p>
        <router-link to="/customer_signup" class="signup-link">
          Create a Customer Account
        </router-link>
        |
        <router-link to="/professional_signup" class="signup-link">
          Create a Professional Account
        </router-link>
      </p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      email: "",
      password: "",
    };
  },
  methods: {
    login() {
      axios
        .post("http://localhost:5000/login", {
          email: this.email,
          password: this.password,
        })
        .then((response) => {
          const role = response.data.role;
          localStorage.setItem("role", role);

          if (role === "customer") {
            localStorage.setItem("customerId", response.data.user_id);
            localStorage.setItem("customerFullName", response.data.full_name);
            this.$router.push("/customer-dashboard");
          } else if (role === "professional") {
            localStorage.setItem("professionalId", response.data.user_id);
            localStorage.setItem(
              "professionalFullName",
              response.data.full_name
            );
            this.$router.push("/professional-dashboard");
          } else if (role === "admin") {
            this.$router.push("/admin-dashboard");
          } else {
            alert("Unknown role. Please contact support.");
          }
        })
        .catch(() => {
          alert("Invalid email or password");
        });
    },
  },
};
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 2rem;
  text-align: center;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
  background-color: #fff;
}

.title {
  font-size: 24px;
  font-weight: 600;
  color: #333;
  margin-bottom: 1.5rem;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  align-items: stretch;
}

.input-field {
  padding: 0.75rem;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 4px;
  width: 100%;
}

.submit-button {
  padding: 0.75rem;
  font-size: 16px;
  font-weight: 600;
  color: #fff;
  background-color: #007bff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.submit-button:hover {
  background-color: #0056b3;
}

.signup-options {
  margin-top: 1.5rem;
  color: #666;
  font-size: 14px;
}

.no-account-text {
  margin-bottom: 0.5rem;
}

.signup-link {
  color: #007bff;
  text-decoration: none;
  font-weight: 500;
}

.signup-link:hover {
  text-decoration: underline;
}
</style>
