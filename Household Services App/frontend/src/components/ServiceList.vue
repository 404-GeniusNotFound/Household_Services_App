<template>
  <div class="service-list-container">
    <button @click="showAddModal = true" class="btn btn-primary">
      + New Service
    </button>

    <table class="services-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Service Name</th>
          <th>Base Price</th>
          <th>Category</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="service in services" :key="service.id">
          <td>{{ service.id }}</td>
          <td>{{ service.name }}</td>
          <td>₹{{ service.price }}</td>
          <td>{{ service.category }}</td>
          <td>
            <button @click="openEditModal(service)" class="btn btn-secondary">
              Edit
            </button>
            <button @click="deleteService(service.id)" class="btn btn-danger">
              Delete
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <div v-if="showAddModal" class="modal-overlay">
      <div class="modal-content">
        <button @click="closeAddModal" class="close-button">&times;</button>
        <AddService @service-added="fetchServices" @close="closeAddModal" />
      </div>
    </div>

    <div v-if="showEditModal" class="modal-overlay">
      <div class="modal-content">
        <button @click="closeEditModal" class="close-button">&times;</button>
        <EditService
          :service="selectedService"
          @service-edited="fetchServices"
          @close="closeEditModal"
        />
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import AddService from "./AddService.vue";
import EditService from "./EditService.vue";

export default {
  components: {
    AddService,
    EditService,
  },
  data() {
    return {
      services: [],
      showAddModal: false,
      showEditModal: false,
      selectedService: null,
    };
  },
  mounted() {
    this.fetchServices();
  },
  methods: {
    fetchServices() {
      axios
        .get("http://localhost:5000/services")
        .then((response) => {
          this.services = response.data;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    openEditModal(service) {
      this.selectedService = service;
      this.showEditModal = true;
    },
    deleteService(serviceId) {
      axios
        .delete(`http://localhost:5000/services/${serviceId}`)
        .then(() => {
          this.fetchServices();
        })
        .catch((error) => {
          console.error(error);
        });
    },
    closeAddModal() {
      this.showAddModal = false;
    },
    closeEditModal() {
      this.showEditModal = false;
    },
  },
};
</script>

<style scoped>
.service-list-container {
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

.services-table {
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

.btn-primary {
  background-color: #007bff;
  color: #fff;
}

.btn-secondary {
  background-color: #6c757d;
  color: #fff;
}

.btn-danger {
  background-color: #dc3545;
  color: #fff;
}

.btn:hover {
  opacity: 0.9;
}

/* Modal styling */
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
  z-index: 1000;
}

.modal-content {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  width: 400px;
  max-width: 90%;
  box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.2);
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
  color: #333;
}
</style>
