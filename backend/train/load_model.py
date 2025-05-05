from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load from local
local_model_dir = "./distilgpt2_local"
model = AutoModelForCausalLM.from_pretrained(local_model_dir)
tokenizer = AutoTokenizer.from_pretrained(local_model_dir)

model.eval()

def generate_text(prompt, max_length=50):
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_length=max_length,
            num_return_sequences=1,
            no_repeat_ngram_size=2,
            top_p=0.92,
            temperature=0.7,
        )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)


