// Main JavaScript for Credit Card Fraud Detection App

// Global variables
let uploadInProgress = false;

// Document ready
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Initialize tooltips
    initializeTooltips();

    // Initialize file upload handlers
    initializeFileUpload();

    // Initialize form validation
    initializeFormValidation();

    // Add animations
    addAnimations();

    // Initialize cyber effects
    initializeCyberEffects();

    // Add particle background
    initializeParticles();

    console.log('🚀 Fraud Detection AI initialized');
}

function initializeTooltips() {
    // Initialize Bootstrap tooltips if available
    if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
}

function initializeFileUpload() {
    const fileInput = document.getElementById('file');
    const uploadForm = document.getElementById('uploadForm');
    
    if (fileInput) {
        // File input change handler
        fileInput.addEventListener('change', function(e) {
            handleFileSelection(e);
        });
        
        // Drag and drop functionality
        setupDragAndDrop(fileInput);
    }
    
    if (uploadForm) {
        uploadForm.addEventListener('submit', function(e) {
            handleFormSubmit(e);
        });
    }
}

function handleFileSelection(event) {
    const file = event.target.files[0];
    const fileInfo = document.getElementById('fileInfo');
    
    if (file) {
        const fileSize = (file.size / 1024 / 1024).toFixed(2);
        const fileName = file.name;
        
        // Validate file
        const validation = validateFile(file);
        
        if (validation.valid) {
            showFileInfo(fileName, fileSize, 'success');
            enableSubmitButton();
        } else {
            showFileInfo(fileName, fileSize, 'error', validation.message);
            disableSubmitButton();
        }
    }
}

function validateFile(file) {
    const maxSize = 16 * 1024 * 1024; // 16MB
    const allowedTypes = ['text/csv', 'application/vnd.ms-excel'];
    const allowedExtensions = ['.csv'];
    
    // Check file size
    if (file.size > maxSize) {
        return {
            valid: false,
            message: 'File size exceeds 16MB limit'
        };
    }
    
    // Check file extension
    const fileName = file.name.toLowerCase();
    const hasValidExtension = allowedExtensions.some(ext => fileName.endsWith(ext));
    
    if (!hasValidExtension) {
        return {
            valid: false,
            message: 'Only CSV files are allowed'
        };
    }
    
    return { valid: true };
}

