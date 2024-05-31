import Chart from 'chart.js/auto';

$(() => {
  /** RENT REVENUE */
  // Get the current year
  const currentYear = new Date().getFullYear();

  // Generate an array of the last 10 years
  const years = Array.from({ length: 10 }, (_, i) => currentYear - i);

  // Create a dropdown option for each year
  const rentInvoiceYearSelect = document.getElementById('rentInvoiceYearSelect');
  years.forEach((year) => {
    const option = document.createElement('option');
    option.value = year;
    option.text = year;
    rentInvoiceYearSelect?.appendChild(option);
  });

  const rentInvoiceRevenueCtx = document.getElementById('rent-invoice-revenue-chart')?.getContext('2d');
  if (!rentInvoiceRevenueCtx) {
    return;
  }
  // Initialize the chart with empty data
  const rentInvoiceRevenueChart = new Chart(rentInvoiceRevenueCtx, {
    type: 'line',
    data: {
      labels: [],
      datasets: [{
        label: 'Total Revenue',
        data: [],
        fill: false,
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1,
      }],
    },
    options: {
      scales: {
        x: {
          beginAtZero: true,
        },
        y: {
          beginAtZero: true,
        },
      },
    },
  });

  $('#rentInvoiceYearSelect').on('change', () => {
    const year = $('#rentInvoiceYearSelect').val();
    $.getJSON(`/dashboard/rent-invoice-revenue/${year}`, (data) => {
      // Update the chart data
      rentInvoiceRevenueChart.data.labels = data.labels;
      rentInvoiceRevenueChart.data.datasets[0].data = data.data;

      // Re-render the chart
      rentInvoiceRevenueChart.update();
    });
  });

  // Trigger the change event to load the chart for the initially selected year
  $('#rentInvoiceYearSelect').trigger('change');

  /** SELL REVENUE */
  // Create a dropdown option for each year
  const sellInvoiceYearSelect = document.getElementById('sellInvoiceYearSelect');
  if (!sellInvoiceYearSelect) {
    return;
  }

  years.forEach((year) => {
    const option = document.createElement('option');
    option.value = year;
    option.text = year;
    sellInvoiceYearSelect?.appendChild(option);
  });

  const topSellingToolsCtx = document.getElementById('top-selling-tools-chart').getContext('2d');
  const topSellingToolsChart = new Chart(topSellingToolsCtx, {
    type: 'bar',
    data: {
      labels: [],
      datasets: [{
        label: 'Total Revenue',
        data: [],
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        borderColor: 'rgb(75, 192, 192)',
        borderWidth: 1,
      }],
    },
    options: {
      scales: {
        y: {
          beginAtZero: true,
        },
      },
    },
  });

  $('#sellInvoiceYearSelect').on('change', () => {
    const year = $('#sellInvoiceYearSelect').val();
    $.getJSON(`/dashboard/top-selling-tools/${year}`, (data) => {
      // Update the chart data
      topSellingToolsChart.data.labels = data.labels;
      topSellingToolsChart.data.datasets[0].data = data.data;

      // Re-render the chart
      topSellingToolsChart.update();
    });
  });

  $('#sellInvoiceYearSelect').trigger('change');

  /** MACHINE STATUS COUNT */
  const machineStatusCountCtx = document.getElementById('machine-status-count-chart').getContext('2d');
  if (!machineStatusCountCtx) {
    return;
  }

  let machineStatusCountChart;

  // Fetch the machine status counts from your server
  $.getJSON('/dashboard/machine-status-count/', (machineStatusCounts) => {
    if (machineStatusCountChart) {
      machineStatusCountChart.destroy();
    }

    machineStatusCountChart = new Chart(machineStatusCountCtx, {
      type: 'doughnut',
      data: {
        labels: machineStatusCounts.labels,
        datasets: [{
          label: 'Machine Status Count',
          data: machineStatusCounts.data,
          backgroundColor: [
            'rgba(255, 99, 132, 0.2)',
            'rgba(54, 162, 235, 0.2)',
            'rgba(255, 206, 86, 0.2)',
          ],
          borderColor: [
            'rgba(255, 99, 132, 1)',
            'rgba(54, 162, 235, 1)',
            'rgba(255, 206, 86, 1)',
          ],
          borderWidth: 1,
        }],
      },
    });
  });

  /** RENT INVOICE STATUS COUNT */
  const rentInvoiceStatusCountCtx = document.getElementById('rent-invoice-status-count-chart')?.getContext('2d');
  if (!rentInvoiceStatusCountCtx) {
    return;
  }

  let rentInvoiceStatusCountChart;
  $.getJSON('/dashboard/rent-invoice-status-count/', (rentInvoiceStatusCounts) => {
    if (rentInvoiceStatusCountChart) {
      rentInvoiceStatusCountChart.destroy();
    }

    rentInvoiceStatusCountChart = new Chart(rentInvoiceStatusCountCtx, {
      type: 'bar',
      data: {
        labels: rentInvoiceStatusCounts.labels,
        datasets: [{
          label: 'Rent Invoice Status Count',
          data: rentInvoiceStatusCounts.data,
          backgroundColor: rentInvoiceStatusCounts.labels.map((label, index) => {
            // Use a different color for each bar
            const colors = ['rgba(75, 192, 192, 0.2)', 'rgba(255, 99, 132, 0.2)', 'rgba(255, 206, 86, 0.2)'];
            return colors[index % colors.length];
          }),
          borderColor: rentInvoiceStatusCounts.labels.map((label, index) => {
            // Use a different color for each bar
            const colors = ['rgb(75, 192, 192)', 'rgb(255, 99, 132)', 'rgb(255, 206, 86)'];
            return colors[index % colors.length];
          }),
          borderWidth: 1,
        }],
      },
      options: {
        scales: {
          y: {
            beginAtZero: true,
          },
        },
      },
    });
  });

  /** TOP 10 SPENDING SCHOOL CHART */
  const topSpendingSchoolCtx = document.getElementById('top-10-spending-school-chart')?.getContext('2d');
  if (!topSpendingSchoolCtx) {
    return;
  }

  let topSpendingSchoolChart;

  $.getJSON('/dashboard/top-10-spending-school/', (topSpendingSchool) => {
    if (topSpendingSchoolChart) {
      topSpendingSchoolChart.destroy();
    }

    topSpendingSchoolChart = new Chart(topSpendingSchoolCtx, {
      type: 'bar',
      data: {
        labels: topSpendingSchool.labels,
        datasets: [{
          label: 'Total Revenue',
          data: topSpendingSchool.data,
          backgroundColor: 'rgba(75, 192, 192, 0.2)',
          borderColor: 'rgb(75, 192, 192)',
          borderWidth: 1,
        }],
      },
      options: {
        scales: {
          y: {
            beginAtZero: true,
          },
        },
      },
    });
  });
});
