function updateVisualization() {
    const dataset = document.getElementById('datasetSelect').value;
    fetch(`/visualize/data?dataset=${dataset}`)
      .then(response => response.json())
      .then(data => {
        Plotly.newPlot('visualizationCanvas', data.traces, data.layout);
      });
  }
  
  // Initial load if the element exists.
  if (document.getElementById('visualizationCanvas')) {
    updateVisualization();
  }
  