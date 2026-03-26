/**
 * VedLinks Upload Page - Frontend Logic (Multi-File Support)
 */

document.addEventListener('DOMContentLoaded', () => {
    setupDropZone();
    loadExistingChapters();
});

// ===== File Drop Zone =====

let selectedFiles = [];

function setupDropZone() {
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const removeAllBtn = document.getElementById('removeAllFiles');

    // Click to browse
    dropZone.addEventListener('click', (e) => {
        if (e.target.closest('.btn-remove-file') || e.target.closest('.btn-remove-single')) return;
        fileInput.click();
    });

    // File selected via input
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            addFiles(Array.from(e.target.files));
        }
    });

    // Drag events
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('drag-over');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('drag-over');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('drag-over');
        if (e.dataTransfer.files.length > 0) {
            const pdfFiles = Array.from(e.dataTransfer.files).filter(
                f => f.type === 'application/pdf' || f.name.toLowerCase().endsWith('.pdf')
            );
            if (pdfFiles.length === 0) {
                showToast('Only PDF files are allowed', 'error');
            } else {
                if (pdfFiles.length < e.dataTransfer.files.length) {
                    showToast(`${e.dataTransfer.files.length - pdfFiles.length} non-PDF file(s) skipped`, 'error');
                }
                addFiles(pdfFiles);
            }
        }
    });

    // Remove all files
    removeAllBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        clearAllFiles();
    });

    // Form submit
    document.getElementById('uploadForm').addEventListener('submit', handleUpload);
}

function addFiles(newFiles) {
    // Filter out duplicates by name
    const existingNames = new Set(selectedFiles.map(f => f.name));
    const uniqueNew = newFiles.filter(f => !existingNames.has(f.name));

    if (uniqueNew.length < newFiles.length) {
        showToast(`${newFiles.length - uniqueNew.length} duplicate file(s) skipped`, 'error');
    }

    selectedFiles = [...selectedFiles, ...uniqueNew];
    renderFileList();
}

function removeFile(index) {
    selectedFiles.splice(index, 1);
    renderFileList();
}

function clearAllFiles() {
    selectedFiles = [];
    document.getElementById('fileInput').value = '';
    renderFileList();
}

function renderFileList() {
    const content = document.getElementById('dropZoneContent');
    const selected = document.getElementById('dropZoneSelected');
    const filesList = document.getElementById('selectedFilesList');
    const filesCount = document.getElementById('filesCount');

    if (selectedFiles.length === 0) {
        content.style.display = '';
        selected.style.display = 'none';
        return;
    }

    content.style.display = 'none';
    selected.style.display = 'block';
    filesCount.textContent = `${selectedFiles.length} file${selectedFiles.length > 1 ? 's' : ''} selected`;

    filesList.innerHTML = selectedFiles.map((file, i) => `
        <div class="selected-file-item">
            <span class="selected-file-icon">📄</span>
            <span class="selected-file-name" title="${file.name}">${file.name}</span>
            <span class="selected-file-size">${formatSize(file.size)}</span>
            <button type="button" class="btn-remove-single" onclick="event.stopPropagation(); removeFile(${i})" title="Remove">✕</button>
        </div>
    `).join('');
}

function formatSize(bytes) {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
}

// ===== Upload Handler =====

async function handleUpload(e) {
    e.preventDefault();

    if (selectedFiles.length === 0) {
        showToast('Please select at least one PDF file', 'error');
        return;
    }

    const classVal = document.getElementById('classSelect').value;
    const subject = document.getElementById('subjectSelect').value;
    const chapterNumber = document.getElementById('chapterNumber').value;
    const chapterName = document.getElementById('chapterName').value.trim();
    const topics = document.getElementById('topicsInput').value.trim();

    if (!classVal || !subject || !chapterNumber || !chapterName) {
        showToast('Please fill in all required fields', 'error');
        return;
    }

    const uploadBtn = document.getElementById('uploadBtn');
    uploadBtn.disabled = true;
    uploadBtn.innerHTML = '<span class="btn-icon">⏳</span> Uploading...';

    const formData = new FormData();

    // Append all files
    selectedFiles.forEach(file => {
        formData.append('files', file);
    });

    formData.append('class', classVal);
    formData.append('subject', subject);
    formData.append('chapter_number', chapterNumber);
    formData.append('chapter_name', chapterName);
    formData.append('topics', topics);

    try {
        const response = await fetch('/api/upload-textbook', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            if (response.status === 413) {
                showToast('File is too large. Maximum size allowed is 100MB.', 'error');
            } else {
                try {
                    const data = await response.json();
                    showToast(data.error || 'Upload failed', 'error');
                } catch (e) {
                    showToast(`Server issue (${response.status}). The file might be too large or invalid.`, 'error');
                }
            }
            return;
        }

        const data = await response.json();

        if (data.success) {
            showToast(data.message, 'success');
            // Reset form
            clearAllFiles();
            document.getElementById('uploadForm').reset();
            // Reload history
            loadExistingChapters();
        } else {
            showToast(data.error || 'Upload failed', 'error');
        }
    } catch (error) {
        console.error('Upload error:', error);
        showToast('Network error: ' + error.message, 'error');
    } finally {
        uploadBtn.disabled = false;
        uploadBtn.innerHTML = '<span class="btn-icon">📤</span> Upload Textbook';
    }
}

