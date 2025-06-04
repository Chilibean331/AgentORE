fetch('intel_export.csv')
  .then(response => response.text())
  .then(text => {
    const data = text.split('\n').slice(1).map(line => line.split(','));
    const map = L.map('map').setView([36.27, 43.38], 8);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);
    data.forEach(row => {
      const lat = parseFloat(row[6]);
      const lon = parseFloat(row[7]);
      if(!isNaN(lat) && !isNaN(lon)) {
        L.marker([lat, lon]).addTo(map).bindPopup(row[2]);
      }
    });
  });
