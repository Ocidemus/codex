from transformers import GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments, DataCollatorForLanguageModeling
from datasets import load_dataset, DatasetDict
import torch

print("Loading dataset...")
dataset = load_dataset("code_search_net", "python", split={"train": "train", "validation": "validation"})

tokenizer = GPT2Tokenizer.from_pretrained("distilgpt2")
tokenizer.pad_token = tokenizer.eos_token 

model = GPT2LMHeadModel.from_pretrained("distilgpt2")

def preprocess(example):
    if example["func_code_string"] and example["func_documentation_string"]:
        text = f"{example['func_documentation_string']}\n{example['func_code_string']}"
        encoding = tokenizer(text, truncation=True, padding="max_length", max_length=512)
        encoding["labels"] = encoding["input_ids"].copy()
        return encoding
    return None

print("Tokenizing...")
train_data = dataset["train"].map(preprocess, remove_columns=dataset["train"].column_names)
val_data = dataset["validation"].map(preprocess, remove_columns=dataset["validation"].column_names)

train_data = train_data.filter(lambda x: x is not None and "input_ids" in x)
val_data = val_data.filter(lambda x: x is not None and "input_ids" in x)

# Training arguments
training_args = TrainingArguments(
    output_dir="./distilgpt2-comment-gen",
    overwrite_output_dir=True,
    do_eval=True,
    learning_rate=5e-5,
    per_device_train_batch_size=2,
    per_device_eval_batch_size=2,
    num_train_epochs=3,
    weight_decay=0.01,
    save_steps=500,
    save_total_limit=2,
    logging_dir="./logs",
    logging_steps=100,
    remove_unused_columns=False 
)

data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer, mlm=False
)

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_data,
    eval_dataset=val_data,
    data_collator=data_collator
)

print("Training...")
trainer.train()

# Save final model
model.save_pretrained("./distilgpt2-comment-gen")
tokenizer.save_pretrained("./distilgpt2-comment-gen")
