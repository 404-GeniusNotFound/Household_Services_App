<template>
  <div class="edit-profile-container">
    <h2>Edit Profile</h2>
    <form @submit.prevent="editProfile">
      <div class="form-group">
        <label for="full_name">Full Name:</label>
        <input
          type="text"
          v-model="form.full_name"
          class="form-control"
          required
        />
      </div>
      <div class="form-group">
        <label for="phone_number">Phone Number:</label>
        <input
          type="text"
          v-model="form.phone_number"
          class="form-control"
          required
        />
      </div>
      <div class="form-group">
        <label for="address">Address:</label>
        <input
          type="text"
          v-model="form.address"
          class="form-control"
          required
        />
      </div>
      <div class="form-group">
        <label for="pin_code">Pin Code:</label>
        <input
          type="text"
          v-model="form.pin_code"
          class="form-control"
          required
        />
      </div>
      <div class="button-group">
        <button type="submit" class="btn btn-primary">Save Changes</button>
        <button type="button" @click="$emit('close')" class="btn btn-secondary">
          Cancel
        </button>
      </div>
    </form>
    <p v-if="message" class="text-success">{{ message }}</p>
    <p v-if="error" class="text-danger">{{ error }}</p>
  </div>
</template>

<script>
import axios from "axios";

export default {
  props: {
    customerId: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      form: {
        full_name: "",
        phone_number: "",
        address: "",
        pin_code: "",
      },
      message: "",
      error: "",
    };
  },
  mounted() {
    this.loadCustomerProfile();
  },
  methods: {
    loadCustomerProfile() {
      axios
        .get(`http://localhost:5000/customers/${this.customerId}`)
        .then((response) => {
          this.form = {
            full_name: response.data.full_name,
            phone_number: response.data.phone_number,
            address: response.data.address,
            pin_code: response.data.pin_code,
          };
          this.error = "";
        })
        .catch((error) => {
          this.error = "Failed to load profile details.";
          console.error("Error loading profile:", error);
        });
    },
    editProfile() {
      axios
        .put(`http://localhost:5000/customers/${this.customerId}`, this.form)
        .then((response) => {
          this.message = response.data.message;
          this.error = "";
          this.$emit("profile-updated");
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
.edit-profile-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
}

.form-group {
  margin-bottom: 15px;
}

.form-control {
  width: 100%;
  padding: 8px;
  font-size: 16px;
}

.button-group {
  display: flex;
  justify-content: space-between;
  margin-top: 15px;
}

.btn {
  padding: 8px 12px;
  font-size: 16px;
  cursor: pointer;
  border: none;
}

.btn-primary {
  background-color: #007bff;
  color: #fff;
}

.btn-primary:hover {
  background-color: #0056b3;
}

.btn-secondary {
  background-color: #6c757d;
  color: #fff;
}

.btn-secondary:hover {
  background-color: #5a6268;
}

.text-success {
  color: green;
  margin-top: 15px;
}

.text-danger {
  color: red;
  margin-top: 15px;
}
</style>
