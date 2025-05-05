<template>
  <div class="add-service-container">
    <h2 class="title">Create a New Service</h2>
    <form @submit.prevent="createService" class="service-form">
      <div class="form-group">
        <label for="name" class="form-label">Service Name:</label>
        <input type="text" v-model="name" class="form-control" required />
      </div>
      <div class="form-group">
        <label for="price" class="form-label">Price:</label>
        <input type="number" v-model="price" class="form-control" required />
      </div>
      <div class="form-group">
        <label for="category" class="form-label">Category:</label>
        <input type="text" v-model="category" class="form-control" required />
      </div>
      <div class="form-group">
        <label for="description" class="form-label">Description:</label>
        <textarea
          v-model="description"
          class="form-control"
          required
        ></textarea>
      </div>
      <button type="submit" class="btn btn-primary">Create Service</button>
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
      name: "",
      price: "",
      category: "",
      description: "",
      message: "",
      error: "",
    };
  },
  methods: {
    createService() {
      axios
        .post("http://localhost:5000/create_service", {
          name: this.name,
          price: this.price,
          category: this.category,
          description: this.description,
        })
        .then((response) => {
          this.message = response.data.message;
          this.error = "";
          this.resetForm();
          this.$emit("service-added");
          this.$emit("close");
        })
        .catch((error) => {
          this.error = error.response?.data?.error || "An error occurred.";
          this.message = "";
        });
    },
    resetForm() {
      this.name = "";
      this.price = "";
      this.category = "";
      this.description = "";
    },
  },
};
</script>

<style scoped>
.add-service-container {
  max-width: 500px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
  background-color: #fff;
}

.title {
  font-size: 24px;
  font-weight: 600;
  color: #333;
  margin-bottom: 20px;
  text-align: center;
}

.service-form {
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
