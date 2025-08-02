document.getElementById('imageUpload').addEventListener('change', function(e) {
    const preview = document.getElementById('imagePreview');
    preview.innerHTML = '';
    
    if (e.target.files.length) {
        const img = document.createElement('img');
        img.src = URL.createObjectURL(e.target.files[0]);
        img.classList.add('preview-image');
        preview.appendChild(img);
        
        // Start fake scanning animation
        const scanLine = document.createElement('div');
        scanLine.classList.add('scan-line');
        preview.appendChild(scanLine);
        
        setTimeout(() => {
            scanLine.style.transform = 'translateY(100%)';
        }, 100);
    }
});

// Form submission
document.getElementById('uploadForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const btn = document.getElementById('calculateBtn');
    btn.innerHTML = '<div class="ai-thinking">ANALYZING<span class="dots"></span></div>';
    
    // Simulate AI processing
    setTimeout(() => {
        this.submit();
    }, 3000);
});