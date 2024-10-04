const fileInput = document.getElementById('fileInput');
const results = document.getElementById('results');
const uploadBtn = document.getElementById('uploadBtn');

// Handle file upload
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

// Simulate processing the file and displaying the result
function processFile(file) {
  const resultItem = document.createElement('div');
  resultItem.className = 'result-item';
  resultItem.innerHTML = `<p>Processing: ${file.name}</p>`;
  
  // Simulate a delay for processing (replace with actual ML model processing later)
  setTimeout(() => {
    resultItem.innerHTML = `<p>Completed: ${file.name}</p>`;
    results.appendChild(resultItem);
  }, 2000); // Simulated delay for processing
}
