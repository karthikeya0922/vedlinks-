# -*- coding: utf-8 -*-
import requests
import time

langs = ['en', 'te', 'hi', 'mr', 'ta']
lang_names = {'en': 'English', 'te': 'Telugu', 'hi': 'Hindi', 'mr': 'Marathi', 'ta': 'Tamil'}

topics = requests.get('http://127.0.0.1:5000/api/topics').json()['topics']
t = topics[0]
print(f"Testing with topic: {t['name']}\n")

results = {}
for lang in langs:
    print(f"Testing {lang_names[lang]} ({lang})...")
    resp = requests.post('http://127.0.0.1:5000/api/generate-lesson-plan', json={
        'teacherName': 'Test Teacher',
        'schoolName': 'Test School',
        'chapterId': t['id'],
        'chapterName': t['name'],
        'grade': '10',
        'subject': 'Science',
        'periodsCount': 1,
        'periodDuration': 40,
        'lang': lang
    }, timeout=90)
    plan = resp.json()['lessonPlan']
    phase = plan['phases'][0]
    results[lang] = {
        'phaseName': phase['name'],
        'learningOutcome': phase['learningOutcome'][:80],
        'teacherAct': phase['teacherActivities'][0],
        'methodology': phase['methodology'][0],
        'values': plan['values'][:70],
        'realLife': plan['realLifeApplication'][:70],
    }
    time.sleep(1)

print()
print('=' * 70)
print('FULL 5-LANGUAGE TEST RESULTS')
print('=' * 70)
for lang in langs:
    r = results[lang]
    english_count = sum(
        1 for s in [r['learningOutcome'], r['teacherAct'], r['values']]
        if all(ord(c) < 128 for c in s if c.isalpha())
    )
    status = 'PASS' if (lang == 'en' or english_count == 0) else 'FAIL (still English)'
    print()
    print(f"--- {lang_names[lang]} ({lang}) [{status}] ---")
    print(f"  Phase Name  : {r['phaseName']}")
    print(f"  Outcome     : {r['learningOutcome']}")
    print(f"  Teacher Act : {r['teacherAct']}")
    print(f"  Methodology : {r['methodology']}")
    print(f"  Values      : {r['values']}")
    print(f"  Real Life   : {r['realLife']}")

print()
pass_count = sum(1 for lang in langs if (lang == 'en' or sum(
    1 for s in [results[lang]['learningOutcome'], results[lang]['teacherAct'], results[lang]['values']]
    if all(ord(c) < 128 for c in s if c.isalpha())
) == 0))
print(f"OVERALL: {pass_count}/{len(langs)} languages PASSED")
