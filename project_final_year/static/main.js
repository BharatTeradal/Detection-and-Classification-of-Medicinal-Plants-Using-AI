// This file contains all the JavaScript functionality previously embedded in the HTML file. 
// It handles image uploads, analyzes leaf images, displays results, and manages the feedback submission process.

// --- Leaf Analysis Section ---
const fileInputLeaf = document.getElementById('leaf-image');
const analyzeBtn = document.getElementById('analyze-btn');
const previewImage = document.getElementById('preview-image');
const loading = document.getElementById('loading');
const error = document.getElementById('error');
const result = document.getElementById('result');

// --- Plant Prediction Section ---
const fileInput = document.getElementById('fileInput');
const resultsDiv = document.getElementById('results');
const previewContainer = document.getElementById('preview-container');

// Preview selected images for plant prediction
fileInput.addEventListener('change', function (e) {
    const files = e.target.files;
    previewContainer.innerHTML = '';
    Array.from(files).forEach(file => {
        const reader = new FileReader();
        reader.onload = function (event) {
            const img = document.createElement('img');
            img.src = event.target.result;
            img.style.width = '100px';
            img.style.height = '100px';
            img.style.objectFit = 'cover';
            img.style.borderRadius = '8px';
            previewContainer.appendChild(img);
        };
        reader.readAsDataURL(file);
    });
});

// Upload images and get predictions
async function uploadImages() {
    const files = fileInput.files;
    if (!files.length) {
        alert("Please select image(s) to upload.");
        return;
    }

    const formData = new FormData();
    for (let file of files) {
        formData.append('files', file);
    }

    // Adjust endpoint as needed
    const response = await fetch('http://localhost:8000/predict', {
        method: 'POST',
        body: formData
    });

    const results = await response.json();
    resultsDiv.innerHTML = '';
    resultsDiv.style.display = 'flex';
    resultsDiv.style.flexWrap = 'wrap';
    resultsDiv.style.gap = '20px';

    results.forEach((result, index) => {
        const prediction = result.prediction;
        if (!prediction || Object.keys(prediction).length === 0) {
            resultsDiv.innerHTML += `<div class="card"><p>No prediction found for <strong>${result.filename}</strong>.</p></div>`;
            return;
        }

        // Show image and plant name
        const card = document.createElement('div');
        card.className = 'card';
        card.style.textAlign = 'center';
        card.style.cursor = 'pointer';
        card.style.width = '180px';
        card.style.boxShadow = '0 2px 8px rgba(0,0,0,0.08)';
        card.style.borderRadius = '10px';
        card.style.padding = '10px';
        card.style.background = '#f8f8f8';

        // Use the preview image if available
        const img = document.createElement('img');
        img.src = URL.createObjectURL(files[index]);
        img.className = 'result-thumb';
        img.style.width = '150px';
        img.style.height = '150px';
        img.style.objectFit = 'cover';
        img.style.borderRadius = '8px';
        img.style.cursor = 'pointer';
        img.onclick = () => showModal(prediction);

        const name = document.createElement('div');
        name.textContent = prediction.plant_name;
        name.className = 'plant-name';
        name.style.marginTop = '8px';
        name.style.fontWeight = 'bold';
        name.style.fontSize = '1.1em';

        card.appendChild(img);
        card.appendChild(name);
        resultsDiv.appendChild(card);
    });
}

// Modal logic for plant info
function showModal(prediction) {
    const modal = document.getElementById('info-modal');
    const modalContent = document.getElementById('modal-content');
    modalContent.innerHTML = `
        <h2>${prediction.plant_name}</h2>
        <h4>🌿 Basic Description</h4>
        <p>${prediction.basic_info?.definition || 'N/A'}</p>
        <p>${prediction.basic_info?.applications || 'N/A'}</p>
        <p>${prediction.basic_info?.advantages || 'N/A'}</p>
        <p>${prediction.basic_info?.usage || 'N/A'}</p>
        <p>${prediction.basic_info?.precautions || 'N/A'}</p>
        
b

        <h4>🧪 Medicinal Description</h4>
        <p>${prediction.healthcare_info?.definition || 'N/A'}</p>
        <p>${prediction.healthcare_info?.healthbenefits|| 'N/A'}</p>
        <p>${prediction.healthcare_info?.traditionaluse || 'N/A'}</p>
        <p>${prediction.healthcare_info?.activecompounds || 'N/A'}</p>
        <p>${prediction.healthcare_info?.dosage || 'N/A'}</p>
        <p>${prediction.healthcare_info?.precautions || 'N/A'}</p>
        <p>${prediction.healthcare_info?.sources || 'N/A'}</p>
        <button onclick="closeModal()" style="margin-top:10px;">Close</button>
    `;
    modal.style.display = 'flex';
}

