<template>
  <ProfessionalLayout
    @show-profile-modal="showEditProfessionalProfileModal = true"
  >
    <h2 class="section-title">Service Requests</h2>
    <table class="table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Customer Name</th>
          <th>Contact Phone</th>
          <th>Location</th>
          <th>Status</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="service in serviceRequests" :key="service.id">
          <td>{{ service.id }}</td>
          <td>{{ service.customer_name || "N/A" }}</td>
          <td>{{ service.customer_phone || "N/A" }}</td>
          <td>{{ service.customer_location || "N/A" }}</td>
          <td>{{ service.status }}</td>
          <td>
            <button
              v-if="service.status === 'assigned'"
              @click="updateServiceStatus(service.id, 'accepted')"
              class="btn btn-success"
            >
              Accept
            </button>
            <button
              v-if="service.status === 'assigned'"
              @click="updateServiceStatus(service.id, 'rejected')"
              class="btn btn-danger"
            >
              Reject
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <h2 class="section-title">Closed Services</h2>
    <table class="table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Customer Name</th>
          <th>Location</th>
          <th>Date</th>
          <th>Rating</th>
          <th>Review</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="service in closedServices" :key="service.id">
          <td>{{ service.id }}</td>
          <td>{{ service.customer_name || "N/A" }}</td>
          <td>{{ service.customer_location || "N/A" }}</td>
          <td>{{ service.completion_date || "Not Available" }}</td>
          <td>{{ service.rating || "N/A" }}</td>
          <td>{{ service.remarks || "No Review" }}</td>
        </tr>
      </tbody>
    </table>

    <div v-if="showEditProfessionalProfileModal" class="modal-overlay">
      <div class="modal-content">
        <button
          @click="showEditProfessionalProfileModal = false"
          class="close-button"
        >
          &times;
        </button>
        <EditProfessionalProfile
          :professionalId="professionalId"
          @close="showEditProfessionalProfileModal = false"
        />
      </div>
    </div>
  </ProfessionalLayout>
</template>

<script>
import axios from "axios";
import EditProfessionalProfile from "./EditProfessionalProfile.vue";
import ProfessionalLayout from "./ProfessionalLayout.vue";

export default {
  components: {
    EditProfessionalProfile,
    ProfessionalLayout,
  },
  data() {
    return {
      professionalId: localStorage.getItem("professionalId"),
      serviceRequests: [],
      closedServices: [],
      showEditProfessionalProfileModal: false,
    };
  },
  mounted() {
    this.fetchServiceRequests();
  },
  methods: {
    fetchServiceRequests() {
      axios
        .get("http://localhost:5000/service_requests", {
          withCredentials: true,
        })
        .then((response) => {
          const allRequests = response.data;
          this.serviceRequests = allRequests.filter(
            (req) =>
              req.professional_id == this.professionalId &&
              (req.status === "assigned" || req.status === "accepted")
          );
          this.closedServices = allRequests.filter(
            (req) =>
              req.status === "completed" ||
              (req.status === "rated" &&
                req.professional_id == this.professionalId)
          );
        })
        .catch((error) => {
          console.error("Error fetching service requests:", error);
        });
    },
    updateServiceStatus(requestId, status) {
      axios
        .patch(
          `http://localhost:5000/service_requests/${requestId}/status`,
          { status },
          { withCredentials: true }
        )
        .then((response) => {
          alert(response.data.message);
          const serviceToUpdate = this.serviceRequests.find(
            (service) => service.id === requestId
          );
          if (serviceToUpdate) {
            serviceToUpdate.status = status;
          }
        })
        .catch((error) => {
          console.error(
            `Error updating status for request ${requestId}:`,
            error
          );
          alert("An error occurred while updating the status.");
        });
    },
    formatDate(dateString) {
      if (!dateString) return null;
      const date = new Date(dateString);
      return date.toLocaleString();
    },
  },
};
</script>

<style scoped>
.section-title {
  font-size: 20px;
  font-weight: 600;
  color: #333;
  margin-bottom: 15px;
}

.table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 30px; /* Add extra space between tables */
}

th,
td {
  padding: 12px; /* Increased padding for better readability */
  border: 1px solid #ddd;
  text-align: left;
}

.btn-success {
  background-color: #28a745;
  color: #fff;
  padding: 5px 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-danger {
  background-color: #dc3545;
  color: #fff;
  padding: 5px 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-content {
  background: #fff;
  padding: 20px;
  border-radius: 5px;
  width: 400px;
  position: relative;
}

.close-button {
  background: transparent;
  border: none;
  font-size: 1.5em;
  position: absolute;
  top: 10px;
  right: 10px;
  cursor: pointer;
}
</style>