// ===== Load Existing Chapters =====

async function loadExistingChapters() {
    const container = document.getElementById('historyList');

    try {
        const response = await fetch('/api/topics-grouped');
        const data = await response.json();

        if (data.success && Object.keys(data.grouped).length > 0) {
            container.innerHTML = '';
            const grouped = data.grouped;

            for (const cls of Object.keys(grouped)) {
                for (const subject of Object.keys(grouped[cls])) {
                    const chapters = grouped[cls][subject];

                    const groupDiv = document.createElement('div');
                    groupDiv.className = 'history-group';
                    groupDiv.innerHTML = `
                        <div class="history-group-header">
                            <span class="history-class-badge">Class ${cls}</span>
                            <span class="history-subject">${subject}</span>
                            <span class="history-count">${chapters.length} ch</span>
                        </div>
                    `;

                    chapters.forEach(ch => {
                        const item = document.createElement('div');
                        item.className = 'history-item';
                        item.innerHTML = `
                            <span class="history-ch-num">Ch ${ch.chapter_number}</span>
                            <span class="history-ch-name">${ch.chapter}</span>
                        `;
                        groupDiv.appendChild(item);
                    });

                    container.appendChild(groupDiv);
                }
            }
        } else {
            container.innerHTML = '<div class="no-topics">No chapters uploaded yet</div>';
        }
    } catch (error) {
        container.innerHTML = '<div class="error">Failed to load chapters</div>';
    }
}

// ===== AI Training Logic =====

let trainingPollInterval = null;

async function startTraining() {
    const btn = document.getElementById('startTrainingBtn');
    const statusBox = document.getElementById('trainingStatus');

    try {
        const response = await fetch('/api/start-finetuning', { method: 'POST' });
        const data = await response.json();

        if (data.success) {
            showToast('Fine-tuning started in the background', 'success');
            btn.disabled = true;
            statusBox.style.display = 'block';
            startPollingStatus();
        } else {
            showToast(data.error || 'Failed to start training', 'error');
        }
    } catch (error) {
        showToast('Network error: ' + error.message, 'error');
    }
}

function startPollingStatus() {
    if (trainingPollInterval) clearInterval(trainingPollInterval);

    trainingPollInterval = setInterval(async () => {
        try {
            const response = await fetch('/api/training-status');
            const data = await response.json();

            updateTrainingUI(data);

            if (!data.is_training && (data.current_step === 'completed' || data.current_step === 'failed')) {
                clearInterval(trainingPollInterval);
                document.getElementById('startTrainingBtn').disabled = false;
                if (data.current_step === 'completed') {
                    showToast('AI Model has been successfully updated!', 'success');
                }
            }
        } catch (error) {
            console.error('Status poll error:', error);
        }
    }, 2000);
}

function updateTrainingUI(data) {
    const progressBar = document.getElementById('progressBar');
    const progressPercent = document.getElementById('progressPercent');
    const stepText = document.getElementById('currentStepText');
    const latestLog = document.getElementById('latestLog');
    const statusBox = document.getElementById('trainingStatus');

    if (data.is_training || data.current_step !== 'idle') {
        statusBox.style.display = 'block';
        progressBar.style.width = `${data.progress}%`;
        progressPercent.textContent = `${Math.round(data.progress)}%`;

        let stepLabel = "Processing...";
        if (data.current_step === 'generating_data') stepLabel = "📚 Extracting textbook data...";
        if (data.current_step === 'training_model') stepLabel = "🧠 Fine-tuning AI model...";
        if (data.current_step === 'completed') stepLabel = "✅ Training Finished!";
        if (data.current_step === 'failed') stepLabel = "❌ Training Failed";

        stepText.textContent = stepLabel;

        if (data.logs && data.logs.length > 0) {
            latestLog.textContent = data.logs[data.logs.length - 1];
        }
    }
}

// Initial status check
async function checkInitialStatus() {
    try {
        const response = await fetch('/api/training-status');
        const data = await response.json();
        if (data.is_training || data.current_step === 'completed') {
            updateTrainingUI(data);
            if (data.is_training) startPollingStatus();
        }
    } catch (e) { }
}

// Event Listeners
document.getElementById('startTrainingBtn')?.addEventListener('click', startTraining);
checkInitialStatus();

// ===== Toast =====

function showToast(message, type = 'success') {
    const existing = document.querySelector('.toast');
    if (existing) existing.remove();

    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    const icon = type === 'success' ? '✓' : '✕';
    toast.innerHTML = `
        <span class="toast-icon">${icon}</span>
        <span class="toast-message">${message}</span>
    `;

    document.body.appendChild(toast);
    setTimeout(() => toast.classList.add('show'), 10);
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}