function closeModal() {
    document.getElementById('info-modal').style.display = 'none';
}

// Optional: Close modal when clicking outside content
document.getElementById('info-modal').addEventListener('click', function (e) {
    if (e.target === this) closeModal();
});

// --- Leaf Analysis Logic ---
fileInputLeaf.addEventListener('change', function () {
    const file = fileInputLeaf.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            previewImage.src = e.target.result;
            previewImage.style.display = 'block';
        };
        reader.readAsDataURL(file);
        analyzeBtn.disabled = false;
    } else {
        previewImage.style.display = 'none';
        analyzeBtn.disabled = true;
    }
});

analyzeBtn.addEventListener('click', async () => {
    const file = fileInputLeaf.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    loading.style.display = 'block';
    error.style.display = 'none';
    result.style.display = 'none';

    try {
        const response = await fetch('/analyze_leaf', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) throw new Error('Analysis failed');

        const data = await response.json();
        displayResults(data.analysis);
        result.style.display = 'block';
    } catch (err) {
        error.textContent = 'Error analyzing leaf: ' + err.message;
        error.style.display = 'block';
    } finally {
        loading.style.display = 'none';
    }
});

function displayResults(analysis) {
    // Dimensions
    document.getElementById('width').textContent = analysis.dimensions.width;
    document.getElementById('height').textContent = analysis.dimensions.height;
    document.getElementById('aspect-ratio').textContent = analysis.dimensions.aspect_ratio;

    // Color
    document.getElementById('dominant-color').textContent = analysis.color.dominant_color;
    document.getElementById('rgb').textContent = 
        `R:${analysis.color.rgb.r} G:${analysis.color.rgb.g} B:${analysis.color.rgb.b}`;
    document.getElementById('intensity').textContent = analysis.color.intensity;

    // Shape
    document.getElementById('area').textContent = analysis.shape.area;
    document.getElementById('perimeter').textContent = analysis.shape.perimeter;
    document.getElementById('circularity').textContent = analysis.shape.circularity;

    // Texture
    document.getElementById('contrast').textContent = analysis.texture.contrast;
    document.getElementById('smoothness').textContent = analysis.texture.smoothness;
}

// --- Feedback Section ---
let latestPrediction = null;

function showFeedbackSection() {
    if (!latestPrediction) {
        alert("No prediction available to report.");
        return;
    }

    const reportedDiv = document.getElementById('reported-details');
    reportedDiv.innerHTML = `
        <strong>Identified Plant:</strong> ${latestPrediction.plant_name}<br/>
        <strong>Confidence:</strong> ${(latestPrediction.confidence * 100).toFixed(2)}%<br/>
        <strong>Definition:</strong> ${latestPrediction.basic_info?.definition || 'N/A'}
    `;

    document.getElementById('feedback-section').classList.remove('hidden');
}

async function submitFeedback() {
    const feedbackText = document.getElementById('feedback-text').value;
    const suggestedCorrection = document.getElementById('suggested-correction').value;

    if (!latestPrediction) {
        alert("No prediction to report feedback on.");
        return;
    }

    const feedbackData = {
        plant_name: latestPrediction.plant_name,
        user_feedback: feedbackText,
        suggested_correct_name: suggestedCorrection
    };

    const response = await fetch('http://localhost:8000/report_misclassification', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(feedbackData)
    });

    const result = await response.json();
    alert(result.message);
    document.getElementById('feedback-section').classList.add('hidden');
    document.getElementById('feedback-text').value = '';
    document.getElementById('suggested-correction').value = '';
}

// Expose closeModal globally for inline onclick
window.closeModal = closeModal;
window.submitFeedback = submitFeedback;

// --- END ---