function showFileInfo(fileName, fileSize, status, message = '') {
    // Create or update file info display
    let fileInfoDiv = document.getElementById('fileInfo');
    
    if (!fileInfoDiv) {
        fileInfoDiv = document.createElement('div');
        fileInfoDiv.id = 'fileInfo';
        fileInfoDiv.className = 'mt-3';
        
        const fileInput = document.getElementById('file');
        fileInput.parentNode.appendChild(fileInfoDiv);
    }
    
    const statusClass = status === 'success' ? 'alert-success' : 'alert-danger';
    const icon = status === 'success' ? 'fa-check-circle' : 'fa-exclamation-triangle';
    
    fileInfoDiv.innerHTML = `
        <div class="alert ${statusClass} alert-dismissible fade show" role="alert">
            <i class="fas ${icon} me-2"></i>
            <strong>${fileName}</strong> (${fileSize} MB)
            ${message ? `<br><small>${message}</small>` : ''}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
}

function setupDragAndDrop(fileInput) {
    const dropZone = fileInput.parentElement;
    
    // Add drag and drop styling
    dropZone.addEventListener('dragover', function(e) {
        e.preventDefault();
        dropZone.classList.add('drag-over');
    });
    
    dropZone.addEventListener('dragleave', function(e) {
        e.preventDefault();
        dropZone.classList.remove('drag-over');
    });
    
    dropZone.addEventListener('drop', function(e) {
        e.preventDefault();
        dropZone.classList.remove('drag-over');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            fileInput.files = files;
            handleFileSelection({ target: { files: files } });
        }
    });
}

function handleFormSubmit(event) {
    const fileInput = document.getElementById('file');
    const submitBtn = document.getElementById('submitBtn');
    
    if (uploadInProgress) {
        event.preventDefault();
        return;
    }
    
    if (!fileInput.files.length) {
        event.preventDefault();
        showAlert('Please select a CSV file to upload.', 'warning');
        return;
    }
    
    const file = fileInput.files[0];
    const validation = validateFile(file);
    
    if (!validation.valid) {
        event.preventDefault();
        showAlert(validation.message, 'danger');
        return;
    }
    
    // Show loading state
    uploadInProgress = true;
    showLoadingState(submitBtn);
    showLoadingModal();
}

function showLoadingState(button) {
    if (button) {
        button.disabled = true;
        button.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
    }
}

function showLoadingModal() {
    const loadingModal = document.getElementById('loadingModal');
    if (loadingModal && typeof bootstrap !== 'undefined') {
        const modal = new bootstrap.Modal(loadingModal);
        modal.show();
    }
}

function enableSubmitButton() {
    const submitBtn = document.getElementById('submitBtn');
    if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.classList.remove('btn-secondary');
        submitBtn.classList.add('btn-primary');
    }
}

function disableSubmitButton() {
    const submitBtn = document.getElementById('submitBtn');
    if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.classList.remove('btn-primary');
        submitBtn.classList.add('btn-secondary');
    }
}

function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        <i class="fas fa-info-circle me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }
}

function addAnimations() {
    // Add staggered animations to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        if (!card.style.animationDelay) {
            card.style.animationDelay = `${index * 0.15}s`;
            card.classList.add('fade-in-up');
        }
    });

    // Add hover effects to feature icons
    const featureIcons = document.querySelectorAll('.feature-icon');
    featureIcons.forEach(icon => {
        icon.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.1) rotate(5deg)';
        });

        icon.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1) rotate(0deg)';
        });
    });
}

function initializeCyberEffects() {
    // Add glitch effect to cyber text on hover
    const cyberTexts = document.querySelectorAll('.text-cyber');
    cyberTexts.forEach(text => {
        text.addEventListener('mouseenter', function() {
            this.style.textShadow = '2px 0 #ff0000, -2px 0 #00ffff';
            this.style.animation = 'glitch 0.3s ease-in-out';
        });

        text.addEventListener('mouseleave', function() {
            this.style.textShadow = 'none';
            this.style.animation = 'none';
        });
    });

    // Add typing effect to gradient text
    const gradientTexts = document.querySelectorAll('.gradient-text');
    gradientTexts.forEach(text => {
        const originalText = text.textContent;
        text.textContent = '';

        let i = 0;
        const typeWriter = () => {
            if (i < originalText.length) {
                text.textContent += originalText.charAt(i);
                i++;
                setTimeout(typeWriter, 50);
            }
        };

        // Start typing effect after a delay
        setTimeout(typeWriter, 500);
    });
}

function initializeParticles() {
    // Create floating particles effect
    const particleContainer = document.createElement('div');
    particleContainer.className = 'particle-container';
    particleContainer.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
    `;

    document.body.appendChild(particleContainer);

    // Create particles
    for (let i = 0; i < 20; i++) {
        createParticle(particleContainer);
    }
}

function createParticle(container) {
    const particle = document.createElement('div');
    particle.style.cssText = `
        position: absolute;
        width: 4px;
        height: 4px;
        background: linear-gradient(45deg, #6366f1, #ec4899);
        border-radius: 50%;
        opacity: 0.6;
        animation: float ${Math.random() * 10 + 10}s linear infinite;
    `;

    // Random starting position
    particle.style.left = Math.random() * 100 + '%';
    particle.style.top = '100%';

    container.appendChild(particle);

    // Remove particle after animation
    setTimeout(() => {
        if (particle.parentNode) {
            particle.parentNode.removeChild(particle);
        }
    }, 20000);
}

function initializeFormValidation() {
    // Add real-time validation for forms
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('input', function(e) {
            validateFormField(e.target);
        });
    });
}

function validateFormField(field) {
    if (field.type === 'file') {
        const files = field.files;
        if (files.length > 0) {
            const validation = validateFile(files[0]);
            if (validation.valid) {
                field.classList.remove('is-invalid');
                field.classList.add('is-valid');
            } else {
                field.classList.remove('is-valid');
                field.classList.add('is-invalid');
            }
        }
    }
}

// Utility functions
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function() {
        showAlert('Copied to clipboard!', 'success');
    }).catch(function(err) {
        console.error('Could not copy text: ', err);
        showAlert('Failed to copy to clipboard', 'danger');
    });
}

// Export functions for global access
window.FraudDetectionApp = {
    showAlert,
    formatFileSize,
    formatNumber,
    copyToClipboard,
    validateFile
};

// Add CSS for drag and drop
const style = document.createElement('style');
style.textContent = `
    .drag-over {
        border-color: #007bff !important;
        background-color: rgba(0, 123, 255, 0.1) !important;
    }
    
    .fade-in-up {
        animation: fadeInUp 0.6s ease-out forwards;
        opacity: 0;
    }
`;
document.head.appendChild(style);
