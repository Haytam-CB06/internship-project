let mychart;
let jsondata;
let graphCount=0;
function uploadFile() {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];

    if (!file) {
        alert('Please select a file first.');
        return;
    }
    
    var formData = new FormData();
    formData.append("file", file);

    // First upload the file
    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => { throw err; });
        }
        return response.json();
    })
    .then(data => {
        console.log('Upload success:', data);
        alert('File uploaded successfully!');
        
        // Only after successful upload, fetch the graph data
        return fetch('/get_graph_data');
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to get graph data');
        }
        return response.json();
    })
    .then(data => {
        if (data.error) {
            throw new Error(data.error);
        }
        jsondata = data;
        createChart(data, 'bar');
    })
    .catch(error => {
        console.error("Error:", error);
        alert('Error: ' + (error.message || 'Failed to process file'));
    });
}
    function createChart(data, type) {
        const ctx = document.getElementById('myChart').getContext('2d');
        const x=document.getElementById('Xaxis1').value;
        const y=document.getElementById('Yaxis1').value;
        if (!x) {
                alert('Please select your X axis name.');
                return;
            }
            if (!y) {
                alert('Please select your Y axis name.');
                return;
            }
        
       


     mychart = new Chart(ctx, {
            type: type,
            data: {
                labels: data.map(row=>row[x]),
                datasets: [{
                    label:  ` ${y}/${x}`,
                    data: data.map(row=>row[y]),
                    borderWidth: 1
                }]
            },
            options: {
                aspectRatio:1,
      responsive: true,
      scales: type === 'bar' || type === 'line' ? {
        y: { beginAtZero: true }
      } : {}
    }
  });

  chartInstances[id].chart = chart;
}

    function setcharttype(type){
        mychart.destroy();
        createChart(jsondata,type);
    }