import requests
import json
import os
import sys

# Configuration from script.txt
SECRET_KEY = 'a9be7de1869a48ea9391dc41e0f46c2e'
INVOKE_URL = 'https://clovaspeech-gw.ncloud.com/external/v1/14316/ff53947133a68d852595e81c18582e7dddf5914cc5ce468a63e993ca61ce3435/recognizer/upload'

def process_file(file_path):
    print(f"Processing file: {file_path}")
    
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return None

    headers = {
        'X-CLOVASPEECH-API-KEY': SECRET_KEY
    }

    # Parameters for the recognition
    params = {
        'language': 'ko-KR',
        'completion': 'sync', # Sync for immediate response, might need async for very long files but let's try sync
        'wordAlignment': True,
        'fullText': True,
        'diarization': {
            'enable': True,
        }
    }

    files = {
        'media': open(file_path, 'rb'),
        'params': (None, json.dumps(params), 'application/json')
    }

    try:
        print("Sending request to Clova Speech API...")
        response = requests.post(INVOKE_URL, headers=headers, files=files)
        
        print(f"Response Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            # print(json.dumps(result, indent=2, ensure_ascii=False)) # Debug
            return result
        else:
            print(f"Error Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return None
    finally:
        files['media'].close()

def save_result_to_txt(result, original_file_path):
    if not result:
        return

    text_output_path = os.path.splitext(original_file_path)[0] + ".txt"
    
    # Extract text from result
    # Format might depend on diarization. 
    # Usually: result['text'] is full text, result['segments'] has speaker info.
    
    content_list = []
    
    if 'segments' in result:
        for segment in result['segments']:
            speaker = segment.get('speaker', {}).get('name', 'Unknown')
            text = segment.get('text', '')
            content_list.append(f"{speaker}: {text}")
    else:
        content_list.append(result.get('text', ''))

    final_text = "\n".join(content_list)

    with open(text_output_path, 'w', encoding='utf-8-sig') as f:
        f.write(final_text)
        
    print(f"Saved transcript to: {text_output_path}")
    return text_output_path

if __name__ == "__main__":
    target_file = r"d:\?ì£¼?˜ë§?€\2013\?Œì„±?¹ìŒ_130814_110717.mp3"
    if len(sys.argv) > 1:
        target_file = sys.argv[1]
        
    result = process_file(target_file)
    if result:
        save_result_to_txt(result, target_file)
