<template>
  <CustomerLayout>
    <div class="dashboard-content">
      <h2 class="section-title">Welcome, {{ customerName }}</h2>

      <h3 class="subsection-title">Looking For?</h3>
      <div class="categories">
        <button
          v-for="category in categories"
          :key="category"
          @click="fetchServicesByCategory(category)"
          class="category-btn"
        >
          {{ category }}
        </button>
      </div>

      <div v-if="services.length" class="services-list">
        <h3 class="subsection-title">Best Packages</h3>
        <table>
          <thead>
            <tr>
              <th>Service Name</th>
              <th>Service Description</th>
              <th>Cost</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="service in services" :key="service.id">
              <td>{{ service.name }}</td>
              <td>{{ service.description }}</td>
              <td>₹{{ service.price }}</td>
              <td>
                <button
                  @click="bookService(service.id)"
                  class="action-btn book-btn"
                >
                  Book
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <h3 class="subsection-title">Service History</h3>
      <table class="history-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Service Name</th>
            <th>Professional Name</th>
            <th>Phone No.</th>
            <th>Status</th>
            <th>Close</th>
            <th>Rate</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="history in serviceHistory" :key="history.id">
            <td>{{ history.id }}</td>
            <td>{{ history.service_name }}</td>
            <td>{{ history.professional_name }}</td>
            <td>{{ history.professional_phone }}</td>
            <td>{{ history.status }}</td>
            <td>
              <button
                v-if="history.status === 'accepted'"
                @click="openPaymentModal(history)"
                class="action-btn pay-close-btn"
              >
                Pay and Close
              </button>
              <span
                v-else-if="
                  history.status === 'completed' || history.status === 'rated'
                "
              >
                Closed
              </span>
            </td>
            <td>
              <button
                v-if="history.status === 'completed'"
                @click="openServiceRating(history.id)"
                class="action-btn rate-btn"
              >
                Rate
              </button>
              <span v-if="history.status === 'rated'">
                Rated: {{ history.rating }}/5
              </span>
            </td>
          </tr>
        </tbody>
      </table>

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

      <div v-if="showServiceRatingModal" class="modal-overlay">
        <div class="modal-content">
          <button @click="closeServiceRating" class="close-button">
            &times;
          </button>
          <ServiceRating
            v-if="showServiceRatingModal"
            :serviceId="currentServiceId"
            @close="closeServiceRating"
          />
        </div>
      </div>

      <!-- Payment Modal -->
      <div v-if="showPaymentModal" class="modal-overlay">
        <div class="modal-content">
          <button @click="closePaymentModal" class="close-button">
            &times;
          </button>
          <PaymentPage
            :service="currentPaymentService"
            @pay="handlePayment"
            @close="closePaymentModal"
          />
        </div>
      </div>
    </div>
  </CustomerLayout>
</template>

<script>
import axios from "axios";
import EditCustomerProfile from "./EditCustomerProfile.vue";
import ServiceRating from "./ServiceRating.vue";
import PaymentPage from "./PaymentPage.vue";
import CustomerLayout from "./CustomerLayout.vue";

