import os
import glob
import time
from openai import OpenAI
from rate_limiter import TPMRateLimiter

# Initialize OpenAI
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

BASE_DIR = r"d:\AntiGravity\ÇÑ°¡¶÷ÄÁÅÙÃ÷ÆÀÀå"
TARGET_DIRS = ["2013", "2014-2016", "2020-2025"]
OUTPUT_FILE = r"d:\AntiGravity\ÇÑ°¡¶÷ÄÁÅÙÃ÷ÆÀÀå\topic_report.md"

# Initialize Rate Limiter
limiter = TPMRateLimiter(tpm_limit=30000)

def get_file_summary(filepath):
    filename = os.path.basename(filepath)
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            # Reduced to 150 chars to save tokens
            content_snippet = f.read(150).replace('\n', ' ')
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return None

    return {
        "filename": filename,
        "snippet": content_snippet[:150]
    }

def collect_data():
    all_data = []
    
    for dir_name in TARGET_DIRS:
        dir_path = os.path.join(BASE_DIR, dir_name)
        if not os.path.exists(dir_path):
            print(f"Directory not found: {dir_path}")
            continue
            
        print(f"Scanning {dir_name}...")
        files = glob.glob(os.path.join(dir_path, "*.txt"))
        
        # Priority logic: Filter out raw files if processed exist?
        # For now, just take everything but prioritize logical grouping if meaningful.
        # We will let the LLM see all filenames.
        
        for f_path in files:
            fname = os.path.basename(f_path)
            if "error_report" in fname or "script" in fname:
                continue

            data = get_file_summary(f_path)
            if data:
                data["folder"] = dir_name
                all_data.append(data)
                
    return all_data

def analyze_batch(batch_items, batch_index):
    """
    Analyzes a batch of files and returns a summarized list of topics.
    """
    print(f"Processing batch {batch_index} ({len(batch_items)} items)...")
    
    context_str = ""
    for item in batch_items:
        context_str += f"[{item['folder']}] {item['filename']}: {item['snippet']}\n"
        
    prompt = """
    ?¤ì ?ì¼?¤ì ëª©ë¡ê³??´ì©??ë³´ê³ , ê°??ì¼??'?µì¬ ì£¼ì 'ë¥??ì½?´ì ë¦¬ì¤?¸ë¡ ë§ë¤?´ì¤.
    ?ì: "- [?ì¼ëª? ?µì¬ì£¼ì : (ì£¼ì ?´ì©)"
    """
    
    full_prompt = prompt + "\n\n" + context_str
    
    # Rate Limit Check
    estimated = limiter.estimate_tokens(full_prompt)
    limiter.wait_for_tokens(estimated)
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": full_prompt}
            ],
            max_tokens=2000
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error processing batch {batch_index}: {e}")
        return ""

def generate_final_report(all_summaries):
    print("Generating final classification report...")
    
    system_prompt = """
    ?¹ì ? ?ì¤??ì£¼ì  ë¶ì ?ë¬¸ê°?ë??
    ?ê³µ??'?ì¼ëª??µì¬ì£¼ì ' ëª©ë¡??ë°í?¼ë¡, ?ì²´ ?´ì©???ì°ë¥´ë 'ê³ì¸µ??ì£¼ì  ë¶ë¥ ë¦¬í¬??ë¥??ì±?´ì£¼?¸ì.
    
    [?êµ¬?¬í­]
    1. **?ë¶ë¥ - ì¤ë¶ë¥?- ?ë¶ë¥?*??3?¨ê³ë¥?ê°ì¶ ê³ì¸µ??êµ¬ì¡°ë¡??ë¦¬??ê²?
    2. ê°?ë¶ë¥?ë ?´ë¹?ë ì£¼ì ?¤ì?ë ?´ì©???¬í¨??ê²?
    3. **2013, 2014-2016, 2020-2025** ê°??ê¸°ë³?ê´?¬ì¬??ì£¼ì ??ë³???ë¦??ë³´ì´ë©?ë³ë ?¹ì("?ê¸°ë³?ì£¼ì  ?ë¦")?¼ë¡ ?ë¦¬??ê²?
    4. ì¤ë³µ??ì£¼ì ???µí©??ê²?
    5. ë³´ê³ ???ëª©? "ì£¼ì  ë¶ì ë°?ë¶ë¥ ë¦¬í¬??ë¡???ê²?
    6. ?¸ì´??**?êµ­??*ë¡??ì±??ê²?
    7. ê²°ê³¼ë¬¼ì? Markdown ?ì?¼ë¡ ?ì±??ê²?
    """
    
    full_content = f"?¤ì? ë¶ì???ì¼ë³?ì£¼ì  ?ì½?ë?? ?´ë? ì¢í©?ì¬ ë¦¬í¬?¸ë? ?ì±?´ì£¼?¸ì.\n\n{all_summaries}"
    
    # Rate Limit Check
    estimated = limiter.estimate_tokens(full_content) + limiter.estimate_tokens(system_prompt)
    limiter.wait_for_tokens(estimated)
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": full_content}
            ],
            max_tokens=4000
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating final report: {e}")
        return None

def main():
    data = collect_data()
    if not data:
        print("No data found.")
        return
    
    # Process in batches of 40
    batch_size = 40
    all_batch_results = ""
    
    for i in range(0, len(data), batch_size):
        batch = data[i : i + batch_size]
        result = analyze_batch(batch, i // batch_size + 1)
        if result:
            all_batch_results += result + "\n"
        
        # Sleep handled by rate limiter loop inside analyze_batch call if needed, 
        # but here we can add a small buffer or rely on limiter.
        # time.sleep(2) 
        
    final_report = generate_final_report(all_batch_results)
    
    if final_report:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write(final_report)
        print(f"Report saved to {OUTPUT_FILE}")
    else:
        print("Failed to generate final report.")

if __name__ == "__main__":
    main()
