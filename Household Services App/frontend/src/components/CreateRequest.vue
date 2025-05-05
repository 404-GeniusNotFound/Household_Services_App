<template>
  <div>
    <h2>Create Service Request</h2>
    <form @submit.prevent="createRequest">
      <div class="form-group">
        <label for="service_id">Service ID:</label>
        <input
          type="number"
          v-model="service_id"
          class="form-control"
          required
        />
      </div>
      <div class="form-group">
        <label for="customer_id">Customer ID:</label>
        <input
          type="number"
          v-model="customer_id"
          class="form-control"
          required
        />
      </div>
      <div class="form-group">
        <label for="remarks">Remarks:</label>
        <input type="text" v-model="remarks" class="form-control" />
      </div>
      <button type="submit" class="btn btn-primary">Create Request</button>
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
      service_id: "",
      customer_id: "",
      remarks: "",
      message: "",
      error: "",
    };
  },
  methods: {
    createRequest() {
      axios
        .post("http://localhost:5000/create_request", {
          service_id: this.service_id,
          customer_id: this.customer_id,
          remarks: this.remarks,
        })
        .then((response) => {
          this.message = response.data.message;
          this.error = "";
          this.resetForm();
        })
        .catch((error) => {
          this.error = error.response?.data?.error || "An error occurred.";
          this.message = "";
        });
    },
    resetForm() {
      this.service_id = "";
      this.customer_id = "";
      this.remarks = "";
    },
  },
};
</script>

<style scoped>
/* Basic styling for form layout and messages */
.form-group {
  margin-bottom: 10px;
}
.btn {
  margin-top: 10px;
}
.text-success {
  color: green;
  margin-top: 10px;
}
.text-danger {
  color: red;
  margin-top: 10px;
}
</style>
