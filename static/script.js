/**
 * VedLinks AI Question Paper Generator - Frontend Logic
 */

// State Management
const state = {
    sections: [],
    topics: [],
    selectedTopics: new Set(),
    nextSectionIndex: 0,
    sectionLetters: 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
    modelLoaded: false,
    currentPaper: null  // Store generated paper for export
};

// Question Types
const QUESTION_TYPES = {
    'mcq': 'Multiple Choice (MCQ)',
    'fill_blank': 'Fill in the Blanks',
    'very_short': 'Very Short Answer',
    'short': 'Short Answer',
    'long': 'Long Answer'
};

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    loadTopics();
    checkModelStatus();
    addSection(); // Add default Section A
});

// ===== Topics Management =====

async function loadTopics() {
    const container = document.getElementById('topicsList');

    try {
        const response = await fetch('/api/topics');
        const data = await response.json();

        if (data.success && data.topics.length > 0) {
            state.topics = data.topics;
            renderTopics();
        } else {
            container.innerHTML = '<div class="no-topics">No topics found in data/raw/</div>';
        }
    } catch (error) {
        console.error('Error loading topics:', error);
        container.innerHTML = '<div class="error">Failed to load topics</div>';
    }
}

function renderTopics() {
    const container = document.getElementById('topicsList');
    container.innerHTML = '';

    state.topics.forEach(topic => {
        const isSelected = state.selectedTopics.has(topic.id);
        const div = document.createElement('div');
        div.className = `topic-item${isSelected ? ' selected' : ''}`;
        div.onclick = () => toggleTopic(topic.id);

        div.innerHTML = `
            <div class="topic-checkmark"></div>
            <div class="topic-info">
                <div class="topic-name">${topic.name}</div>
                <div class="topic-meta">${topic.type} • ${topic.size}</div>
            </div>
        `;

        container.appendChild(div);
    });
}

function toggleTopic(topicId) {
    if (state.selectedTopics.has(topicId)) {
        state.selectedTopics.delete(topicId);
    } else {
        state.selectedTopics.add(topicId);
    }
    renderTopics();
}

function selectAllTopics() {
    state.topics.forEach(topic => state.selectedTopics.add(topic.id));
    renderTopics();
}

function clearAllTopics() {
    state.selectedTopics.clear();
    renderTopics();
}

// ===== Difficulty Management =====

function updateDifficulty() {
    const easy = parseInt(document.getElementById('easySlider').value);
    const medium = parseInt(document.getElementById('mediumSlider').value);
    const hard = parseInt(document.getElementById('hardSlider').value);

    document.getElementById('easyValue').textContent = `${easy}%`;
    document.getElementById('mediumValue').textContent = `${medium}%`;
    document.getElementById('hardValue').textContent = `${hard}%`;

    const total = easy + medium + hard;
    const warning = document.getElementById('difficultyWarning');

    if (total !== 100) {
        warning.style.display = 'block';
        warning.textContent = `⚠️ Total is ${total}% (should be 100%)`;
    } else {
        warning.style.display = 'none';
    }
}

// ===== Sections Management =====

function addSection() {
    const letter = state.sectionLetters[state.nextSectionIndex] || `S${state.nextSectionIndex + 1}`;

    const section = {
        id: Date.now(),
        name: letter,
        questionType: 'mcq',
        questionCount: 10,
        marksPerQuestion: 1
    };

    state.sections.push(section);
    state.nextSectionIndex++;

    renderSections();
    updateTotalMarks();
}

function removeSection(sectionId) {
    state.sections = state.sections.filter(s => s.id !== sectionId);

    // Rename remaining sections
    state.sections.forEach((section, index) => {
        section.name = state.sectionLetters[index] || `S${index + 1}`;
    });
    state.nextSectionIndex = state.sections.length;

    renderSections();
    updateTotalMarks();
}

function updateSection(sectionId, field, value) {
    const section = state.sections.find(s => s.id === sectionId);
    if (section) {
        if (field === 'questionCount' || field === 'marksPerQuestion') {
            section[field] = parseInt(value) || 1;
        } else {
            section[field] = value;
        }
        renderSections();
        updateTotalMarks();
    }
}

