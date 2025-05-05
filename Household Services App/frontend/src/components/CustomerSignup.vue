<!-- src/components/customersignup.vue -->
<template>
  <div class="signup-container">
    <h2 class="title">Customer Signup</h2>
    <form @submit.prevent="signup" class="signup-form">
      <div class="form-group">
        <label for="email" class="form-label">Email:</label>
        <input type="email" v-model="email" class="form-control" required />
      </div>
      <div class="form-group">
        <label for="password" class="form-label">Password:</label>
        <input
          type="password"
          v-model="password"
          class="form-control"
          required
        />
      </div>
      <div class="form-group">
        <label for="full_name" class="form-label">Full Name:</label>
        <input type="text" v-model="full_name" class="form-control" required />
      </div>
      <div class="form-group">
        <label for="phone_number" class="form-label">Phone Number:</label>
        <input
          type="text"
          v-model="phone_number"
          class="form-control"
          required
          maxlength="10"
          @input="phone_number = phone_number.replace(/\D/g, '').slice(0, 10)"
        />
      </div>
      <div class="form-group">
        <label for="address" class="form-label">Address:</label>
        <input type="text" v-model="address" class="form-control" required />
      </div>
      <div class="form-group">
        <label for="pin_code" class="form-label">Pin Code:</label>
        <input type="text" v-model="pin_code" class="form-control" required />
      </div>
      <button type="submit" class="btn btn-primary">Register</button>
    </form>
    <p v-if="message" class="text-success">{{ message }}</p>
    <p v-if="error" class="text-danger">{{ error }}</p>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      email: "",
      password: "",
      full_name: "",
      phone_number: "",
      address: "",
      pin_code: "",
      message: "",
      error: "",
    };
  },
  methods: {
    signup() {
      axios
        .post("http://localhost:5000/customer_signup", {
          email: this.email,
          password: this.password,
          full_name: this.full_name,
          phone_number: this.phone_number,
          address: this.address,
          pin_code: this.pin_code,
        })
        .then((response) => {
          this.message = response.data.message;
          this.error = "";
          this.resetForm();
          setTimeout(() => this.$router.push({ name: "Login" }), 1500);
        })
        .catch((error) => {
          this.error = error.response?.data?.error || "An error occurred.";
          this.message = "";
        });
    },
    resetForm() {
      this.email = "";
      this.password = "";
      this.full_name = "";
      this.phone_number = "";
      this.address = "";
      this.pin_code = "";
    },
  },
};
</script>

<style scoped>
.signup-container {
  max-width: 500px;
  margin: 0 auto;
  padding: 20px;
  background-color: #fff;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
}

.title {
  font-size: 24px;
  font-weight: 600;
  color: #333;
  margin-bottom: 20px;
  text-align: center;
}

.signup-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-label {
  font-size: 14px;
  color: #555;
  margin-bottom: 5px;
}

.form-control {
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.btn-primary {
  padding: 10px;
  font-size: 16px;
  font-weight: 600;
  color: #fff;
  background-color: #007bff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn-primary:hover {
  background-color: #0056b3;
}

.text-success {
  color: #28a745;
  font-size: 14px;
  margin-top: 10px;
  text-align: center;
}

.text-danger {
  color: #dc3545;
  font-size: 14px;
  margin-top: 10px;
  text-align: center;
}
</style>
