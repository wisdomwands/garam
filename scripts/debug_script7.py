import os
import re
from openai import OpenAI

# Initialize OpenAI Client (Same key)
try:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
except Exception as e:
    print(f"Error initializing OpenAI client: {e}")
    exit()

def extract_wonjunim_words_from_txt(file_path):
    print(f"Reading {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        extracted_texts = []
        current_speaker = None
        speaker_pattern = re.compile(r'^諛쒗솕??s+(\d+)\s+')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            match = speaker_pattern.match(line)
            if match:
                current_speaker = match.group(1)
                print(f"Found speaker: {current_speaker}")
                continue
            
            if current_speaker == '1':
                extracted_texts.append(line)
        
        return " ".join(extracted_texts)
            
    except Exception as e:
        print(f"Error reading/parsing file {file_path}: {e}")
        return None

def main():
    file_path = r"d:\antigravity\한가람컨텐츠팀장\2020-2025\20210428-??遺?260114_151531.txt"
    extracted = extract_wonjunim_words_from_txt(file_path)
    
    if extracted:
        print(f"Extracted {len(extracted)} chars")
        print(f"Preview: {extracted[:200]}...")
    else:
        print("Failed to extract text.")

    # Test API
    print("Testing OpenAI API...")
    try:
        response = client.chat.completions.create(
            model="gpt-4o", # Test with 4o first as it's reliable
            messages=[{"role": "user", "content": "Hello"}]
        )
        print("API Response:", response.choices[0].message.content)
    except Exception as e:
        print(f"API Error: {e}")

if __name__ == "__main__":
    main()
