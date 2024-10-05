const fileInput = document.getElementById('fileInput');
const results = document.getElementById('results');
const uploadBtn = document.getElementById('uploadBtn');
const cpuForm = document.getElementById('cpuForm');
const cpuResult = document.getElementById('cpuResult');

// Handle image file upload for defect analysis (Model 1)
uploadBtn.addEventListener('click', () => {
  const files = fileInput.files;
  if (files.length > 0) {
    results.innerHTML = '';
    for (let file of files) {
      processFile(file);
    }
  } else {
    alert("Please upload a file.");
  }
});

// Simulate processing the image file (Model 1)
function processFile(file) {
  const resultItem = document.createElement('div');
  resultItem.className = 'result-item';
  resultItem.innerHTML = `<p>Processing: ${file.name}</p>`;
  
  // Simulate a delay for processing (replace with actual ML model processing)
  setTimeout(() => {
    resultItem.innerHTML = `<p>Completed: ${file.name}</p>`;
    results.appendChild(resultItem);
  }, 2000); // Simulated delay
}

// Handle CPU performance form submission (Model 2)
cpuForm.addEventListener('submit', async (event) => {
  event.preventDefault();

  const data = {
    cores: document.getElementById('cores').value,
    frequency: document.getElementById('frequency').value,
    tdp: document.getElementById('tdp').value,
    dieSize: document.getElementById('dieSize').value,
    transistors: document.getElementById('transistors').value,
    processSize: document.getElementById('processSize').value
  };

  // Simulate API call to the ML model for CPU analysis
  const response = await fetch('/analyze-cpu', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });

  const result = await response.json();

  // Display the CPU Mark result
  cpuResult.innerHTML = `<p>Estimated CPU Mark: ${result.cpuMark.toFixed(2)}</p>`;
});
