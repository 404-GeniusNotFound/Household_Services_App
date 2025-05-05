<template>
  <div class="edit-service-container">
    <h2 class="title">Edit Service</h2>
    <form @submit.prevent="editService" class="edit-service-form">
      <div class="form-group">
        <label for="name" class="form-label">Service Name:</label>
        <input type="text" v-model="form.name" class="form-control" required />
      </div>
      <div class="form-group">
        <label for="price" class="form-label">Price:</label>
        <input
          type="number"
          v-model="form.price"
          class="form-control"
          required
        />
      </div>
      <div class="form-group">
        <label for="category" class="form-label">Category:</label>
        <input
          type="text"
          v-model="form.category"
          class="form-control"
          required
        />
      </div>
      <div class="form-group">
        <label for="description" class="form-label">Description:</label>
        <textarea
          v-model="form.description"
          class="form-control"
          required
        ></textarea>
      </div>
      <button type="submit" class="btn btn-primary">Save Changes</button>
    </form>
    <p v-if="message" class="text-success">{{ message }}</p>
    <p v-if="error" class="text-danger">{{ error }}</p>
  </div>
</template>

<script>
import axios from "axios";

export default {
  props: {
    service: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      form: {
        name: this.service.name,
        price: this.service.price,
        category: this.service.category, // Use a text input for category
        description: this.service.description,
      },
      message: "",
      error: "",
    };
  },
  watch: {
    service: {
      handler(newService) {
        this.form = {
          name: newService.name,
          price: newService.price,
          category: newService.category,
          description: newService.description,
        };
      },
      immediate: true,
    },
  },
  methods: {
    editService() {
      axios
        .put(`http://localhost:5000/services/${this.service.id}`, this.form)
        .then((response) => {
          this.message = response.data.message;
          this.error = "";
          this.$emit("service-edited");
          this.$emit("close");
        })
        .catch((error) => {
          this.error = error.response?.data?.error || "An error occurred.";
          this.message = "";
        });
    },
  },
};
</script>

<style scoped>
.edit-service-container {
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

.edit-service-form {
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
