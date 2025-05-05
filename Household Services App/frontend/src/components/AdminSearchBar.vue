<template>
  <div class="search-container">
    <select v-model="searchType" class="search-select">
      <option value="service">Services</option>
      <option value="customer">Customers</option>
      <option value="professional">Professionals</option>
      <option value="service_request">Service Requests</option>
    </select>
    <input
      type="text"
      v-model="searchQuery"
      placeholder="Enter search text"
      class="search-input"
    />
    <button @click="handleSearch" class="btn btn-primary">Search</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      searchQuery: "",
      searchType: "service",
    };
  },
  methods: {
    handleSearch() {
      this.$emit("on-search", {
        searchQuery: this.searchQuery,
        searchType: this.searchType,
      });
    },
  },
};
</script>

<style scoped>
.search-container {
  display: flex;
  gap: 10px;
  align-items: center;
  margin: 20px 0;
  padding: 10px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background-color: #f9f9f9;
  box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
}

.search-select {
  padding: 8px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 4px;
  outline: none;
}

.search-input {
  padding: 8px;
  font-size: 16px;
  width: 250px;
  border: 1px solid #ccc;
  border-radius: 4px;
  outline: none;
}

.btn-primary {
  padding: 8px 12px;
  font-size: 16px;
  font-weight: 600;
  color: #fff;
  background-color: #007bff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn-primary:hover {
  background-color: #0056b3;
}
</style>
