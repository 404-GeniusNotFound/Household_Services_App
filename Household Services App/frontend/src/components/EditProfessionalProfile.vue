<template>
  <div class="edit-profile-modal">
    <h2 class="modal-title">Edit Profile</h2>
    <form @submit.prevent="editProfile">
      <div class="form-group">
        <label for="full_name" class="form-label">Full Name:</label>
        <input
          type="text"
          v-model="form.full_name"
          class="form-control"
          required
        />
      </div>
      <div class="form-group">
        <label for="address" class="form-label">Address:</label>
        <input
          type="text"
          v-model="form.address"
          class="form-control"
          required
        />
      </div>
      <div class="form-group">
        <label for="pin_code" class="form-label">Pin Code:</label>
        <input
          type="text"
          v-model="form.pin_code"
          class="form-control"
          required
        />
      </div>
      <div class="form-group">
        <label for="phone_number" class="form-label">Phone Number:</label>
        <input
          type="text"
          v-model="form.phone_number"
          class="form-control"
          required
        />
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
    professionalId: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      form: {
        full_name: "",
        address: "",
        pin_code: "",
        phone_number: "",
      },
      message: "",
      error: "",
    };
  },
  mounted() {
    this.loadProfessionalProfile();
  },
  methods: {
    loadProfessionalProfile() {
      axios
        .get(`http://localhost:5000/professionals/${this.professionalId}`)
        .then((response) => {
          this.form = {
            full_name: response.data.full_name,
            address: response.data.address,
            pin_code: response.data.pin_code,
            phone_number: response.data.phone_number,
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
        .put(
          `http://localhost:5000/professionals/${this.professionalId}`,
          this.form
        )
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
.edit-profile-modal {
  background: #fff;
  padding: 20px 30px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  max-width: 400px;
  margin: 0 auto;
}

.modal-title {
  font-size: 22px;
  font-weight: 600;
  color: #333;
  text-align: center;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
}

.form-label {
  font-size: 14px;
  color: #555;
  margin-bottom: 5px;
}

.form-control {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.btn-primary {
  width: 100%;
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
  text-align: center;
  margin-top: 10px;
}

.text-danger {
  color: #dc3545;
  font-size: 14px;
  text-align: center;
  margin-top: 10px;
}
</style>
