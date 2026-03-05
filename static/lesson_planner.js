/**
 * VedLinks AI Lesson Plan Generator - Frontend Logic
 */

// State Management
const lessonState = {
    chapters: [],
    currentPlan: null
};

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    loadChapters();
    setDefaultDate();
    loadSavedTeacherInfo();
});

// ===== Chapter Loading =====

async function loadChapters() {
    try {
        const response = await fetch('/api/topics');
        const data = await response.json();

        if (data.success && data.topics.length > 0) {
            lessonState.chapters = data.topics;
            renderChapterOptions();
        }
    } catch (error) {
        console.error('Error loading chapters:', error);
    }
}

function renderChapterOptions() {
    const select = document.getElementById('chapterSelect');
    select.innerHTML = '<option value="">Select Chapter...</option>';

    lessonState.chapters.forEach(chapter => {
        const option = document.createElement('option');
        option.value = chapter.id;
        option.textContent = chapter.name;
        select.appendChild(option);
    });
}

// ===== Form Helpers =====

function setDefaultDate() {
    const dateInput = document.getElementById('lessonDate');
    const today = new Date().toISOString().split('T')[0];
    dateInput.value = today;
}

function loadSavedTeacherInfo() {
    const savedInfo = localStorage.getItem('vedlinks_teacher_info');
    if (savedInfo) {
        const info = JSON.parse(savedInfo);
        document.getElementById('teacherName').value = info.teacherName || '';
        document.getElementById('schoolName').value = info.schoolName || '';
        document.getElementById('designation').value = info.designation || '';
    }
}

function saveTeacherInfo() {
    const info = {
        teacherName: document.getElementById('teacherName').value,
        schoolName: document.getElementById('schoolName').value,
        designation: document.getElementById('designation').value
    };
    localStorage.setItem('vedlinks_teacher_info', JSON.stringify(info));
}

// ===== Lesson Plan Generation =====

async function generateLessonPlan() {
    // Validation
    const chapterId = document.getElementById('chapterSelect').value;
    if (!chapterId) {
        showToast('Please select a chapter', 'error');
        return;
    }

    const teacherName = document.getElementById('teacherName').value;
    const schoolName = document.getElementById('schoolName').value;

    if (!teacherName || !schoolName) {
        showToast('Please enter teacher and school name', 'error');
        return;
    }

    // Save teacher info for future use
    saveTeacherInfo();

    // Show loading overlay
    const overlay = document.getElementById('loadingOverlay');
    const statusText = document.getElementById('loadingStatus');
    overlay.classList.add('active');

    const generateBtn = document.getElementById('generateBtn');
    generateBtn.disabled = true;

    try {
        statusText.textContent = 'Preparing lesson plan template...';

        // Build configuration
        const config = {
            teacherName: teacherName,
            schoolName: schoolName,
            designation: document.getElementById('designation').value,
            grade: document.getElementById('gradeSelect').value,
            subject: document.getElementById('subjectSelect').value,
            chapterId: chapterId,
            chapterName: document.getElementById('chapterSelect').options[document.getElementById('chapterSelect').selectedIndex].text,
            topic: document.getElementById('topicInput').value || 'Complete Chapter Overview',
            date: document.getElementById('lessonDate').value,
            planNumber: document.getElementById('planNumber').value,
            periodsCount: document.getElementById('periodsCount').value,
            periodDuration: document.getElementById('periodDuration').value
        };

        statusText.textContent = 'Generating lesson plan...';

        // Generate lesson plan
        const response = await fetch('/api/generate-lesson-plan', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(config)
        });

        const data = await response.json();

        if (data.success) {
            statusText.textContent = 'Rendering lesson plan...';
            renderLessonPlan(data.lessonPlan);
            showToast('Lesson plan generated successfully!', 'success');
        } else {
            throw new Error(data.error || 'Failed to generate lesson plan');
        }

    } catch (error) {
        console.error('Generation error:', error);
        showToast('Error generating lesson plan: ' + error.message, 'error');
    } finally {
        overlay.classList.remove('active');
        generateBtn.disabled = false;
    }
}

// ===== Lesson Plan Rendering =====

