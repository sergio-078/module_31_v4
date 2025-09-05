// Basic JavaScript for the site

// Auto-dismiss alerts after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Confirmations for delete actions
    const deleteForms = document.querySelectorAll('form[data-confirm]');
    deleteForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const message = this.getAttribute('data-confirm') || 'Are you sure?';
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });

    // Category filter
    const categoryFilter = document.getElementById('category-filter');
    if (categoryFilter) {
        categoryFilter.addEventListener('change', function() {
            this.form.submit();
        });
    }

    // Initialize CKEditor tooltips
    initEditorTools();
});

// Preview image before upload
function previewImage(input) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        const preview = document.getElementById('image-preview');

        if (!preview) {
            // Create preview container if it doesn't exist
            const container = document.createElement('div');
            container.id = 'image-preview';
            container.className = 'mt-2';
            container.innerHTML = '<p class="text-muted small">Preview:</p><img class="img-thumbnail" style="max-height: 200px;">';
            input.parentNode.appendChild(container);
        }

        reader.onload = function(e) {
            const img = document.querySelector('#image-preview img');
            img.src = e.target.result;
            img.alt = 'Preview';
        }

        reader.readAsDataURL(input.files[0]);
    }
}

// Initialize editor tools
function initEditorTools() {
    // Add responsive class to embedded content
    document.querySelectorAll('.post-content iframe, .post-content video').forEach(media => {
        media.classList.add('embed-responsive-item');
    });

    // Add lightbox to images
    document.querySelectorAll('.post-content img').forEach(img => {
        img.classList.add('img-fluid', 'rounded');
        img.style.cursor = 'pointer';
        img.onclick = function() {
            const modal = document.createElement('div');
            modal.className = 'modal fade';
            modal.innerHTML = `
                <div class="modal-dialog modal-lg modal-dialog-centered">
                    <div class="modal-content">
                        <div class="modal-body text-center">
                            <img src="${this.src}" alt="${this.alt}" class="img-fluid">
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        </div>
                    </div>
                </div>
            `;
            document.body.appendChild(modal);
            new bootstrap.Modal(modal).show();
            modal.addEventListener('hidden.bs.modal', () => modal.remove());
        };
    });
}

// Video player controls
function initVideoPlayers() {
    document.querySelectorAll('video').forEach(video => {
        video.controls = true;
        video.classList.add('embed-responsive-item');
    });
}

// Copy embed code
function copyEmbedCode(element) {
    const code = element.previousElementSibling.textContent;
    navigator.clipboard.writeText(code).then(() => {
        const originalText = element.textContent;
        element.textContent = 'Copied!';
        setTimeout(() => {
            element.textContent = originalText;
        }, 2000);
    });
}

// Fallback для CKEditor
function setupCKEditorFallback() {
    if (typeof CKEDITOR === 'undefined') {
        console.warn('CKEditor не доступен, используем обычное текстовое поле');
        const editor = document.getElementById('content-editor');
        if (editor) {
            editor.style.display = 'block';
            editor.style.visibility = 'visible';
            editor.classList.add('form-control');
        }
    }
}

// Проверяем через 5 секунд
setTimeout(setupCKEditorFallback, 5000);