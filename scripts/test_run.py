import os
import sys

# Add 한가람컨텐츠팀장 to path to import convert_files
sys.path.append(r"d:\AntiGravity\한가람컨텐츠팀장")
import convert_files

# Test file
test_file = r"d:\AntiGravity\한가람컨텐츠팀장\2024-2025\20210430_080533_湲곕낯_260114_151554.txt"

print(f"Testing conversion on {test_file}")
convert_files.process_file(test_file)
