import sys

path = 'c:\\Users\\karth\\OneDrive\\Desktop\\my code\\vedlinks 1 final - trail 1\\templates\\practice.html'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 1. replace `<style>` tag down to `</style>` with `<link rel="stylesheet" href="/static/practice.css">`
start_style = -1
end_style = -1
for i, line in enumerate(lines):
    if '<style>' in line:
        start_style = i
    if '</style>' in line:
        end_style = i
        break

if start_style != -1 and end_style != -1:
    lines = lines[:start_style] + ['    <link rel="stylesheet" href="/static/practice.css">\n'] + lines[end_style+1:]

# 2. replace nav-bar with the standard header block
nav_start = -1
nav_end = -1
for i, line in enumerate(lines):
    if '<nav class="nav-bar">' in line:
        nav_start = i
    if '</nav>' in line and nav_start != -1:
        nav_end = i
        break

new_header = """    <div class="app-container">
        <!-- Header -->
        <header class="header">
            <div class="header-content">
                <div class="logo">
                    <span class="logo-icon">🎯</span>
                    <div class="logo-text">
                        <h1>VedLinks</h1>
                        <span class="tagline" data-i18n="tagline_practice">Practice & Clear Doubts</span>
                    </div>
                </div>
                <nav class="nav-links-container">
                    <a href="/" class="nav-link">📝 <span data-i18n="nav_question_paper">Question Paper</span></a>
                    <a href="/lesson-planner" class="nav-link">📋 <span data-i18n="nav_lesson_planner">Lesson Planner</span></a>
                    <a href="/upload" class="nav-link">📤 <span data-i18n="nav_upload">Upload Textbook</span></a>
                    <a href="/practice" class="nav-link active">🎯 <span data-i18n="nav_practice">Practice & Doubts</span></a>
                    <select id="langSwitcher" class="lang-switcher" onchange="VedLinksI18n.setLanguage(this.value)">
                        <option value="en">🇬🇧 English</option>
                        <option value="te">🇮🇳 తెలుగు</option>
                        <option value="hi">🇮🇳 हिन्दी</option>
                        <option value="mr">🇮🇳 मराठी</option>
                        <option value="ta">🇮🇳 தமிழ்</option>
                        <option value="kn">🇮🇳 ಕನ್ನಡ</option>
                    </select>
                </nav>
            </div>
        </header>

        <!-- Main Content -->
        <main class="main-content">
"""

if nav_start != -1 and nav_end != -1:
    lines = lines[:nav_start] + [new_header] + lines[nav_end+1:]

# 3. Add closing tags for main and app-container before <script src="/static/i18n.js">
script_idx = -1
for i, line in enumerate(lines):
    if '<script src="/static/i18n.js"></script>' in line:
        script_idx = i
        break

if script_idx != -1:
    lines = lines[:script_idx] + ['        </main>\n    </div>\n\n'] + lines[script_idx:]

# Ensure no `style="background: rgba(255,255,255,0.2);"` overrides in other places
for i, line in enumerate(lines):
    if 'style="background: rgba(255,255,255,0.2);"' in line:
        lines[i] = line.replace('style="background: rgba(255,255,255,0.2);"', '')

# Also let's fix the practiceLangSelect styling override
for i, line in enumerate(lines):
    if '<select id="practiceLangSelect"' in line:
        continue
    if 'style="padding:8px 12px;' in line and '#f5f3ff' in line:
        lines[i] = '                        style="padding:8px 12px; border-radius:8px; border:1px solid var(--border-color); background:var(--bg-secondary); color:var(--text-primary); font-weight:600; font-size:0.9rem; cursor:pointer;">\n'
        
# Fix the generated results background logic to match dark theme too
for i, line in enumerate(lines):
    if 'background: #f8f9fa;' in line:
        lines[i] = line.replace('background: #f8f9fa;', 'background: var(--bg-card); border: 1px solid var(--border-color);')
    if 'background: white;' in line:
        lines[i] = line.replace('background: white;', 'background: var(--bg-secondary);')

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Updated practice.html successfully.")
