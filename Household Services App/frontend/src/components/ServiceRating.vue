<template>
  <div class="service-rating-modal">
    <h2>Service Remarks - Request ID: {{ serviceId }}</h2>

    <div class="form-group">
      <label>Service Name:</label>
      <input type="text" v-model="serviceName" class="form-control" disabled />
    </div>

    <div class="form-group">
      <label>Completion Date:</label>
      <input
        type="text"
        v-model="completionDate"
        class="form-control"
        disabled
      />
    </div>

    <div class="form-group">
      <label>Professional Name:</label>
      <input
        type="text"
        v-model="professionalName"
        class="form-control"
        disabled
      />
    </div>

    <div class="form-group">
      <label>Service Rating:</label>
      <select v-model="rating" class="form-control">
        <option value="" disabled>Select Rating</option>
        <option v-for="n in 5" :key="n" :value="n">{{ n }}</option>
      </select>
    </div>

    <div class="form-group">
      <label>Remarks (if any):</label>
      <textarea v-model="remarks" class="form-control"></textarea>
    </div>

    <div class="button-group">
      <button @click="submitRating" class="btn btn-success">Submit</button>
      <button @click="$emit('close')" class="btn btn-secondary">Close</button>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  props: ["serviceId"],
  data() {
    return {
      serviceName: "",
      description: "",
      completionDate: "",
      professionalName: "",
      contactNumber: "",
      rating: "",
      remarks: "",
    };
  },
  mounted() {
    this.loadServiceDetails();
  },
  methods: {
    loadServiceDetails() {
      axios
        .get(`http://localhost:5000/service_requests/${this.serviceId}`)
        .then((response) => {
          const data = response.data;
          this.serviceName = data.service_name;
          this.description = data.description;
          this.completionDate = data.completion_date;
          this.professionalName = data.professional_name;
          this.contactNumber = data.phone_no;
        })
        .catch((error) => {
          console.error("Error loading service details:", error);
        });
    },
    submitRating() {
      if (!this.rating) {
        alert("Please select a rating before submitting.");
        return;
      }

      const payload = {
        rating: this.rating,
        remarks: this.remarks,
      };
      axios
        .post(`http://localhost:5000/review_request/${this.serviceId}`, payload)
        .then((response) => {
          alert(response.data.message);
          this.$emit("close");
        })
        .catch((error) => {
          console.error(
            "Error submitting rating:",
            error.response?.data || error
          );
        });
    },
  },
};
</script>

<style scoped>
.service-rating-modal {
  max-width: 500px;
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

.btn-success {
  background-color: #28a745;
  color: #fff;
}

.btn-success:hover {
  background-color: #218838;
}

.btn-secondary {
  background-color: #6c757d;
  color: #fff;
}

.btn-secondary:hover {
  background-color: #5a6268;
}
</style>
