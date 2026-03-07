/**
 * VedLinks AI Question Paper Generator - Frontend Logic
 */

// State Management
const state = {
    sections: [],
    topics: [],
    groupedTopics: {},     // Class -> Subject -> Chapters
    selectedTopics: new Set(),
    expandedClasses: new Set(),
    expandedSubjects: new Set(),
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
        const response = await fetch('/api/topics-grouped');
        const data = await response.json();

        if (data.success && Object.keys(data.grouped).length > 0) {
            state.groupedTopics = data.grouped;
            // Also flatten for backward compat with generatePaper
            state.topics = [];
            for (const cls in data.grouped) {
                for (const subject in data.grouped[cls]) {
                    data.grouped[cls][subject].forEach(ch => {
                        state.topics.push({ id: ch.id, name: ch.chapter, class: cls, subject });
                    });
                }
            }
            // Expand first class by default
            const firstClass = Object.keys(data.grouped)[0];
            if (firstClass) {
                state.expandedClasses.add(firstClass);
                const firstSubject = Object.keys(data.grouped[firstClass])[0];
                if (firstSubject) state.expandedSubjects.add(`${firstClass}|${firstSubject}`);
            }
            renderTopics();
        } else {
            container.innerHTML = '<div class="no-topics">No topics found</div>';
        }
    } catch (error) {
        console.error('Error loading topics:', error);
        container.innerHTML = '<div class="error">Failed to load topics</div>';
    }
}

function renderTopics() {
    const container = document.getElementById('topicsList');
    container.innerHTML = '';

    const grouped = state.groupedTopics;

    for (const cls of Object.keys(grouped)) {
        const isClassExpanded = state.expandedClasses.has(cls);
        const subjects = grouped[cls];

        // Count selected in this class
        let classTotal = 0, classSelected = 0;
        for (const subj in subjects) {
            subjects[subj].forEach(ch => {
                classTotal++;
                if (state.selectedTopics.has(ch.id)) classSelected++;
            });
        }

        // Class header
        const classDiv = document.createElement('div');
        classDiv.className = 'topic-class-group';
        classDiv.innerHTML = `
            <div class="topic-class-header ${isClassExpanded ? 'expanded' : ''}" onclick="toggleClassGroup('${cls}')">
                <span class="topic-chevron">${isClassExpanded ? '▾' : '▸'}</span>
                <span class="topic-class-badge">Class ${cls}</span>
                <span class="topic-count-badge">${classSelected}/${classTotal}</span>
            </div>
        `;

        // Class body (subjects)
        const classBody = document.createElement('div');
        classBody.className = `topic-class-body ${isClassExpanded ? 'expanded' : ''}`;

        for (const subject of Object.keys(subjects)) {
            const subjectKey = `${cls}|${subject}`;
            const isSubjExpanded = state.expandedSubjects.has(subjectKey);
            const chapters = subjects[subject];

            let subjTotal = chapters.length;
            let subjSelected = chapters.filter(ch => state.selectedTopics.has(ch.id)).length;

            const subjectDiv = document.createElement('div');
            subjectDiv.className = 'topic-subject-group';
            subjectDiv.innerHTML = `
                <div class="topic-subject-header ${isSubjExpanded ? 'expanded' : ''}" onclick="toggleSubjectGroup('${cls}', '${subject}')">
                    <span class="topic-chevron">${isSubjExpanded ? '▾' : '▸'}</span>
                    <span class="topic-subject-name">📘 ${subject}</span>
                    <span class="topic-count-badge">${subjSelected}/${subjTotal}</span>
                    <button class="btn-select-all-mini" onclick="event.stopPropagation(); selectSubjectTopics('${cls}', '${subject}')" title="Select all chapters">✓</button>
                </div>
            `;

            // Subject body (chapters)
            const subjBody = document.createElement('div');
            subjBody.className = `topic-subject-body ${isSubjExpanded ? 'expanded' : ''}`;

            chapters.forEach(ch => {
                const isSelected = state.selectedTopics.has(ch.id);
                const chDiv = document.createElement('div');
                chDiv.className = `topic-chapter-item ${isSelected ? 'selected' : ''}`;
                chDiv.onclick = (e) => { e.stopPropagation(); toggleTopic(ch.id); };
                chDiv.innerHTML = `
                    <div class="topic-checkmark">${isSelected ? '✓' : ''}</div>
                    <div class="topic-info">
                        <div class="topic-name">Ch ${ch.chapter_number}: ${ch.chapter}</div>
                        <div class="topic-meta">${ch.topic_count} topics</div>
                    </div>
                `;
                subjBody.appendChild(chDiv);
            });

            subjectDiv.appendChild(subjBody);
            classBody.appendChild(subjectDiv);
        }

        classDiv.appendChild(classBody);
        container.appendChild(classDiv);
    }
}

