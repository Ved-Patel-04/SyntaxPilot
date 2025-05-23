from pathlib import Path
import json
import random
import os
import re


ROOT_DIR = Path(".")
OUTPUT_FILE = "train_data.jsonl"
TRAIN_FILE = "train.jsonl"
TEST_FILE = "test.jsonl"
CONTEXT_LINES = 5
EXAMPLES_PER_FILE = 10
DELETE_PROBABILITY = 878 / 1000
TRAIN_RATIO = 0.9

def strip_comments(code):
    code = re.sub(r'//.*', '', code)
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
    return code

def is_code_line(line):
    stripped = line.strip()
    return bool(stripped)

def get_partial_versions(line):
    break_point = random.randrange(2, 8) / 10
    split_point = int(len(line) * break_point)
    return [line[:split_point].strip()]

all_samples = []

for filepath in ROOT_DIR.rglob("*.c"):
    try:
        lines = filepath.read_text(encoding="utf-8", errors="ignore").splitlines()

        processed_lines = []
        inside_multiline_comment = False

        for line in lines:
            if inside_multiline_comment:
                if "*/" in line:
                    line = line.split("*/", 1)[1]
                    inside_multiline_comment = False
                else:
                    continue

            while "/*" in line:
                start = line.find("/*")
                end = line.find("*/", start + 2)
                if end != -1:
                    line = line[:start] + line[end + 2:]
                else:
                    line = line[:start]
                    inside_multiline_comment = True
                    break

            line = strip_comments(line)
            if is_code_line(line) and random.random() >= DELETE_PROBABILITY:
                processed_lines.append(line)

        for i in range(CONTEXT_LINES // 2, len(processed_lines)):
            full_line = processed_lines[i].strip()
            if len(full_line) < 5:
                continue

            start_context = max(0, i - CONTEXT_LINES)
            context_lines = processed_lines[start_context:i]
            context = "\n".join(context_lines)

            for partial in get_partial_versions(full_line):
                sample = {
                    "context": context,
                    "partial_line": partial,
                    "completion": full_line + ' <|endoftext|>'                    
                }
                all_samples.append(sample)
    except Exception as e:
        print(f"Failed to process {filepath}: {e}")

random.shuffle(all_samples)

train_size = int(len(all_samples) * TRAIN_RATIO)
train_samples = all_samples[:train_size]
test_samples = all_samples[train_size:]

with open(TRAIN_FILE, "w", encoding="utf-8") as train_out_file:
    for sample in train_samples:
        json.dump(sample, train_out_file)
        train_out_file.write("\n")

with open(TEST_FILE, "w", encoding="utf-8") as test_out_file:
    for sample in test_samples:
        json.dump(sample, test_out_file)
        test_out_file.write("\n")

print(f"Generated {len(train_samples)} training examples in {TRAIN_FILE}")
print(f"Generated {len(test_samples)} testing examples in {TEST_FILE}")