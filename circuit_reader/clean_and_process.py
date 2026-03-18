import json
import re
import os

source_file = r'd:\페르미아\가람\회로도관련\회로도소개 - 007(통합본).txt'
output_json = r'd:\페르미아\가람\circuit_reader\content.json'

# Step 1: Clean the original text file (Remove all **)
if os.path.exists(source_file):
    with open(source_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove ** pattern
    cleaned_content = content.replace('**', '')
    
    with open(source_file, 'w', encoding='utf-8') as f:
        f.write(cleaned_content)
    print(f"Cleaned ** from {source_file}")

# Step 2: Reprocess to JSON
with open(source_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

dialogues = []
current_speaker = None
current_text = []

for line in lines:
    line = line.strip()
    if not line:
        continue
    
    if line.startswith('말씀하신 내용'):
        if current_speaker:
            dialogues.append({'speaker': current_speaker, 'text': ' '.join(current_text)})
        current_speaker = 'Wonju'
        current_text = []
    elif line.startswith('Gemini의 응답'):
        if current_speaker:
            dialogues.append({'speaker': current_speaker, 'text': ' '.join(current_text)})
        current_speaker = 'Remin'
        current_text = []
    else:
        # Check for headers or other metadata to skip if necessary
        if 'Step Id:' in line or 'File Path:' in line or 'Total Lines:' in line:
            continue
        current_text.append(line)

if current_speaker:
    dialogues.append({'speaker': current_speaker, 'text': ' '.join(current_text)})

with open(output_json, 'w', encoding='utf-8') as f:
    json.dump(dialogues, f, ensure_ascii=False, indent=2)

print(f"Processed {len(dialogues)} dialogue entries into {output_json}.")
