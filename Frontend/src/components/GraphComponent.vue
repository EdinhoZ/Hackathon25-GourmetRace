<template>
  <div>
      <h3>{{ coinName }} Price Prediction</h3>
      <!-- Plotly chart container -->
      <div ref="plotlyChart" style="height: 400px;"></div>
  </div>
</template>

<script>
// Import Plotly directly from the plotly.js-dist package
import Plotly from 'plotly.js-dist';

export default {
  props: {
    coinName: String // Coin name passed from the parent component
  },
  data() {
    return {
      forecastData: [],
      chartData: [],
      layout: {
        title: "Crypto Future Predictions",
        xaxis: { title: "Date" },
        yaxis: { title: "Predicted Price" },
      }
    };
  },
  methods: {
    async fetchForecast() {
      try {
        const response = await fetch(`http://127.0.0.1:8000/forecast/${this.coinName}/`);
        const data = await response.json();
        this.forecastData = data;

        this.chartData = [{
          x: data.map(item => item.ds),
          y: data.map(item => item.yhat),
          type: "scatter",
          mode: "lines",
          name: `${this.coinName} Predicted Price`
        }];

        this.plotChart();
      } catch (error) {
        console.error("Error fetching forecast:", error);
      }
    },
    plotChart() {
      Plotly.newPlot(this.$refs.plotlyChart, this.chartData, this.layout);
    }
  },
  watch: {
    coinName(newName, oldName) {
      if (newName !== oldName) {
        this.fetchForecast();
      }
    }
  },
  mounted() {
    this.fetchForecast();
  }
};
</script>

<style scoped>
.plotly-chart {
    width: 100%;
    height: 400px;
}
</style>