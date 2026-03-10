import urllib.request, json
import time

try:
    req = urllib.request.Request('http://localhost:5000/api/topics')
    with urllib.request.urlopen(req) as res:
        data = json.loads(res.read().decode('utf-8'))
        
        # Find a topic that likely has no knowledge bank (e.g. from uploaded PDFs)
        topic_id = None
        topic_chap = None
        for t in data['topics']:
            if t['source'] == 'registry' or t['source'] == 'topic_file':
                # Skip the default biology ones which we know have KB
                if 'How do organisms reproduce' in t['chapter'] or 'Our Environment' in t['chapter']:
                    topic_id = t['id']
                    topic_chap = t['chapter']
                    break
        
        if not topic_id:
            topic_id = data['topics'][1]['id']
            topic_chap = data['topics'][1]['chapter']
            
        print('Testing Topic:', topic_chap, '(', topic_id, ')')

    start = time.time()
    req2 = urllib.request.Request(
        'http://localhost:5000/api/concepts',
        data=json.dumps({'topicId': topic_id, 'lang': 'en'}).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(req2) as res2:
        concept_data = json.loads(res2.read().decode('utf-8'))
        print(f'Runtime: {time.time()-start:.2f}s')
        print(f"Total concepts generated: {concept_data.get('count', 0)}")
        
        for i, c in enumerate(concept_data.get('concepts', [])):
             print(f"\n-- Concept {i+1} [{c.get('source', '')}] --")
             print(f"Term: {c.get('term', '')}")
             print(f"Definition: {c.get('definition', '')[:100]}...")
except Exception as e:
    print('Error:', e)


