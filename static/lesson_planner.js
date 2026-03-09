/**
 * VedLinks AI Lesson Plan Generator - Frontend Logic
 */

// Output language labels for the rendered lesson plan (independent from UI language)
const LP_LABELS = {
    en: {
        prereq: 'PRE-REQUISITE KNOWLEDGE',
        details: 'LESSON PLAN DETAILS',
        duration: 'Duration', outcome: 'Learning Outcome', methodology: 'Methodology/Strategy',
        aids: 'Teaching Aids', teacher_act: 'Teacher Activities', learner_act: 'Learner Activities',
        assessment: 'Assessment', homework: 'Home Assignment',
        values: 'VALUES DEALT IN THE LESSON (VD):',
        reallife: 'REAL LIFE APPLICATION (RL):',
        crosscurr: 'CROSS CURRICULAR CONNECTION (CC):', extended: 'EXTENDED TASK:',
        sig_teacher: 'Signature of Subject Teacher', sig_hod: 'Signature of HOD', sig_principal: 'Signature of Principal',
        lbl_teacher: 'Teacher:', lbl_grade: 'Grade:', lbl_subject: 'Subject:',
        lbl_periods: 'Periods:', lbl_lesson: 'Lesson:', lbl_plan: 'Plan No:', lbl_topic: 'Topic:',
        lbl_class: 'Class', lbl_lesson_plan: 'Lesson Plan',
        download: '📥 Download Word', print: '🖨️ Print'
    },
    te: {
        prereq: 'అవసరమైన అర్హత జ్ఞానం',
        details: 'పాఠ్య ప్రణాళిక వివరాలు',
        duration: 'వ్యవధి', outcome: 'అభ్యాస ఫలితం', methodology: 'బోధన పద్ధతి/వ్యూహం',
        aids: 'బోధన సహాయాలు', teacher_act: 'ఉపాధ్యాయుని కార్యకలాపాలు', learner_act: 'విద్యార్థి కార్యకలాపాలు',
        assessment: 'మూల్యాంకనం', homework: 'గృహపాఠం',
        values: 'పాఠంలో చర్చించిన విలువలు:', reallife: 'నిజ జీవిత అనువర్తనం:',
        crosscurr: 'అంతర్-విషయ సంబంధం:', extended: 'విస్తరించిన పని:',
        sig_teacher: 'సబ్జెక్ట్ ఉపాధ్యాయుని సంతకం', sig_hod: 'HOD సంతకం', sig_principal: 'ప్రిన్సిపల్ సంతకం',
        lbl_teacher: 'ఉపాధ్యాయుడు:', lbl_grade: 'తరగతి:', lbl_subject: 'సబ్జెక్ట్:',
        lbl_periods: 'పిరియడ్లు:', lbl_lesson: 'పాఠం:', lbl_plan: 'ప్రణాళిక నం:', lbl_topic: 'అంశం:',
        lbl_class: 'తరగతి', lbl_lesson_plan: 'పాఠ్య ప్రణాళిక',
        download: '📥 వర్డ్ డౌన్‌లోడ్', print: '🖨️ ముద్రించు'
    },
    hi: {
        prereq: 'पूर्व-आवश्यक ज्ञान',
        details: 'पाठ योजना विवरण',
        duration: 'अवधि', outcome: 'सीखने का परिणाम', methodology: 'शिक्षण पद्धति/रणनीति',
        aids: 'शिक्षण सामग्री', teacher_act: 'शिक्षक गतिविधियाँ', learner_act: 'छात्र गतिविधियाँ',
        assessment: 'मूल्यांकन', homework: 'गृहकार्य',
        values: 'पाठ में संबोधित मूल्य:', reallife: 'वास्तविक जीवन अनुप्रयोग:',
        crosscurr: 'अंतर-विषय संबंध:', extended: 'विस्तारित कार्य:',
        sig_teacher: 'विषय शिक्षक के हस्ताक्षर', sig_hod: 'HOD के हस्ताक्षर', sig_principal: 'प्रधानाचार्य के हस्ताक्षर',
        lbl_teacher: 'शिक्षक:', lbl_grade: 'कक्षा:', lbl_subject: 'विषय:',
        lbl_periods: 'कालांश:', lbl_lesson: 'पाठ:', lbl_plan: 'योजना क्र.:', lbl_topic: 'विषय:',
        lbl_class: 'कक्षा', lbl_lesson_plan: 'पाठ योजना',
        download: '📥 वर्ड डाउनलोड', print: '🖨️ प्रिंट करें'
    },
    mr: {
        prereq: 'पूर्व-ज्ञान',
        details: 'पाठ योजना तपशील',
        duration: 'कालावधी', outcome: 'शिक्षण परिणाम', methodology: 'शिक्षण पद्धती/रणनीती',
        aids: 'शिक्षण साधने', teacher_act: 'शिक्षक उपक्रम', learner_act: 'विद्यार्थी उपक्रम',
        assessment: 'मूल्यमापन', homework: 'गृहपाठ',
        values: 'पाठातील मूल्ये:', reallife: 'वास्तव जीवनातील उपयोजन:',
        crosscurr: 'आंतर-विषय संबंध:', extended: 'विस्तारित कार्य:',
        sig_teacher: 'विषय शिक्षकाची सही', sig_hod: 'HOD ची सही', sig_principal: 'मुख्याध्यापकाची सही',
        lbl_teacher: 'शिक्षक:', lbl_grade: 'इयत्ता:', lbl_subject: 'विषय:',
        lbl_periods: 'तास:', lbl_lesson: 'पाठ:', lbl_plan: 'योजना क्र.:', lbl_topic: 'विषय:',
        lbl_class: 'इयत्ता', lbl_lesson_plan: 'पाठ योजना',
        download: '📥 वर्ड डाउनलोड', print: '🖨️ प्रिंट करा'
    },
    ta: {
        prereq: 'முன் தேவையான அறிவு',
        details: 'பாட திட்ட விவரங்கள்',
        duration: 'கால அளவு', outcome: 'கற்றல் விளைவு', methodology: 'கற்பித்தல் முறை/உத்தி',
        aids: 'கற்பித்தல் உதவிகள்', teacher_act: 'ஆசிரியர் செயல்பாடுகள்', learner_act: 'மாணவர் செயல்பாடுகள்',
        assessment: 'மதிப்பீடு', homework: 'வீட்டுப்பாடம்',
        values: 'பாடத்தில் கூறப்பட்ட மதிப்புகள்:', reallife: 'நிஜ வாழ்க்கை பயன்பாடு:',
        crosscurr: 'பாட இணைப்புகள்:', extended: 'நீட்டிக்கப்பட்ட பணி:',
        sig_teacher: 'பாட ஆசிரியர் கையொப்பம்', sig_hod: 'HOD கையொப்பம்', sig_principal: 'அதிபர் கையொப்பம்',
        lbl_teacher: 'ஆசிரியர்:', lbl_grade: 'வகுப்பு:', lbl_subject: 'பாடம்:',
        lbl_periods: 'பாட நேரம்:', lbl_lesson: 'பாடம்:', lbl_plan: 'திட்ட எண்:', lbl_topic: 'தலைப்பு:',
        lbl_class: 'வகுப்பு', lbl_lesson_plan: 'பாட திட்டம்',
        download: '📥 வேர்ட் பதிவிறக்கம்', print: '🖨️ அச்சிடு'
    },
    kn: {
        prereq: 'ಪೂರ್ವ-ಅಗತ್ಯ ಜ್ಞಾನ',
        details: 'ಪಾಠ ಯೋಜನೆ ವಿವರಗಳು',
        duration: 'ಅವಧಿ', outcome: 'ಕಲಿಕಾ ಫಲಿತಾಂಶ', methodology: 'ಬೋಧನಾ ವಿಧಾನ/ತಂತ್ರ',
        aids: 'ಬೋಧನಾ ಸಾಧನಗಳು', teacher_act: 'ಶಿಕ್ಷಕ ಚಟುವಟಿಕೆಗಳು', learner_act: 'ವಿದ್ಯಾರ್ಥಿ ಚಟುವಟಿಕೆಗಳು',
        assessment: 'ಮೌಲ್ಯಮಾಪನ', homework: 'ಗೃಹಕಾರ್ಯ',
        values: 'ಪಾಠದಲ್ಲಿ ಸಂಬೋಧಿಸಿದ ಮೌಲ್ಯಗಳು:', reallife: 'ನಿಜ ಜೀವನ ಅನ್ವಯ:',
        crosscurr: 'ಅಂತರ ಪಠ್ಯ ಸಂಪರ್ಕ:', extended: 'ವಿಸ್ತರಿತ ಕಾರ್ಯ:',
        sig_teacher: 'ವಿಷಯ ಶಿಕ್ಷಕರ ಸಹಿ', sig_hod: 'HOD ಸಹಿ', sig_principal: 'ಪ್ರಾಂಶುಪಾಲರ ಸಹಿ',
        lbl_teacher: 'ಶಿಕ್ಷಕ:', lbl_grade: 'ತರಗತಿ:', lbl_subject: 'ವಿಷಯ:',
        lbl_periods: 'ಅವಧಿಗಳು:', lbl_lesson: 'ಪಾಠ:', lbl_plan: 'ಯೋಜನೆ ಸಂ.:', lbl_topic: 'ವಿಷಯ:',
        lbl_class: 'ತರಗತಿ', lbl_lesson_plan: 'ಪಾಠ ಯೋಜನೆ',
        download: '📥 ವರ್ಡ್ ಡೌನ್‌ಲೋಡ್', print: '🖨️ ಮುದ್ರಿಸಿ'
    }
};

