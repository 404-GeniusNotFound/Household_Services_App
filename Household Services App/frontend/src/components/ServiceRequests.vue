<template>
  <div class="service-requests-container">
    <table class="requests-table">
      <thead>
        <tr>
          <th>Request ID</th>
          <th>Service</th>
          <th>Customer</th>
          <th>Professional</th>
          <th>Status</th>
          <th>Remarks</th>
          <th>Request Date</th>
          <th>Completion Date</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="request in requests" :key="request.id">
          <td>{{ request.id }}</td>
          <td>{{ getServiceName(request.service_id) }}</td>
          <td>{{ request.customer_name }}</td>
          <td>{{ request.professional_name || "N/A" }}</td>
          <td>{{ request.status }}</td>
          <td>{{ request.remarks }}</td>
          <td>{{ request.request_date }}</td>
          <td>{{ request.completion_date || "Not completed" }}</td>
          <td>
            <div v-if="request.status === 'requested'">
              <select
                v-model="selectedProfessional[request.id]"
                class="form-control"
              >
                <option value="" disabled>Select a Professional</option>
                <option
                  v-for="professional in getProfessionalsForRequest(request)"
                  :key="professional.id"
                  :value="professional.id"
                >
                  {{ professional.username }}
                </option>
              </select>

              <button
                @click="assignProfessional(request.id)"
                class="btn btn-success btn-sm"
              >
                Assign Professional
              </button>
            </div>
            <div v-else-if="request.status === 'accepted'">
              <button
                @click="closeRequest(request.id)"
                class="btn btn-primary btn-sm"
              >
                Mark as Completed
              </button>
            </div>
            <div v-else>
              <span class="na-text">----------------</span>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      requests: [],
      services: [],
      customers: [],
      professionals: [],
      selectedProfessional: {},
      serviceIdToCategory: {},
    };
  },
  mounted() {
    this.fetchRequests();
    this.fetchServices();
    this.fetchApprovedProfessionals();
  },
  methods: {
    fetchRequests() {
      axios
        .get("http://localhost:5000/service_requests")
        .then((response) => {
          this.requests = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    fetchServices() {
      axios
        .get("http://localhost:5000/services")
        .then((response) => {
          this.services = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    fetchApprovedProfessionals() {
      axios
        .get("http://localhost:5000/professionals/approved")
        .then((response) => {
          this.professionals = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    getServiceName(serviceId) {
      const service = this.services.find((s) => s.id === serviceId);
      return service ? service.name : "Unknown Service";
    },
    formatDate(dateString) {
      if (!dateString) return null;
      const date = new Date(dateString);
      return date.toLocaleString();
    },
    getProfessionalsForRequest(request) {
      const service = this.services.find((s) => s.id === request.service_id);
      const category = service ? service.category : null;
      if (!category) return [];
      return this.professionals.filter(
        (p) =>
          p.service_name &&
          p.service_name.toLowerCase() === category.toLowerCase()
      );
    },
    assignProfessional(requestId) {
      const professionalId = this.selectedProfessional[requestId];
      if (!professionalId) {
        alert("Please select a professional to assign.");
        return;
      }
      axios
        .patch(`http://localhost:5000/assign_professional/${requestId}`, {
          professional_id: professionalId,
        })
        .then((response) => {
          alert(response.data.message);
          this.fetchRequests();
        })
        .catch((error) => {
          console.log(error);
        });
    },
    closeRequest(requestId) {
      axios
        .patch(`http://localhost:5000/service_requests/${requestId}/close`)
        .then((response) => {
          alert(response.data.message);
          this.fetchRequests();
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
};
</script>

<style scoped>
.service-requests-container {
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
}

.title {
  font-size: 24px;
  font-weight: 600;
  color: #333;
  margin-bottom: 20px;
}

.requests-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
  font-size: 16px;
}

th,
td {
  padding: 12px;
  border: 1px solid #ddd;
  text-align: left;
}

th {
  background-color: #f0f0f0;
  font-weight: 600;
  color: #555;
}

.btn {
  padding: 8px 12px;
  font-size: 14px;
  margin-right: 5px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-success {
  background-color: #28a745;
  color: #fff;
}

.btn-primary {
  background-color: #007bff;
  color: #fff;
}

.na-text {
  color: #888;
  font-size: 14px;
}

.btn:hover {
  opacity: 0.9;
}

.form-control {
  width: 100%;
  padding: 8px;
  font-size: 14px;
  margin-bottom: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
</style>
