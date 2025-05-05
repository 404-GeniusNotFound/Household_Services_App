<template>
  <AdminLayout>
    <div class="dashboard-content">
      <h3 class="section-title">Services</h3>
      <ServiceList />
      <h3 class="section-title">Professionals</h3>
      <ProfessionalList />
      <h3 class="section-title">Service Requests</h3>
      <ServiceRequests />
    </div>
  </AdminLayout>
</template>

<script>
import AdminLayout from "./AdminLayout.vue";
import ServiceList from "./ServiceList.vue";
import ProfessionalList from "./ProfessionalList.vue";
import ServiceRequests from "./ServiceRequests.vue";

export default {
  components: {
    AdminLayout,
    ServiceList,
    ProfessionalList,
    ServiceRequests,
  },
};
</script>

<style scoped>
.dashboard-content {
  padding: 20px;
}

.section-title {
  font-size: 20px;
  font-weight: 600;
  color: #333;
  margin: 20px 0 10px;
}
</style>
