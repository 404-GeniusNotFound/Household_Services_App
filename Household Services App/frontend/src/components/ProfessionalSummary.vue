<template>
  <ProfessionalLayout>
    <div class="summary-content">
      <h2 class="section-title">Professional Summary</h2>
      <div class="chart-section">
        <div class="chart-container">
          <h3>Reviews/Ratings</h3>
          <Chart
            v-if="ratingChartData"
            :data="ratingChartData"
            :options="donutOptions"
            type="doughnut"
          />
          <p v-else>Loading ratings data...</p>
        </div>
        <div class="chart-container">
          <h3>Service Requests</h3>
          <p class="status-note">* current statuses</p>
          <Chart
            v-if="statusChartData"
            :data="statusChartData"
            :options="barOptions"
            type="bar"
          />
          <p v-else>Loading service requests data...</p>
        </div>
      </div>
    </div>
  </ProfessionalLayout>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { Chart } from "vue-chartjs";
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  DoughnutController,
  ArcElement,
  BarController,
  BarElement,
  CategoryScale,
  LinearScale,
} from "chart.js";
import ProfessionalLayout from "./ProfessionalLayout.vue";

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  DoughnutController,
  ArcElement,
  BarController,
  BarElement,
  CategoryScale,
  LinearScale
);

const ratingChartData = ref(null);
const statusChartData = ref(null);

const donutOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: "top",
    },
    title: {
      display: true,
      text: "Ratings Distribution",
    },
  },
};

const barOptions = {
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
    const professionalId = localStorage.getItem("professionalId");
    const response = await axios.get(
      "http://localhost:5000/professional/summary",
      { params: { professional_id: professionalId } }
    );
    const { status_summary, ratings_summary } = response.data;
    processRatingData(ratings_summary);
    processStatusData(status_summary);
  } catch (error) {
    console.error("Error fetching chart data:", error);
    alert("Failed to load chart data. Please try again later.");
  }
}

function processRatingData(ratingsSummary) {
  const labels = Object.keys(ratingsSummary).map((rating) => `${rating} Star`);
  const data = Object.values(ratingsSummary);

  ratingChartData.value = {
    labels: labels,
    datasets: [
      {
        label: "Ratings",
        backgroundColor: [
          "#66BB6A",
          "#FFA726",
          "#42A5F5",
          "#FF7043",
          "#AB47BC",
        ],
        data: data,
      },
    ],
  };
}

function processStatusData(statusSummary) {
  const labels = [
    "Assigned",
    "Closed",
    "Rejected",
    "Accepted",
    "Completed",
    "Rated",
  ];
  const data = [
    statusSummary["assigned"],
    statusSummary["closed"],
    statusSummary["rejected"],
    statusSummary["accepted"],
    statusSummary["completed"],
    statusSummary["rated"],
  ];

  statusChartData.value = {
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
.summary-content {
  padding: 20px;
}

.section-title {
  font-size: 24px;
  font-weight: 600;
  color: #333;
  margin-bottom: 20px;
  text-align: center;
}

.chart-section canvas {
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  max-height: 450px;
  margin-top: 20px;
}

.chart-container canvas {
  width: 100%;
  max-height: 400px;
  margin-top: 20px;
  background-color: #fff;
  padding: 10px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
</style>