function renderLessonPlan(plan) {
    const outputPanel = document.getElementById('outputPanel');
    lessonState.currentPlan = plan;

    const formattedDate = new Date(plan.date).toLocaleDateString('en-IN', {
        day: 'numeric',
        month: 'long',
        year: 'numeric'
    });

    let html = `
        <div class="lesson-plan-output">
            <div class="lesson-plan-header">
                <h3>📋 Lesson Plan - ${plan.subject}</h3>
                <div class="lesson-plan-actions">
                    <button class="btn btn-primary" onclick="downloadLessonPlanWord()">📥 Download Word</button>
                    <button class="btn btn-secondary" onclick="printLessonPlan()">🖨️ Print</button>
                </div>
            </div>
            <div class="lesson-plan-content">
                <div class="lesson-plan-document">
                    <!-- School Header -->
                    <div class="lp-school-header">
                        <div class="lp-school-name">${plan.schoolName}</div>
                        <div class="lp-school-subtitle">LESSON PLAN ${plan.date ? `(${formattedDate})` : ''}</div>
                    </div>
                    
                    <!-- Info Grid -->
                    <div class="lp-info-grid">
                        <div class="lp-info-item">
                            <span class="lp-info-label">Teacher:</span>
                            <span class="lp-info-value">${plan.teacherName}</span>
                        </div>
                        <div class="lp-info-item">
                            <span class="lp-info-label">Grade:</span>
                            <span class="lp-info-value">Class ${plan.grade}</span>
                        </div>
                        <div class="lp-info-item">
                            <span class="lp-info-label">Subject:</span>
                            <span class="lp-info-value">${plan.subject}</span>
                        </div>
                        <div class="lp-info-item">
                            <span class="lp-info-label">Periods:</span>
                            <span class="lp-info-value">${plan.periodsCount} (${plan.periodDuration} min each)</span>
                        </div>
                        <div class="lp-info-item">
                            <span class="lp-info-label">Lesson:</span>
                            <span class="lp-info-value">${plan.chapterName}</span>
                        </div>
                        <div class="lp-info-item">
                            <span class="lp-info-label">Plan No:</span>
                            <span class="lp-info-value">${plan.planNumber}</span>
                        </div>
                        <div class="lp-info-item" style="grid-column: span 2;">
                            <span class="lp-info-label">Topic:</span>
                            <span class="lp-info-value">${plan.topic}</span>
                        </div>
                    </div>
                    
                    <!-- Pre-requisite Knowledge -->
                    <div class="lp-section">
                        <div class="lp-section-title">PRE-REQUISITE KNOWLEDGE</div>
                        <ul class="lp-prereq-list">
                            ${plan.prerequisiteKnowledge.map(item => `<li>${item}</li>`).join('')}
                        </ul>
                    </div>
                    
                    <!-- Main Teaching Table -->
                    <div class="lp-section">
                        <div class="lp-section-title">LESSON PLAN DETAILS</div>
                        <div class="lp-table-container">
                            <table class="lp-table">
                                <thead>
                                    <tr>
                                        <th>Duration</th>
                                        <th>Learning Outcome</th>
                                        <th>Methodology/Strategy</th>
                                        <th>Teaching Aids</th>
                                        <th>Teacher Activities</th>
                                        <th>Learner Activities</th>
                                        <th>Assessment</th>
                                        <th>Home Assignment</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    ${renderPhaseRows(plan.phases)}
                                </tbody>
                            </table>
                        </div>
                    </div>
                    
                    <!-- Footer Sections -->
                    <div class="lp-footer-section">
                        <div class="lp-footer-label">VALUES DEALT IN THE LESSON (VD):</div>
                        <div class="lp-footer-content">${plan.values}</div>
                    </div>
                    
                    <div class="lp-footer-section">
                        <div class="lp-footer-label">REAL LIFE APPLICATION (RL):</div>
                        <div class="lp-footer-content">${plan.realLifeApplication}</div>
                    </div>
                    
                    <div class="lp-footer-section">
                        <div class="lp-footer-label">CROSS CURRICULAR CONNECTION (CC):</div>
                        <div class="lp-footer-content">${plan.crossCurricular}</div>
                    </div>
                    
                    ${plan.extendedTask ? `
                    <div class="lp-footer-section">
                        <div class="lp-footer-label">EXTENDED TASK:</div>
                        <div class="lp-footer-content">${plan.extendedTask}</div>
                    </div>
                    ` : ''}
                    
                    <!-- Signatures -->
                    <div class="lp-signatures">
                        <div class="lp-signature-box">
                            <div class="lp-signature-line">Signature of Subject Teacher</div>
                        </div>
                        <div class="lp-signature-box">
                            <div class="lp-signature-line">Signature of HOD</div>
                        </div>
                        <div class="lp-signature-box">
                            <div class="lp-signature-line">Signature of Principal</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;

    outputPanel.innerHTML = html;
}

function renderPhaseRows(phases) {
    return phases.map(phase => `
        <tr>
            <td class="lp-phase-cell">
                <strong>${phase.name}</strong><br>
                <span class="lp-duration-badge">${phase.duration}</span>
            </td>
            <td>${phase.learningOutcome}</td>
            <td>
                ${phase.methodology.map(m => `<span class="lp-method-tag">${m}</span>`).join('')}
            </td>
            <td>
                ${phase.teachingAids.map(aid => `<span class="lp-aid-badge">📚 ${aid}</span>`).join('')}
            </td>
            <td>
                <ul class="lp-activity-list">
                    ${phase.teacherActivities.map(a => `<li>${a}</li>`).join('')}
                </ul>
            </td>
            <td>
                <ul class="lp-activity-list">
                    ${phase.learnerActivities.map(a => `<li>${a}</li>`).join('')}
                </ul>
            </td>
            <td>${phase.assessment}</td>
            <td>${phase.homeAssignment || '-'}</td>
        </tr>
    `).join('');
}

// ===== Export Functions =====

async function downloadLessonPlanWord() {
    if (!lessonState.currentPlan) {
        showToast('No lesson plan generated yet', 'error');
        return;
    }

    try {
        const response = await fetch('/api/export-lesson-plan-docx', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ lessonPlan: lessonState.currentPlan })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Export failed');
        }

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `lesson_plan_${lessonState.currentPlan.chapterName.replace(/[^a-z0-9]/gi, '_')}_${new Date().toISOString().slice(0, 10)}.docx`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);

        showToast('Lesson plan downloaded successfully!', 'success');

    } catch (error) {
        console.error('Download error:', error);
        showToast('Error downloading: ' + error.message, 'error');
    }
}

function printLessonPlan() {
    const content = document.querySelector('.lesson-plan-document');
    if (content) {
        const printWindow = window.open('', '_blank');
        printWindow.document.write(`
            <html>
            <head>
                <title>Lesson Plan - ${lessonState.currentPlan.chapterName}</title>
                <style>
                    body { font-family: Arial, sans-serif; padding: 20px; }
                    .lp-school-header { text-align: center; margin-bottom: 20px; border-bottom: 2px solid #333; padding-bottom: 10px; }
                    .lp-school-name { font-size: 24px; font-weight: bold; }
                    .lp-info-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 20px; padding: 10px; border: 1px solid #ddd; }
                    .lp-info-item { display: flex; gap: 8px; }
                    .lp-info-label { font-weight: bold; min-width: 80px; }
                    .lp-section-title { font-weight: bold; background: #f0f0f0; padding: 8px 12px; margin-bottom: 10px; }
                    .lp-table { width: 100%; border-collapse: collapse; font-size: 11px; }
                    .lp-table th, .lp-table td { border: 1px solid #333; padding: 8px; text-align: left; vertical-align: top; }
                    .lp-table th { background: #f0f0f0; font-weight: bold; }
                    .lp-footer-section { margin-bottom: 10px; padding: 10px; border-left: 3px solid #333; background: #f9f9f9; }
                    .lp-footer-label { font-weight: bold; margin-bottom: 5px; }
                    .lp-signatures { display: flex; justify-content: space-between; margin-top: 40px; padding-top: 20px; border-top: 2px dashed #999; }
                    .lp-signature-box { text-align: center; width: 30%; }
                    .lp-signature-line { border-top: 1px solid #333; padding-top: 5px; margin-top: 50px; }
                    .lp-prereq-list, .lp-activity-list { margin: 0; padding-left: 20px; }
                    .lp-method-tag, .lp-aid-badge { display: inline-block; padding: 2px 6px; margin: 2px; font-size: 10px; background: #eee; border-radius: 3px; }
                    .lp-duration-badge { display: inline-block; padding: 2px 6px; background: #333; color: white; border-radius: 3px; font-size: 10px; }
                    @media print { body { -webkit-print-color-adjust: exact; } }
                </style>
            </head>
            <body>${content.innerHTML}</body>
            </html>
        `);
        printWindow.document.close();
        printWindow.print();
    }
}

// ===== Toast Notification =====

function showToast(message, type = 'success') {
    const existingToast = document.querySelector('.toast');
    if (existingToast) {
        existingToast.remove();
    }

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
