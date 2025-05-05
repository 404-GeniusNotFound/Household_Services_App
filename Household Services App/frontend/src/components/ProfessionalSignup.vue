<template>
  <div class="signup-container">
    <h2 class="title">Professional Signup</h2>
    <form
      @submit.prevent="signup"
      class="signup-form"
      enctype="multipart/form-data"
    >
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
          type="tel"
          v-model="phone_number"
          class="form-control"
          required
          pattern="\d{10}"
          maxlength="10"
          title="Please enter a 10-digit phone number"
          @input="validatePhoneNumber"
        />
        <p v-if="phoneError" class="text-danger">{{ phoneError }}</p>
      </div>
      <div class="form-group">
        <label for="service_name" class="form-label">Service Name:</label>
        <select v-model="service_name" class="form-control" required>
          <option value="" disabled>Select a Service</option>
          <option
            v-for="category in categories"
            :key="category"
            :value="category"
          >
            {{ category }}
          </option>
        </select>
      </div>
      <div class="form-group">
        <label for="experience" class="form-label">Experience (years):</label>
        <input
          type="number"
          v-model="experience"
          class="form-control"
          required
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
      <div class="form-group">
        <label for="cv_file" class="form-label"
          >Upload CV (PDF/DOC/DOCX):</label
        >
        <input
          type="file"
          name="cv_file"
          @change="handleFileUpload"
          class="form-control"
          accept=".pdf, .doc, .docx"
        />
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
      service_name: "",
      experience: 0,
      address: "",
      pin_code: "",
      cv: null,
      message: "",
      error: "",
      phoneError: "",
      categories: [],
    };
  },
  mounted() {
    this.fetchCategories();
  },
  methods: {
    fetchCategories() {
      axios
        .get("http://localhost:5000/services/categories")
        .then((response) => {
          this.categories = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    handleFileUpload(event) {
      this.cv = event.target.files[0];
    },
    validatePhoneNumber() {
      const phonePattern = /^\d{10}$/;
      if (!phonePattern.test(this.phone_number)) {
        this.phoneError = "Phone number must be exactly 10 digits.";
      } else {
        this.phoneError = "";
      }
    },
    signup() {
      this.validatePhoneNumber();
      if (this.phoneError) return;

      const formData = new FormData();
      formData.append("email", this.email);
      formData.append("password", this.password);
      formData.append("full_name", this.full_name);
      formData.append("phone_number", this.phone_number);
      formData.append("service_name", this.service_name);
      formData.append("experience", this.experience);
      formData.append("address", this.address);
      formData.append("pin_code", this.pin_code);
      if (this.cv) {
        formData.append("cv_file", this.cv);
      }

      axios
        .post("http://localhost:5000/professional_signup", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
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
      this.service_name = "";
      this.experience = 0;
      this.address = "";
      this.pin_code = "";
      this.cv = null;
      this.phoneError = "";
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