function toggleClassGroup(cls) {
    if (state.expandedClasses.has(cls)) {
        state.expandedClasses.delete(cls);
    } else {
        state.expandedClasses.add(cls);
    }
    renderTopics();
}

function toggleSubjectGroup(cls, subject) {
    const key = `${cls}|${subject}`;
    if (state.expandedSubjects.has(key)) {
        state.expandedSubjects.delete(key);
    } else {
        state.expandedSubjects.add(key);
    }
    renderTopics();
}

function toggleTopic(topicId) {
    if (state.selectedTopics.has(topicId)) {
        state.selectedTopics.delete(topicId);
    } else {
        state.selectedTopics.add(topicId);
    }
    renderTopics();
}

function selectSubjectTopics(cls, subject) {
    const chapters = state.groupedTopics[cls]?.[subject] || [];
    const allSelected = chapters.every(ch => state.selectedTopics.has(ch.id));
    chapters.forEach(ch => {
        if (allSelected) {
            state.selectedTopics.delete(ch.id);
        } else {
            state.selectedTopics.add(ch.id);
        }
    });
    renderTopics();
}

function selectAllTopics() {
    for (const cls in state.groupedTopics) {
        for (const subject in state.groupedTopics[cls]) {
            state.groupedTopics[cls][subject].forEach(ch => state.selectedTopics.add(ch.id));
        }
    }
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
        title: '',
        questionType: 'mcq',
        questionCount: 10,
        marksPerQuestion: 1,
        isCompulsory: true,
        attemptCount: 10
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
        if (field === 'questionCount' || field === 'marksPerQuestion' || field === 'attemptCount') {
            section[field] = parseInt(value) || 1;
        } else if (field === 'isCompulsory') {
            section[field] = value;
            if (value) {
                section.attemptCount = section.questionCount;
            }
        } else {
            section[field] = value;
        }

        // Ensure attemptCount <= questionCount
        if (section.attemptCount > section.questionCount) {
            section.attemptCount = section.questionCount;
        }

        renderSections();
        updateTotalMarks();
    }
}