function renderSections() {
    const container = document.getElementById('sectionsContainer');
    container.innerHTML = '';

    state.sections.forEach(section => {
        const totalMarks = section.questionCount * section.marksPerQuestion;

        const card = document.createElement('div');
        card.className = 'section-card';
        card.innerHTML = `
            <div class="section-header">
                <span class="section-name">Section ${section.name}</span>
                <button class="btn btn-sm btn-danger" onclick="removeSection(${section.id})">
                    ✕ Remove
                </button>
            </div>
            <div class="section-body">
                <div class="section-field">
                    <label>Question Type</label>
                    <select class="form-select" onchange="updateSection(${section.id}, 'questionType', this.value)">
                        ${Object.entries(QUESTION_TYPES).map(([value, label]) =>
            `<option value="${value}"${section.questionType === value ? ' selected' : ''}>${label}</option>`
        ).join('')}
                    </select>
                </div>
                <div class="section-field">
                    <label>Number of Questions</label>
                    <input type="number" class="form-input" min="1" max="50" 
                           value="${section.questionCount}"
                           onchange="updateSection(${section.id}, 'questionCount', this.value)">
                </div>
                <div class="section-field">
                    <label>Marks per Question</label>
                    <input type="number" class="form-input" min="1" max="20" 
                           value="${section.marksPerQuestion}"
                           onchange="updateSection(${section.id}, 'marksPerQuestion', this.value)">
                </div>
                <div class="section-field">
                    <label>Section Total</label>
                    <div class="section-total">
                        <span class="section-total-label">${section.questionCount} × ${section.marksPerQuestion} =</span>
                        <span class="section-total-value">${totalMarks} marks</span>
                    </div>
                </div>
            </div>
        `;

        container.appendChild(card);
    });
}

function updateTotalMarks() {
    const total = state.sections.reduce((sum, section) => {
        return sum + (section.questionCount * section.marksPerQuestion);
    }, 0);

    document.getElementById('totalMarks').textContent = total;
}

// ===== Model Status =====

async function checkModelStatus() {
    const statusEl = document.getElementById('modelStatus');
    const dot = statusEl.querySelector('.status-dot');
    const text = statusEl.querySelector('.status-text');

    try {
        const response = await fetch('/api/model-status');
        const data = await response.json();

        if (data.loaded) {
            dot.className = 'status-dot loaded';
            text.textContent = `Model ready (${data.device})`;
            state.modelLoaded = true;
        } else {
            dot.className = 'status-dot';
            text.textContent = 'Model not loaded';
        }
    } catch (error) {
        dot.className = 'status-dot error';
        text.textContent = 'Server offline';
    }
}

// ===== Paper Generation =====

async function generatePaper() {
    // Validation
    if (state.selectedTopics.size === 0) {
        alert('Please select at least one topic');
        return;
    }

    if (state.sections.length === 0) {
        alert('Please add at least one section');
        return;
    }

    // Show loading overlay
    const overlay = document.getElementById('loadingOverlay');
    const statusText = document.getElementById('loadingStatus');
    overlay.classList.add('active');

    const generateBtn = document.getElementById('generateBtn');
    generateBtn.disabled = true;

    try {
        statusText.textContent = 'Preparing configuration...';

        // Build configuration
        const config = {
            examType: document.getElementById('examType').value,
            difficulty: {
                easy: parseInt(document.getElementById('easySlider').value),
                medium: parseInt(document.getElementById('mediumSlider').value),
                hard: parseInt(document.getElementById('hardSlider').value)
            },
            selectedTopics: Array.from(state.selectedTopics),
            sections: state.sections.map(s => ({
                name: s.name,
                questionType: s.questionType,
                questionCount: s.questionCount,
                marksPerQuestion: s.marksPerQuestion,
                totalMarks: s.questionCount * s.marksPerQuestion
            })),
            includeAnswerKey: document.getElementById('includeAnswerKey').checked,
            includeMarkingScheme: document.getElementById('includeMarkingScheme').checked,
            includeChapterSplit: document.getElementById('includeChapterSplit').checked
        };

        statusText.textContent = 'Loading AI model...';

        // Generate paper
        const response = await fetch('/api/generate-paper', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(config)
        });

        statusText.textContent = 'Generating questions...';

        const data = await response.json();

        if (data.success) {
            statusText.textContent = 'Rendering paper...';
            renderPaper(data.paper);
        } else {
            throw new Error(data.error || 'Failed to generate paper');
        }

    } catch (error) {
        console.error('Generation error:', error);
        alert('Error generating paper: ' + error.message);
    } finally {
        overlay.classList.remove('active');
        generateBtn.disabled = false;
    }
}

// ===== Paper Rendering =====