export default {
  components: {
    CustomerLayout,
    EditCustomerProfile,
    ServiceRating,
    PaymentPage,
  },
  data() {
    return {
      customerName: "Customer",
      categories: [],
      services: [],
      serviceHistory: [],
      showEditProfileModal: false,
      showServiceRatingModal: false,
      showPaymentModal: false,
      currentPaymentService: null,
      currentServiceId: null,
      customerId: localStorage.getItem("customerId"),
    };
  },
  mounted() {
    this.fetchCustomerName();
    this.fetchServiceHistory();
    this.fetchServiceCategories();
  },
  methods: {
    fetchCustomerName() {
      axios
        .get(`http://localhost:5000/customers/${this.customerId}`)
        .then((response) => {
          this.customerName = response.data.full_name;
        })
        .catch((error) => {
          console.error("Error fetching customer name:", error);
        });
    },
    fetchServiceCategories() {
      axios
        .get("http://localhost:5000/services/categories")
        .then((response) => {
          this.categories = response.data;
        })
        .catch((error) => {
          console.error("Error fetching categories:", error);
        });
    },
    fetchServicesByCategory(category) {
      axios
        .get(`http://localhost:5000/services/category/${category}`)
        .then((response) => {
          this.services = response.data;
        })
        .catch((error) => {
          console.error("Error fetching services:", error);
        });
    },
    bookService(serviceId) {
      axios
        .post("http://localhost:5000/create_request", {
          service_id: serviceId,
          customer_id: this.customerId,
        })
        .then((response) => {
          alert(response.data.message);
          this.fetchServiceHistory();
        })
        .catch((error) => {
          console.error("Error booking service:", error);
        });
    },
    fetchServiceHistory() {
      axios
        .get("http://localhost:5000/customer_history", {
          params: { customer_id: this.customerId },
        })
        .then((response) => {
          this.serviceHistory = response.data;
        })
        .catch((error) => {
          console.error("Error fetching service history:", error);
        });
    },
    openPaymentModal(history) {
      console.log("openPaymentModal called with history:", history);

      if (!history.service_id) {
        console.error("Service ID not found in service history item:", history);
        alert("Unable to process payment. Service details are missing.");
        return;
      }

      axios
        .get(`http://localhost:5000/services/${history.service_id}`)
        .then((response) => {
          console.log("Service details fetched:", response.data);
          this.currentPaymentService = {
            id: history.id,
            name: response.data.name,
            price: response.data.price,
          };
          this.showPaymentModal = true;
        })
        .catch((error) => {
          console.error("Error fetching service details:", error);
          alert("Unable to fetch service details. Please try again.");
        });
    },
    handlePayment(service) {
      console.log("handlePayment called with service:", service);

      axios
        .patch(`http://localhost:5000/service_requests/${service.id}/close`)
        .then((response) => {
          alert(response.data.message);
          this.showPaymentModal = false;
          this.fetchServiceHistory();
        })
        .catch((error) => {
          console.error("Error closing service request:", error);
          alert("Payment failed. Please try again.");
        });
    },
    closePaymentModal() {
      this.showPaymentModal = false;
      this.currentPaymentService = null;
    },
    openServiceRating(serviceId) {
      this.currentServiceId = serviceId;
      this.showServiceRatingModal = true;
    },
    closeServiceRating() {
      this.showServiceRatingModal = false;
      this.fetchServiceHistory();
    },
    logout() {
      axios
        .post("http://localhost:5000/logout")
        .then(() => {
          localStorage.removeItem("customerId");
          this.$router.push({ name: "Login" });
        })
        .catch((error) => {
          console.error("Logout error:", error);
        });
    },
  },
};
</script>

<style scoped>
.dashboard-content {
  padding: 20px;
}

.section-title {
  font-size: 24px;
  font-weight: 600;
  color: #333;
  margin-bottom: 20px;
  text-align: center;
}

.subsection-title {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin-top: 20px;
  text-align: center;
}

.categories {
  display: flex;
  justify-content: center;
  gap: 20px;
  flex-wrap: wrap;
  margin-bottom: 30px;
}

.category-btn {
  width: 120px;
  height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f5f5f5;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  border: 1px solid #ddd;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.category-btn:hover {
  transform: scale(1.05);
  background-color: #ddd;
}

.services-list,
.history-table {
  width: 100%;
  margin-top: 20px;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  padding: 10px;
  text-align: left;
  border: 1px solid #ddd;
}

.action-btn {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  color: #fff;
  font-weight: 600;
}

.book-btn {
  background-color: #28a745;
}

.pay-close-btn {
  background-color: #17a2b8;
}

.close-btn {
  background-color: #dc3545;
}

.rate-btn {
  background-color: #ffc107;
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
