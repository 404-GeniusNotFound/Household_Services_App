<template>
  <div class="professional-list-container">
    <table class="professionals-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Name</th>
          <th>Experience (Yrs)</th>
          <th>Service</th>
          <th>Status</th>
          <th>Average Rating</th>
          <th>CV</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="professional in professionals" :key="professional.id">
          <td>{{ professional.id }}</td>
          <td>{{ professional.username }}</td>
          <td>{{ professional.experience }}</td>
          <td>{{ professional.service_name }}</td>
          <td>{{ professional.status }}</td>
          <td>{{ professional.average_rating }}</td>
          <td>
            <a
              v-if="professional.cv_file"
              :href="`http://localhost:5000/download_cv/${professional.cv_file}`"
              target="_blank"
              class="btn btn-info"
            >
              Download CV
            </a>
            <span v-else>N/A</span>
          </td>
          <td>
            <button
              v-if="professional.status !== 'approved'"
              @click="approveProfessional(professional.id)"
              class="btn btn-success"
            >
              Approve
            </button>
            <button
              v-if="professional.status !== 'rejected'"
              @click="rejectProfessional(professional.id)"
              class="btn btn-warning"
            >
              Reject
            </button>
            <button
              @click="deleteProfessional(professional.id)"
              class="btn btn-danger"
            >
              Delete
            </button>
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
      professionals: [],
    };
  },
  mounted() {
    this.fetchProfessionals();
  },
  methods: {
    fetchProfessionals() {
      axios
        .get("http://localhost:5000/professionals")
        .then((response) => {
          this.professionals = response.data;
        })
        .catch((error) => {
          console.error("Error fetching professionals:", error);
        });
    },
    approveProfessional(professionalId) {
      axios
        .patch(`http://localhost:5000/professionals/${professionalId}/approve`)
        .then(() => {
          alert("Professional approved");
          this.fetchProfessionals();
        })
        .catch((error) => {
          console.error("Error approving professional:", error);
        });
    },
    rejectProfessional(professionalId) {
      axios
        .patch(`http://localhost:5000/professionals/${professionalId}/reject`)
        .then(() => {
          alert("Professional rejected");
          this.fetchProfessionals();
        })
        .catch((error) => {
          console.error("Error rejecting professional:", error);
        });
    },
    deleteProfessional(professionalId) {
      axios
        .delete(`http://localhost:5000/professionals/${professionalId}`)
        .then(() => {
          alert("Professional deleted");
          this.fetchProfessionals();
        })
        .catch((error) => {
          console.error("Error deleting professional:", error);
        });
    },
  },
};
</script>

<style scoped>
.professional-list-container {
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

.professionals-table {
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

.btn-warning {
  background-color: #ffc107;
  color: #fff;
}

.btn-danger {
  background-color: #dc3545;
  color: #fff;
}

.btn-info {
  background-color: #17a2b8;
  color: #fff;
}

.btn:hover {
  opacity: 0.9;
}
</style>
