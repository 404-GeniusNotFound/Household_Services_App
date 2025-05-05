<template>
  <ProfessionalLayout>
    <h2 class="section-title">Search</h2>
    <ProfessionalSearchBar @on-search="performSearch" />

    <div v-if="searchResults.length > 0" class="results-container">
      <h3 class="results-title">Search Results</h3>
      <table class="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Customer Name</th>
            <th>Contact Phone</th>
            <th>Location</th>
            <th>Date</th>
            <th>Rating</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="result in searchResults" :key="result.id">
            <td>{{ result.id }}</td>
            <td>{{ result.customer_name }}</td>
            <td>{{ result.customer_phone }}</td>
            <td>{{ result.customer_location }}</td>
            <td>{{ result.request_date }}</td>
            <td>{{ result.rating }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <p v-else class="no-results-message">No results found.</p>
  </ProfessionalLayout>
</template>

<script>
import axios from "axios";
import ProfessionalSearchBar from "./ProfessionalSearchBar.vue";
import ProfessionalLayout from "./ProfessionalLayout.vue";

export default {
  components: {
    ProfessionalSearchBar,
    ProfessionalLayout,
  },
  data() {
    return {
      searchResults: [],
    };
  },
  methods: {
    performSearch({ searchQuery, searchType }) {
      const professionalId = localStorage.getItem("professionalId");
      axios
        .get("http://localhost:5000/professional/search", {
          params: {
            query: searchQuery,
            type: searchType,
            professional_id: professionalId,
          },
        })
        .then((response) => {
          this.searchResults = response.data;
        })
        .catch((error) => {
          console.error("Error performing search:", error);
          this.searchResults = [];
          alert("Failed to fetch search results. Please try again later.");
        });
    },
    formatDate(dateString) {
      if (!dateString) return "Not Available";
      const date = new Date(dateString);
      if (isNaN(date)) return "Invalid Date";
      return date.toLocaleString();
    },
  },
};
</script>

<style scoped>
.section-title {
  font-size: 24px;
  font-weight: 600;
  color: #333;
  margin-bottom: 20px;
  text-align: center;
}

.results-container {
  margin-top: 20px;
}

.results-title {
  font-size: 20px;
  font-weight: 600;
  color: #333;
  margin-bottom: 10px;
}

.table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

th,
td {
  padding: 12px;
  border: 1px solid #ddd;
  text-align: left;
}

.no-results-message {
  color: #666;
  font-size: 16px;
  margin-top: 20px;
  text-align: center;
}
</style>
