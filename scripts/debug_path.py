import os

base_path = r"d:\페르미아\가람컨텐츠팀장"
target_dir = os.path.join(base_path, "원주님말씀.doc", "2024-2025.new")

print(f"Target dir: {target_dir}")
if os.path.exists(target_dir):
    print("Directory exists.")
    if os.path.isdir(target_dir):
        print("It is a directory.")
    else:
        print("It is a file.")
else:
    print("Directory does NOT exist.")
    try:
        os.makedirs(target_dir, exist_ok=True)
        print("Created directory.")
    except Exception as e:
        print(f"Failed to create directory: {e}")

test_file = os.path.join(target_dir, "test.txt")
try:
    with open(test_file, "w") as f:
        f.write("test")
    print(f"Successfully wrote to {test_file}")
except Exception as e:
    print(f"Failed to write to file: {e}")
