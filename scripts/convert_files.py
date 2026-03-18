import os
import glob
import time
from openai import OpenAI
from rate_limiter import TPMRateLimiter

# Initialize OpenAI
# Assuming OPENAI_API_KEY is set in environment variables
client = None
try:
    # API Key should be set in environment variables
    # os.environ["OPENAI_API_KEY"] = ... (Removed hardcoded key)
    
    if os.environ.get("OPENAI_API_KEY"):
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    else:
        print("Warning: OPENAI_API_KEY not found in environment variables.")
except Exception as e:
    print(f"Error initializing OpenAI client: {e}")

SOURCE_DIR = r"d:\AntiGravity\ÇÑ°¡¶÷ÄÁÅÙÃ÷ÆÀÀå\2013"
MODEL_NAME = "gpt-4o" 

# Initialize Rate Limiter (30k TPM)
limiter = TPMRateLimiter(tpm_limit=30000)

def convert_text_openai(text):
    if not client:
        print("Error: OpenAI client not initialized.")
        return None

    prompt = """
    ?¤ì ?ì¤?¸ë? ë¬¸ì´ì²´ë¡ ë³?í´ì¤? 
    ?´ì©???´í´?ê¸° ?½ê² ë¬¸ì´ì²´ë¡ ë§¤ë?½ê² ?¤ë¬ê³? ê°??¨ë½???ì ???ì ëª©ì ë¶ì¬ì¤?
    ë¶ë¥?ê¸° ?´ë µê±°ë ëª¨í¸??'?í¸' ê°ì? ?´ì©? ë³ëë¡?ë¶ë¦¬?ì? ë§ê³ , ë¬¸ë§¥???ì°?¤ë½ê²??¬í¨?í¤ê±°ë, 
    ?¬í¨?í¤ê¸????´ë µ?¤ë©´ ?ì¤?¸ì ë§?ë§ì?ë§ì [ë¶ë¡? ?ì?¼ë¡ ?ë¦¬?´ì ?£ì´ì¤?
    ê²°ê³¼?ì¼ë¡??ë???ì±??ê¸???ëë¡??´ì¤.
    
    ?ë¬¸ ?ì¤??
    """ + text

    # Rate Limiting Check
    estimated_tokens = limiter.estimate_tokens(prompt)
    limiter.wait_for_tokens(estimated_tokens)

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that converts text to a literary style."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return None

def process_file(filepath):
    filename = os.path.basename(filepath)
    base_name = os.path.splitext(filename)[0]
    
    literary_file = os.path.join(SOURCE_DIR, f"{base_name}_ë¬¸ì´ì²?txt")
    
    # Check if output file already exists
    if os.path.exists(literary_file):
        print(f"Skipping {filename} - already converted.")
        return

    print(f"Processing {filename}...")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return

    literary_content = convert_text_openai(content)
    if not literary_content:
        print(f"Failed to convert {filename}")
        return

    # Add original filename header
    literary_header = f"?ì¼ëª? {filename}\n\n"
    literary_final = literary_header + literary_content
    
    try:
        with open(literary_file, 'w', encoding='utf-8') as f:
            f.write(literary_final)
        print(f"Saved {literary_file}")
        
    except Exception as e:
        print(f"Error saving results for {filename}: {e}")

def main():
    if not os.path.exists(SOURCE_DIR):
        print(f"Directory not found: {SOURCE_DIR}")
        return
    
    # Ensure API Key is present
    if not os.environ.get("OPENAI_API_KEY"):
         print("Error: OPENAI_API_KEY environment variable not set.")
         return

    files = glob.glob(os.path.join(SOURCE_DIR, "*.txt"))
    # Filter out result files
    target_files = [f for f in files if not (f.endswith("_ë¬¸ì´ì²?txt") or 
                                             f.endswith("_?í¸.txt") or 
                                             f.endswith("_?¤ì??txt") or 
                                             f.endswith("_?¬êµ¬??txt"))]
    
    print(f"Found {len(target_files)} files to process.")
    
    for file in target_files:
        process_file(file)
        # Sleep briefly to avoid hitting rate limits
        # time.sleep(1) # Handled by RateLimiter now
        pass

if __name__ == "__main__":
    main()
