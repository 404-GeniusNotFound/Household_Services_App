<template>
  <CustomerLayout>
    <div class="summary-container">
      <div class="summary-content">
        <h2 class="section-title">Service Request Summary</h2>
        <p class="status-note">* current statuses</p>
        <div class="chart-container">
          <div v-if="chartData" class="chart-wrapper">
            <Chart :data="chartData" :options="chartOptions" type="bar" />
          </div>
          <p v-else class="loading-message">Loading data...</p>
        </div>
      </div>
    </div>
  </CustomerLayout>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { Chart } from "vue-chartjs";
import CustomerLayout from "./CustomerLayout.vue";
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarController,
  BarElement,
  CategoryScale,
  LinearScale,
} from "chart.js";

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  BarController,
  BarElement,
  CategoryScale,
  LinearScale
);

const chartData = ref(null);
const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false,
    },
    title: {
      display: true,
      text: "Service Requests by Status",
    },
  },
  scales: {
    y: {
      beginAtZero: true,
      ticks: {
        stepSize: 1,
      },
    },
  },
};

onMounted(() => {
  fetchChartData();
});

async function fetchChartData() {
  try {
    const customerId = localStorage.getItem("customerId");
    const response = await axios.get("http://localhost:5000/customer/summary", {
      params: { customer_id: customerId },
    });
    const statusSummary = response.data;
    processChartData(statusSummary);
  } catch (error) {
    console.error("Error fetching chart data:", error);
    alert("Failed to load chart data. Please try again later.");
  }
}

function processChartData(statusSummary) {
  const statuses = [
    "requested",
    "assigned",
    "accepted",
    "rejected",
    "completed",
    "rated",
  ];
  const labels = statuses.map(
    (status) => status.charAt(0).toUpperCase() + status.slice(1)
  );
  const data = statuses.map((status) => statusSummary[status] || 0);

  chartData.value = {
    labels: labels,
    datasets: [
      {
        label: "Service Requests",
        backgroundColor: [
          "#42A5F5",
          "#66BB6A",
          "#FFA726",
          "#AB47BC",
          "#FF7043",
          "#26C6DA",
        ],
        data: data,
      },
    ],
  };
}
</script>

<style scoped>
.summary-container {
  padding: 20px;
  display: flex;
  justify-content: center;
  background-color: #f5f5f5;
}

.summary-content {
  width: 100%;
  max-width: 900px;
  background-color: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.section-title {
  font-size: 24px;
  font-weight: 600;
  color: #333;
  text-align: center;
  margin-bottom: 10px;
}

.chart-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
  margin-top: 20px;
}

.chart-wrapper {
  width: 100%;
  max-width: 700px;
  height: 400px; /* Adjusted height for better visibility */
}

.loading-message {
  text-align: center;
  color: #666;
  font-size: 16px;
  margin-top: 20px;
}

.status-note {
  text-align: center;
  font-size: 14px;
  color: #666;
  margin-top: 5px;
}
</style>
