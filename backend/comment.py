from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

local_dir = "S:/minor2/ai-doc-generator/phi_2_local"
model = None
tokenizer = None
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def load_model():
    global model, tokenizer
    if model is None or tokenizer is None:
        tokenizer = AutoTokenizer.from_pretrained(local_dir, local_files_only=True)
        model = AutoModelForCausalLM.from_pretrained(
            local_dir,
            torch_dtype=torch.float16,
            low_cpu_mem_usage=True,
            local_files_only=True,
        ).to(device)

def generate_comment_for_code(code_snippet):
    load_model()
    prompt = f"""# Add comments to the following code:

{code_snippet}

# Updated version with comments:
"""
    result = generate_response(prompt, tokenizer, model, max_tokens=300)
    return result.split("# Updated version with comments:")[1].split("```\n\n")[0]

def generate_response(prompt, tokenizer, model, max_tokens=300):
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    outputs = model.generate(**inputs, max_new_tokens=max_tokens)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

code_snippet = """
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left_half = arr[:mid]
    right_half = arr[mid:]
    left_half = merge_sort(left_half)
    right_half = merge_sort(right_half)
    return merge(left_half, right_half)

def merge(left, right):
    merged = []
    left_index = 0
    right_index = 0
    while left_index < len(left) and right_index < len(right):
        if left[left_index] <= right[right_index]:
            merged.append(left[left_index])
            left_index += 1
        else:
            merged.append(right[right_index])
            right_index += 1
    merged += left[left_index:]
    merged += right[right_index:]
    return merged

arr = [64, 34, 25, 12, 22, 11, 90]
arr = merge_sort(arr)
print(arr)
"""


result=generate_comment_for_code(code_snippet)
print(result)