function getOutputLang() {
    const sel = document.getElementById('outputLangSelect');
    return (sel ? sel.value : null) || (window.VedLinksI18n ? window.VedLinksI18n.getCurrentLang() : 'en');
}

function lp(key) {
    const lang = getOutputLang();
    return (LP_LABELS[lang] || LP_LABELS['en'])[key] || LP_LABELS['en'][key];
}

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
            periodDuration: document.getElementById('periodDuration').value,
            lang: (document.getElementById('outputLangSelect') ? document.getElementById('outputLangSelect').value : 'en')
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
                <h3>📋 ${lp('lbl_lesson_plan')} - ${plan.subject}</h3>
                <div class="lesson-plan-actions">
                    <button class="btn btn-primary" onclick="downloadLessonPlanWord()">${lp('download')}</button>
                    <button class="btn btn-secondary" onclick="printLessonPlan()">${lp('print')}</button>
                </div>
            </div>
            <div class="lesson-plan-content">
                <div class="lesson-plan-document">
                    <!-- School Header -->
                    <div class="lp-school-header">
                        <div class="lp-school-name">${plan.schoolName}</div>
                        <div class="lp-school-subtitle">${lp('lbl_lesson_plan').toUpperCase()} ${plan.date ? `(${formattedDate})` : ''}</div>
                    </div>
                    
                    <!-- Info Grid -->
                    <div class="lp-info-grid">
                        <div class="lp-info-item">
                            <span class="lp-info-label">${lp('lbl_teacher')}</span>
                            <span class="lp-info-value">${plan.teacherName}</span>
                        </div>
                        <div class="lp-info-item">
                            <span class="lp-info-label">${lp('lbl_grade')}</span>
                            <span class="lp-info-value">${lp('lbl_class')} ${plan.grade}</span>
                        </div>
                        <div class="lp-info-item">
                            <span class="lp-info-label">${lp('lbl_subject')}</span>
                            <span class="lp-info-value">${plan.subject}</span>
                        </div>
                        <div class="lp-info-item">
                            <span class="lp-info-label">${lp('lbl_periods')}</span>
                            <span class="lp-info-value">${plan.periodsCount} (${plan.periodDuration} min each)</span>
                        </div>
                        <div class="lp-info-item">
                            <span class="lp-info-label">${lp('lbl_lesson')}</span>
                            <span class="lp-info-value">${plan.chapterName}</span>
                        </div>
                        <div class="lp-info-item">
                            <span class="lp-info-label">${lp('lbl_plan')}</span>
                            <span class="lp-info-value">${plan.planNumber}</span>
                        </div>
                        <div class="lp-info-item" style="grid-column: span 2;">
                            <span class="lp-info-label">${lp('lbl_topic')}</span>
                            <span class="lp-info-value">${plan.topic}</span>
                        </div>
                    </div>
                    
                    <!-- Pre-requisite Knowledge -->
                    <div class="lp-section">
                        <div class="lp-section-title">${lp('prereq')}</div>
                        <ul class="lp-prereq-list">
                            ${plan.prerequisiteKnowledge.map(item => `<li>${item}</li>`).join('')}
                        </ul>
                    </div>
                    
                    <!-- Main Teaching Table -->
                    <div class="lp-section">
                        <div class="lp-section-title">${lp('details')}</div>
                        <div class="lp-table-container">
                            <table class="lp-table">
                                <thead>
                                    <tr>
                                        <th>${lp('duration')}</th>
                                        <th>${lp('outcome')}</th>
                                        <th>${lp('methodology')}</th>
                                        <th>${lp('aids')}</th>
                                        <th>${lp('teacher_act')}</th>
                                        <th>${lp('learner_act')}</th>
                                        <th>${lp('assessment')}</th>
                                        <th>${lp('homework')}</th>
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
                        <div class="lp-footer-label">${lp('values')}</div>
                        <div class="lp-footer-content">${plan.values}</div>
                    </div>
                    
                    <div class="lp-footer-section">
                        <div class="lp-footer-label">${lp('reallife')}</div>
                        <div class="lp-footer-content">${plan.realLifeApplication}</div>
                    </div>
                    
                    <div class="lp-footer-section">
                        <div class="lp-footer-label">${lp('crosscurr')}</div>
                        <div class="lp-footer-content">${plan.crossCurricular}</div>
                    </div>
                    
                    ${plan.extendedTask ? `
                    <div class="lp-footer-section">
                        <div class="lp-footer-label">${lp('extended')}</div>
                        <div class="lp-footer-content">${plan.extendedTask}</div>
                    </div>
                    ` : ''}
                    
                    <!-- Signatures -->
                    <div class="lp-signatures">
                        <div class="lp-signature-box">
                            <div class="lp-signature-line">${lp('sig_teacher')}</div>
                        </div>
                        <div class="lp-signature-box">
                            <div class="lp-signature-line">${lp('sig_hod')}</div>
                        </div>
                        <div class="lp-signature-box">
                            <div class="lp-signature-line">${lp('sig_principal')}</div>
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
            body: JSON.stringify({ lessonPlan: lessonState.currentPlan, lang: getOutputLang() })
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
