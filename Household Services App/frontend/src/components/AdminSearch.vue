<template>
  <AdminLayout>
    <h2 class="section-title">Search</h2>
    <SearchBar @on-search="performSearch" />

    <div v-if="searchResults.length > 0" class="results-container">
      <h3>Search Results for {{ searchType }}</h3>
      <table class="results-table">
        <thead>
          <tr>
            <th v-for="header in tableHeaders" :key="header">
              {{ formatHeader(header) }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="result in searchResults" :key="result.id">
            <td v-for="header in tableHeaders" :key="header">
              {{ result[header] !== undefined ? result[header] : "N/A" }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <p v-else>No results found.</p>
  </AdminLayout>
</template>

<script>
import AdminLayout from "./AdminLayout.vue";
import SearchBar from "./AdminSearchBar.vue";
import axios from "axios";

export default {
  components: {
    AdminLayout,
    SearchBar,
  },
  data() {
    return {
      searchResults: [],
      searchType: "",
      tableHeaders: [],
    };
  },
  methods: {
    performSearch({ searchQuery, searchType }) {
      this.searchType = searchType;

      axios
        .get(`http://localhost:5000/search`, {
          params: { query: searchQuery, type: searchType },
        })
        .then((response) => {
          this.searchResults = response.data;

          if (this.searchResults.length > 0) {
            this.tableHeaders = Object.keys(this.searchResults[0]);
            this.tableHeaders.sort((a, b) =>
              a === "id" ? -1 : b === "id" ? 1 : 0
            );
          }
        })
        .catch((error) => {
          console.error("Error performing search:", error);
          this.searchResults = [];
        });
    },
    formatHeader(header) {
      return header
        .replace(/_/g, " ")
        .replace(/\b\w/g, (char) => char.toUpperCase());
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

.results-table {
  width: 100%;
  border-collapse: collapse;
}

.results-table th,
.results-table td {
  padding: 10px;
  border: 1px solid #ddd;
  text-align: left;
}

.results-table th {
  background-color: #f0f0f0;
  font-weight: 600;
  color: #555;
}

.results-table td {
  font-size: 14px;
}
</style>