function renderSections() {
    const container = document.getElementById('sectionsContainer');
    container.innerHTML = '';

    state.sections.forEach(section => {
        const totalMarks = (section.isCompulsory ? section.questionCount : section.attemptCount) * section.marksPerQuestion;

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
                    <label>Section Title (Optional)</label>
                    <input type="text" class="form-input" placeholder="e.g. Reading Comprehension" 
                           value="${section.title || ''}"
                           onchange="updateSection(${section.id}, 'title', this.value)">
                </div>
                <div class="section-field">
                    <label>Question Type</label>
                    <select class="form-select" onchange="updateSection(${section.id}, 'questionType', this.value)">
                        ${Object.entries(QUESTION_TYPES).map(([value, label]) =>
            `<option value="${value}"${section.questionType === value ? ' selected' : ''}>${label}</option>`
        ).join('')}
                    </select>
                </div>
                <div style="display: flex; gap: 15px;">
                    <div class="section-field" style="flex: 1;">
                        <label>Total Questions</label>
                        <input type="number" class="form-input" min="1" max="50" 
                               value="${section.questionCount}"
                               onchange="updateSection(${section.id}, 'questionCount', this.value)">
                    </div>
                    <div class="section-field" style="flex: 1;">
                        <label>Marks per Question</label>
                        <input type="number" class="form-input" min="1" max="20" 
                               value="${section.marksPerQuestion}"
                               onchange="updateSection(${section.id}, 'marksPerQuestion', this.value)">
                    </div>
                </div>
                <div class="section-field">
                    <label class="checkbox-label" style="margin-bottom: 10px;">
                        <input type="checkbox" ${section.isCompulsory ? 'checked' : ''} 
                               onchange="updateSection(${section.id}, 'isCompulsory', this.checked)">
                        <span class="checkmark"></span>
                        All Questions Compulsory
                    </label>
                    ${!section.isCompulsory ? `
                        <div style="margin-top: 10px;">
                            <label>Attempt Count</label>
                            <input type="number" class="form-input" min="1" max="${section.questionCount}" 
                                   value="${section.attemptCount}"
                                   onchange="updateSection(${section.id}, 'attemptCount', this.value)">
                        </div>
                    ` : ''}
                </div>
                <div class="section-field">
                    <label>Section Total</label>
                    <div class="section-total">
                        <span class="section-total-label">${section.isCompulsory ? section.questionCount : section.attemptCount} × ${section.marksPerQuestion} =</span>
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
        return sum + ((section.isCompulsory ? section.questionCount : section.attemptCount) * section.marksPerQuestion);
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
                title: s.title,
                questionType: s.questionType,
                questionCount: s.questionCount,
                marksPerQuestion: s.marksPerQuestion,
                isCompulsory: s.isCompulsory,
                attemptCount: s.attemptCount,
                totalMarks: (s.isCompulsory ? s.questionCount : s.attemptCount) * s.marksPerQuestion
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

    const topicMeta = paper.topicMetadata && paper.topicMetadata.length > 0 ? paper.topicMetadata[0] : {};
    const subjectName = topicMeta.subject || 'Science';
    const className = topicMeta.class || 'X';
    const topicName = topicMeta.chapter || 'Various Topics';
    const timeAllowed = paper.duration || '3 hours';

    let html = `
        <div class="paper-output">
            <div class="paper-header">
                <h3>📄 Question Paper Preview</h3>
                <div class="paper-actions">
                    <button class="btn btn-primary" onclick="downloadWord()">📥 Download Word</button>
                    <button class="btn btn-secondary" onclick="printPaper()">🖨️ Print</button>
                    <button class="btn btn-secondary" onclick="copyPaper()">📋 Copy</button>
                </div>
            </div>
            <div class="paper-content" id="paperContent">
                <div style="margin-bottom: 20px; font-family: 'Times New Roman', serif;">
                    <table style="width: 100%; border: none; margin-bottom: 5px;">
                        <tr>
                            <td style="width: 33%; text-align: left; vertical-align: top;">
                                <img src="/static/jgs_logo.png" alt="Johnson Grammar School" style="max-height: 80px; width: auto;" onerror="this.style.display='none'">
                                <div style="font-size:12px; font-weight:bold; margin-top:5px; margin-left:15px;">AP018</div>
                            </td>
                            <td style="width: 33%; text-align: center; vertical-align: bottom;">
                                <div style="font-size:12px; font-weight:bold;">The Joy of being</div>
                            </td>
                            <td style="width: 33%; text-align: right; vertical-align: top;">
                                <div style="font-size:12px; font-weight:bold;">JGS/EXAM/IF-02/R01</div>
                            </td>
                        </tr>
                    </table>
                    
                    <div style="text-align: center; font-size: 18px; font-weight: bold; margin: 15px 0;">
                        ANNUAL EXAMINATION [2025-2026]
                    </div>
                    
                    <table style="width: 100%; border-collapse: collapse; text-align: center; font-size: 14px; border: 2px solid black; margin-bottom: 15px;">
                        <tr>
                            <td colspan="6" style="border: 1px solid black; padding: 8px; text-align: left; font-weight: bold; font-style: italic; border-bottom: 2px solid black;">NAME OF THE STUDENT:</td>
                        </tr>
                        <tr style="font-style: italic; font-weight: bold;">
                            <td style="border: 1px solid black; padding: 8px; width: 15%;">CL / SEC</td>
                            <td style="border: 1px solid black; padding: 8px; width: 25%;">SUBJECT</td>
                            <td style="border: 1px solid black; padding: 8px; width: 15%;">DATE</td>
                            <td style="border: 1px solid black; padding: 8px; width: 15%;">TIME</td>
                            <td style="border: 1px solid black; padding: 8px; width: 15%;">MARKS</td>
                            <td style="border: 1px solid black; padding: 8px; width: 15%;">PAGE</td>
                        </tr>
                        <tr>
                            <td style="border: 1px solid black; padding: 8px; font-weight: bold;">${className}</td>
                            <td style="border: 1px solid black; padding: 8px; font-weight: bold;">${subjectName.toUpperCase()}</td>
                            <td style="border: 1px solid black; padding: 8px; font-weight: bold;">25.02.2026</td>
                            <td style="border: 1px solid black; padding: 8px; font-weight: bold;">${timeAllowed}</td>
                            <td style="border: 1px solid black; padding: 8px; font-weight: bold;">${paper.totalMarks}</td>
                            <td style="border: 1px solid black; padding: 8px; font-weight: bold;">1 of 4</td>
                        </tr>
                    </table>
                    
                    <div style="font-size: 14px; text-align: justify; font-style: italic; font-weight: bold; margin-bottom: 20px;">
                        Instructions: Answers to this paper must be written on the paper provided separately. You will not be allowed to write during the first 15 minutes. This time is to be spent in reading the question paper. The time given at the head of the paper is the time allowed for writing the answers. Marks will be deducted if questions or bits of questions are numbered incorrectly. The intended marks for questions or parts of questions are given in brackets ( ).
                    </div>
                </div>
    `;

    // Render each section
    paper.sections.forEach(section => {
        const attemptText = section.isCompulsory !== false || section.attemptCount >= section.questions.length
            ? '(Attempt all questions from this section)'
            : `(Attempt any ${section.attemptCount} questions from this section)`;

        const marksCountLine = `(${section.isCompulsory !== false ? section.questions.length : section.attemptCount}x${section.marksPerQuestion}=${section.totalMarks}M)`;

        let sectionInstruction = "Choose the correct answers to the questions from the given options.";
        if (section.questionType === 'fill_blank') sectionInstruction = "Fill in the blanks with appropriate words.";
        else if (section.questionType === 'very_short' || section.questionType === 'short') sectionInstruction = "Answer the following questions briefly.";
        else if (section.questionType === 'long') sectionInstruction = "Answer the following questions in detail.";

        html += `
            <div class="paper-section" style="margin-top: 30px;">
                <div style="text-align: center; margin-bottom: 20px; font-family: 'Times New Roman', serif;">
                    <div style="font-weight: bold; font-size: 16px; text-decoration: underline;">
                        SECTION - ${section.name}
                    </div>
                    <div style="font-style: italic; font-weight: bold; font-size: 14px; margin-top: 5px;">
                        ${attemptText}
                    </div>
                </div>
                
                <div style="font-weight: bold; font-size: 16px; margin-bottom: 10px; font-family: 'Times New Roman', serif;">
                    Question 1
                </div>
                
                <div style="display: flex; justify-content: space-between; font-weight: bold; font-size: 16px; margin-bottom: 15px; font-family: 'Times New Roman', serif;">
                    <div>${sectionInstruction}</div>
                    <div>${marksCountLine}</div>
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

    if (q.imageUrl) {
        html += `
            <div style="text-align: center; margin: 15px 0;">
                <img src="${q.imageUrl}" style="max-height: 200px; max-width: 100%; border: 1px solid #ccc; padding: 5px; border-radius: 4px;" alt="Question Diagram" />
            </div>
        `;
    }

    if (type === 'mcq' && q.options) {
        html += '<div class="mcq-options">';
        q.options.forEach((option, idx) => {
            const letter = String.fromCharCode(97 + idx); // a, b, c, d
            const cleanOpt = option.replace(/^[\(\[]?[a-dA-D1-4][\)\].]\s*/, '').trim();
            html += `<div class="mcq-option">(${letter}) ${cleanOpt}</div>`;
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
        showToast('No paper generated yet. Please generate a paper first.', 'error');
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

        showToast('Word document downloaded successfully!', 'success');

    } catch (error) {
        console.error('Download error:', error);
        showToast('Error downloading Word document: ' + error.message, 'error');
    }
}

// ===== Toast Notification System =====

function showToast(message, type = 'success') {
    // Remove existing toast if any
    const existingToast = document.querySelector('.toast');
    if (existingToast) {
        existingToast.remove();
    }

    // Create toast element
    const toast = document.createElement('div');
    toast.className = `toast ${type} `;

    const icon = type === 'success' ? '✓' : '✕';
    toast.innerHTML = `
            < span class="toast-icon" > ${icon}</span >
                <span class="toast-message">${message}</span>
        `;

    document.body.appendChild(toast);

    // Show toast with animation
    setTimeout(() => toast.classList.add('show'), 10);

    // Auto-hide after 3 seconds
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// ===== Enhanced Copy Function =====

function copyPaper() {
    const content = document.getElementById('paperContent');
    if (content) {
        // Extract text content
        const text = content.innerText;
        navigator.clipboard.writeText(text).then(() => {
            showToast('Paper copied to clipboard!', 'success');
        }).catch(err => {
            console.error('Copy failed:', err);
            showToast('Failed to copy paper', 'error');
        });
    }
}

// ===== Keyboard Shortcuts =====

document.addEventListener('keydown', function (e) {
    // Ctrl/Cmd + G: Generate paper
    if ((e.ctrlKey || e.metaKey) && e.key === 'g') {
        e.preventDefault();
        generatePaper();
    }

    // Ctrl/Cmd + S: Download Word (when paper exists)
    if ((e.ctrlKey || e.metaKey) && e.key === 's' && state.currentPaper) {
        e.preventDefault();
        downloadWord();
    }

    // Ctrl/Cmd + P: Print paper (when paper exists)
    if ((e.ctrlKey || e.metaKey) && e.key === 'p' && state.currentPaper) {
        e.preventDefault();
        printPaper();
    }

    // Ctrl/Cmd + Shift + A: Add new section
    if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === 'A') {
        e.preventDefault();
        addSection();
    }
});

// ===== Paper Preset Templates =====

function applyPreset(presetName) {
    // Clear existing sections
    state.sections = [];
    state.nextSectionIndex = 0;

    switch (presetName) {
        case 'cbse_standard':
            // CBSE standard pattern
            addSectionWithConfig('mcq', 20, 1);        // Section A: 20 MCQs, 1 mark each
            addSectionWithConfig('fill_blank', 5, 1);   // Section B: 5 fill-blanks, 1 mark
            addSectionWithConfig('very_short', 5, 2);   // Section C: 5 very short, 2 marks
            addSectionWithConfig('short', 5, 3);        // Section D: 5 short, 3 marks
            addSectionWithConfig('long', 3, 5);         // Section E: 3 long, 5 marks
            break;

        case 'quick_test':
            // Quick classroom test
            addSectionWithConfig('mcq', 10, 1);
            addSectionWithConfig('short', 5, 2);
            break;

        case 'comprehensive':
            // All question types
            addSectionWithConfig('mcq', 15, 1);
            addSectionWithConfig('fill_blank', 10, 1);
            addSectionWithConfig('very_short', 8, 2);
            addSectionWithConfig('short', 6, 3);
            addSectionWithConfig('long', 4, 5);
            break;
    }

    showToast(`Applied ${presetName.replace('_', ' ')} template`, 'success');
}

function addSectionWithConfig(questionType, questionCount, marksPerQuestion) {
    const letter = state.sectionLetters[state.nextSectionIndex] || `S${state.nextSectionIndex + 1} `;

    const section = {
        id: Date.now() + state.nextSectionIndex,
        name: letter,
        questionType: questionType,
        questionCount: questionCount,
        marksPerQuestion: marksPerQuestion
    };

    state.sections.push(section);
    state.nextSectionIndex++;

    renderSections();
    updateTotalMarks();
}

// ===== Statistics Display =====

function updateStats() {
    const totalQuestions = state.sections.reduce((sum, s) => sum + s.questionCount, 0);
    const totalMarks = state.sections.reduce((sum, s) => sum + (s.questionCount * s.marksPerQuestion), 0);
    const sectionCount = state.sections.length;

    // Update UI if stats elements exist
    const statsDisplay = document.getElementById('paperStats');
    if (statsDisplay) {
        statsDisplay.innerHTML = `
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-value">${totalQuestions}</div>
                    <div class="stat-label">Questions</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${totalMarks}</div>
                    <div class="stat-label">Total Marks</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${sectionCount}</div>
                    <div class="stat-label">Sections</div>
                </div>
            </div>
            `;
    }
}

// ===== Progress Tracking =====

function showProgress(current, total, message) {
    const progressContainer = document.getElementById('progressContainer');
    if (progressContainer) {
        const percent = (current / total) * 100;
        progressContainer.innerHTML = `
            <div class="progress-info">${message}</div>
                <div class="progress-bar">
                    <div class="progress-bar-fill" style="width: ${percent}%"></div>
                </div>
        `;
    }
}

// ===== Enhanced Paper Generation with Progress =====

async function generatePaperWithProgress() {
    await generatePaper();
}
