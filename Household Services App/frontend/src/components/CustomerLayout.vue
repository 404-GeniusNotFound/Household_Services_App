<template>
  <div class="customer-dashboard">
    <nav class="sidebar">
      <p class="welcome-message">Welcome, {{ customerName }}</p>
      <router-link to="/customer-dashboard" class="nav-link">Home</router-link>
      <router-link to="/customer/search" class="nav-link">Search</router-link>
      <router-link to="/customer-summary" class="nav-link">Summary</router-link>
      <a href="#" @click.prevent="logout" class="nav-link logout-link">
        Logout
      </a>
      <button @click="showEditProfileModal = true" class="profile-btn">
        Edit Profile
      </button>
    </nav>

    <div class="content">
      <slot></slot>
    </div>

    <div v-if="showEditProfileModal" class="modal-overlay">
      <div class="modal-content">
        <button @click="showEditProfileModal = false" class="close-button">
          &times;
        </button>
        <EditCustomerProfile
          :customerId="customerId"
          @profile-updated="fetchCustomerName"
          @close="showEditProfileModal = false"
        />
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import EditCustomerProfile from "./EditCustomerProfile.vue";

export default {
  components: {
    EditCustomerProfile,
  },
  data() {
    return {
      customerName: localStorage.getItem("customerFullName") || "Customer",
      showEditProfileModal: false,
      customerId: localStorage.getItem("customerId"),
    };
  },
  methods: {
    fetchCustomerName() {
      axios
        .get(`http://localhost:5000/customers/${this.customerId}`)
        .then((response) => {
          this.customerName = response.data.full_name;
          localStorage.setItem("customerFullName", response.data.full_name);
        })
        .catch((error) => {
          console.error("Error fetching customer name:", error);
        });
    },
    logout() {
      axios
        .post("http://localhost:5000/logout")
        .then(() => {
          localStorage.removeItem("customerId");
          localStorage.removeItem("customerFullName");
          this.$router.push({ name: "Login" });
        })
        .catch((error) => {
          console.error("Logout error:", error);
          alert("An error occurred while logging out.");
        });
    },
  },
  mounted() {
    this.fetchCustomerName();
  },
};
</script>

<style scoped>
.customer-dashboard {
  display: flex;
}

.sidebar {
  width: 200px;
  padding: 20px;
  background-color: #333;
  color: #fff;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.welcome-message {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 20px;
}

.nav-link {
  color: #fff;
  text-decoration: none;
  padding: 10px 0;
  font-size: 16px;
  width: 100%;
  text-align: left;
}

.nav-link:hover {
  background-color: #444;
  padding-left: 10px;
  transition: 0.3s;
}

.logout-link {
  color: #ff4d4f;
  margin-top: auto;
}

.content {
  flex: 1;
  padding: 20px;
  background-color: #f5f5f5;
}

.profile-btn {
  padding: 10px;
  margin-top: 20px;
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
  font-size: 16px;
  width: 100%;
  text-align: left;
}

.profile-btn:hover {
  background-color: #0056b3;
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
}

.modal-content {
  background: #fff;
  padding: 20px;
  border-radius: 5px;
  width: 400px;
  max-width: 90%;
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
