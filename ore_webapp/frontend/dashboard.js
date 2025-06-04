async function loadData() {
  const res = await fetch('/dashboard/mission-data');
  if (!res.ok) return;
  const data = await res.json();

  // Quick stats
  const stats = document.getElementById('stats');
  stats.innerText = `Active contacts: ${data.active_contacts} | Last report: ${data.last_report || 'N/A'} | Open incidents: ${data.open_incidents}`;

  // Map overlays
  const map = L.map('map').setView([36.27, 43.38], 8);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
  }).addTo(map);
  (data.map || []).forEach(p => {
    L.marker([p.lat, p.lon]).addTo(map).bindPopup(p.title);
  });

  // Time series chart
  const labels = data.time_series.map(i => i[0]);
  const counts = data.time_series.map(i => i[1]);
  const ctx = document.getElementById('chart').getContext('2d');
  window.chart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{ label: 'Incidents', data: counts, borderColor: 'red' }]
    },
    options: { responsive: true }
  });
}

function exportChartImage() {
  html2canvas(document.getElementById('chart')).then(canvas => {
    const link = document.createElement('a');
    link.download = 'chart.png';
    link.href = canvas.toDataURL();
    link.click();
  });
}

function exportChartPDF() {
  html2canvas(document.getElementById('chart')).then(canvas => {
    const imgData = canvas.toDataURL('image/png');
    const { jsPDF } = window.jspdf;
    const pdf = new jsPDF();
    pdf.addImage(imgData, 'PNG', 10, 10, 180, 100);
    pdf.save('chart.pdf');
  });
}

document.getElementById('export-img').addEventListener('click', exportChartImage);
document.getElementById('export-pdf').addEventListener('click', exportChartPDF);

loadData();

