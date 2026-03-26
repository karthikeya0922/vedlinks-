import sys

file_path = 'C:/internship2/vedlinks-/train_pipeline.py'
with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

old_block = '''                        # Type A: Summarize/Explain this section
                          summary_sentences = [s.strip() for s in chunk.split('.') if len(s.strip()) > 10]
                          summary_answer = f"This section explains that {summary_sentences[0]}." if summary_sentences else f"This section discusses the core concepts of {context_label}."
                          training_samples.append({
                              "prompt": f"### Instruction:\\nSummarize this section from {context_label}.\\n\\n### Input:\\n{chunk[:300]}...\\n\\n### Response:",
                              "completion": summary_answer
                          })

                          # Type B: Question from context
                          insight = f"One important detail to remember is that {summary_sentences[-1]}." if len(summary_sentences) > 1 else f"A key detail about {chapter_name} is its fundamental principles."
                          training_samples.append({
                              "prompt": f"### Instruction:\\nBased on {context_label}, provide a key insight from the following text.\\n\\n### Input:\\n{chunk[:150]}...\\n\\n### Response:",
                              "completion": insight'''

new_block = '''                        # Type A: Summarize/Explain this section
                        summary_sentences = [s.strip() for s in chunk.split('.') if len(s.strip()) > 10]
                        summary_answer = f"This section explains that {summary_sentences[0]}." if summary_sentences else f"This section discusses the core concepts of {context_label}."
                        training_samples.append({
                            "prompt": f"### Instruction:\\nSummarize this section from {context_label}.\\n\\n### Input:\\n{chunk[:300]}...\\n\\n### Response:",
                            "completion": summary_answer
                        })

                        # Type B: Question from context
                        insight = f"One important detail to remember is that {summary_sentences[-1]}." if len(summary_sentences) > 1 else f"A key detail about {chapter_name} is its fundamental principles."
                        training_samples.append({
                            "prompt": f"### Instruction:\\nBased on {context_label}, provide a key insight from the following text.\\n\\n### Input:\\n{chunk[:150]}...\\n\\n### Response:",
                            "completion": insight
                        })'''

if old_block in text:
    text = text.replace(old_block, new_block)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(text)
    print("Fixed indentation.")
else:
    print("Could not find the exact block.")