function renderPaper(paper) {
    const outputPanel = document.getElementById('outputPanel');

    let html = `
        <div class="paper-output">
            <div class="paper-header">
                <h3>📄 ${formatExamType(paper.examType)} - ${paper.totalMarks} Marks</h3>
                <div class="paper-actions">
                    <button class="btn btn-primary" onclick="downloadWord()">📥 Download Word</button>
                    <button class="btn btn-secondary" onclick="printPaper()">🖨️ Print</button>
                    <button class="btn btn-secondary" onclick="copyPaper()">📋 Copy</button>
                </div>
            </div>
            <div class="paper-content" id="paperContent">
    `;

    // Render each section
    paper.sections.forEach(section => {
        html += `
            <div class="paper-section">
                <div class="paper-section-header">
                    <span class="paper-section-title">Section ${section.name} - ${formatQuestionType(section.questionType)}</span>
                    <span class="paper-section-info">${section.questions.length} questions × ${section.marksPerQuestion} marks = ${section.totalMarks} marks</span>
                </div>
        `;

        section.questions.forEach((q, idx) => {
            html += renderQuestion(q, idx + 1, section.questionType);
        });

        html += '</div>';
    });

    // Answer Key
    if (paper.answerKey) {
        html += `
            <div class="answer-key-section">
                <h4>📝 Answer Key</h4>
        `;

        paper.answerKey.forEach(section => {
            html += `<div style="margin-bottom: 1rem;"><strong>Section ${section.section}</strong></div>`;
            section.answers.forEach(ans => {
                html += `
                    <div class="answer-item">
                        <span class="answer-number">Q${ans.number}.</span>
                        <span>${ans.answer}</span>
                    </div>
                `;
            });
        });

        html += '</div>';
    }

    // Marking Scheme
    if (paper.markingScheme) {
        html += `
            <div class="marking-scheme-section">
                <h4>📊 Marking Scheme</h4>
        `;

        paper.markingScheme.forEach(scheme => {
            html += `
                <div class="answer-item">
                    <strong>Section ${scheme.section}:</strong>
                    ${scheme.guidelines}
                </div>
            `;
        });

        html += '</div>';
    }

    // Chapter Split
    if (paper.chapterSplit) {
        html += `
            <div class="chapter-split-section">
                <h4>📈 Chapter-wise Marks Distribution</h4>
        `;

        Object.entries(paper.chapterSplit.distribution).forEach(([topic, marks]) => {
            html += `
                <div class="answer-item">
                    <span>${topic}:</span>
                    <span>${marks} marks</span>
                </div>
            `;
        });

        html += '</div>';
    }

    html += '</div></div>';

    outputPanel.innerHTML = html;

    // Store paper for export
    state.currentPaper = paper;
}

function renderQuestion(q, number, type) {
    let html = `
        <div class="question-item">
            <span class="question-marks">${q.marks} mark${q.marks > 1 ? 's' : ''}</span>
            <span class="question-number">${number}</span>
            <span class="question-text">${q.question}</span>
    `;

    if (type === 'mcq' && q.options) {
        html += '<div class="mcq-options">';
        q.options.forEach(option => {
            html += `<div class="mcq-option">${option}</div>`;
        });
        html += '</div>';
    }

    html += '</div>';
    return html;
}

function formatExamType(type) {
    const types = {
        'unit_test': 'Unit Test',
        'midterm': 'Midterm Examination',
        'final': 'Final Examination',
        'practice': 'Practice Paper'
    };
    return types[type] || type;
}

function formatQuestionType(type) {
    return QUESTION_TYPES[type] || type;
}

// ===== Utility Functions =====

function printPaper() {
    const content = document.getElementById('paperContent');
    if (content) {
        const printWindow = window.open('', '_blank');
        printWindow.document.write(`
            <html>
            <head>
                <title>Question Paper</title>
                <style>
                    body { font-family: Arial, sans-serif; padding: 20px; }
                    .paper-section { margin-bottom: 20px; }
                    .paper-section-header { background: #f0f0f0; padding: 10px; margin-bottom: 10px; }
                    .question-item { padding: 10px; border-bottom: 1px solid #eee; }
                    .question-number { display: inline-block; width: 30px; font-weight: bold; }
                    .question-marks { float: right; color: #666; }
                    .mcq-options { margin-left: 30px; margin-top: 5px; }
                    .mcq-option { padding: 3px 0; }
                    .answer-key-section, .marking-scheme-section { margin-top: 30px; border-top: 2px dashed #ccc; padding-top: 20px; }
                </style>
            </head>
            <body>${content.innerHTML}</body>
            </html>
        `);
        printWindow.document.close();
        printWindow.print();
    }
}

function copyPaper() {
    const content = document.getElementById('paperContent');
    if (content) {
        // Extract text content
        const text = content.innerText;
        navigator.clipboard.writeText(text).then(() => {
            alert('Paper copied to clipboard!');
        }).catch(err => {
            console.error('Copy failed:', err);
        });
    }
}

// ===== Word Document Export =====

async function downloadWord() {
    if (!state.currentPaper) {
        alert('No paper generated yet. Please generate a paper first.');
        return;
    }

    try {
        const response = await fetch('/api/export-docx', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ paper: state.currentPaper })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Export failed');
        }

        // Download the file
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `question_paper_${new Date().toISOString().slice(0, 10)}.docx`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);

    } catch (error) {
        console.error('Download error:', error);
        alert('Error downloading Word document: ' + error.message);
    }
}
