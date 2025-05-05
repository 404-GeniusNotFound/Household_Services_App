<template>
  <CustomerLayout>
    <div class="search-content">
      <h2 class="section-title">Search</h2>
      <CustomerSearchBar @on-search="performSearch" />

      <div
        v-if="searchType === 'services' && searchResults.length > 0"
        class="results-section"
      >
        <h3 class="subsection-title">Available Services</h3>
        <table class="results-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Description</th>
              <th>Price</th>
              <th>Category</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="service in searchResults" :key="service.id">
              <td>{{ service.id }}</td>
              <td>{{ service.name }}</td>
              <td>{{ service.description }}</td>
              <td>{{ service.price }}</td>
              <td>{{ service.category }}</td>
              <td>
                <button @click="bookService(service.id)" class="action-btn">
                  Book
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div
        v-if="searchType === 'service_requests' && searchResults.length > 0"
        class="results-section"
      >
        <h3 class="subsection-title">Service Request History</h3>
        <table class="results-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Service Name</th>
              <th>Professional Name</th>
              <th>Phone No.</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="request in searchResults" :key="request.id">
              <td>{{ request.id }}</td>
              <td>{{ request.service_name }}</td>
              <td>{{ request.professional_name }}</td>
              <td>{{ request.phone_no }}</td>
              <td>{{ request.status }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <p
        v-else-if="searchResults.length === 0 && !loading"
        class="no-results-message"
      >
        No results found.
      </p>
      <p v-if="loading" class="loading-message">Loading...</p>
    </div>
  </CustomerLayout>
</template>

<script>
import axios from "axios";
import CustomerSearchBar from "./CustomerSearchBar.vue";
import CustomerLayout from "./CustomerLayout.vue";

export default {
  components: { CustomerSearchBar, CustomerLayout },
  data() {
    return {
      searchResults: [],
      searchType: "services",
      loading: false,
    };
  },
  methods: {
    performSearch({ searchQuery, searchType }) {
      this.searchType = searchType;
      const customerId = localStorage.getItem("customerId");
      this.loading = true;

      const endpoint =
        searchType === "services"
          ? "/customer/search/services"
          : "/customer/search/service-requests";

      axios
        .get(`http://localhost:5000${endpoint}`, {
          params: {
            query: searchQuery,
            ...(searchType === "service_requests" && {
              customer_id: customerId,
            }),
          },
        })
        .then((response) => {
          this.searchResults = response.data;
        })
        .catch((error) => {
          console.error("Error performing search:", error);
          this.searchResults = [];
        })
        .finally(() => {
          this.loading = false;
        });
    },
    bookService(serviceId) {
      const customerId = localStorage.getItem("customerId");
      axios
        .post("http://localhost:5000/create_request", {
          service_id: serviceId,
          customer_id: customerId,
        })
        .then((response) => {
          alert(response.data.message);
        })
        .catch((error) => {
          console.error("Error booking service:", error);
        });
    },
  },
};
</script>

<style scoped>
.search-content {
  padding: 20px;
  background-color: #f5f5f5;
  border-radius: 8px;
}

.section-title {
  font-size: 24px;
  font-weight: 600;
  color: #333;
  text-align: center;
  margin-bottom: 20px;
}

.subsection-title {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin-top: 20px;
  text-align: left;
}

.results-section {
  margin-top: 20px;
}

.results-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

th,
td {
  border: 1px solid #ddd;
  padding: 10px;
  text-align: center;
}

.action-btn {
  padding: 8px 12px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.action-btn:hover {
  background-color: #0056b3;
}

.no-results-message,
.loading-message {
  text-align: center;
  color: #666;
  font-size: 16px;
  margin-top: 20px;
}
</style>
