// Function to analyze stress level
function analyzeStress() {
    const userInput = document.getElementById('user-input').value;

    if (!userInput.trim()) {
        alert("Please enter some text to analyze.");
        return;
    }  

    fetch('/app2/predict', {  // ✅ Use /app2/predict
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: userInput }),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('result').textContent = "Detected Stress Level: " + data.stress_level;
    })
    .catch(error => {
        console.error('Error:', error);
        alert("An error occurred while analyzing stress level.");
    });
}

// Function to show the stress trend visualization
function showVisualization() {
    const img = document.getElementById('trend-image');
    img.src = '/app2/visualize?' + new Date().getTime(); // ✅ Use /app2/visualize
    img.style.display = 'block';
}

