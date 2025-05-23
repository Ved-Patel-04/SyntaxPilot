from transformers import GPT2LMHeadModel, GPT2Tokenizer, Trainer, TrainingArguments
import torch
import transformers
from datasets import Dataset

model_name = "gpt2"

model = GPT2LMHeadModel.from_pretrained(model_name)

tokenizer = GPT2Tokenizer.from_pretrained(model_name)

tokenizer.pad_token = tokenizer.eos_token

train_data = Dataset.from_json("train.jsonl")
test_data = Dataset.from_json("test.jsonl")

def tokenize_function(examples):

    texts = [
        c + p + t
        for c, p, t in zip(examples['context'],
                           examples['partial_line'],
                           examples['completion'])
    ]
    encodings = tokenizer(
        texts,
        padding="max_length",
        truncation=True,
        max_length=256,
        add_special_tokens=False, 
    )

    labels = [ids.copy() for ids in encodings["input_ids"]]

    for i, (c, p, t) in enumerate(zip(examples['context'],
                                     examples['partial_line'],
                                     examples['completion'])):
        prefix_ids = tokenizer(
            c + p,
            add_special_tokens=False,
            truncation=True,
            max_length=256
        )["input_ids"]
        prefix_len = len(prefix_ids)

        target_ids = tokenizer(
            t,
            add_special_tokens=False,
            truncation=True,
            max_length=256
        )["input_ids"]
        target_len = len(target_ids)

        labels[i][:prefix_len] = [-100] * prefix_len
        end_of_target = prefix_len + target_len
        labels[i][end_of_target:] = [-100] * (len(labels[i]) - end_of_target)

    encodings["labels"] = labels
    return encodings

train_data = train_data.map(tokenize_function, batched=True, batch_size=32)
test_data = test_data.map(tokenize_function, batched=True, batch_size=32)

training_args = TrainingArguments(
    output_dir="./gpt2-finetuned-line-completion-short", 
    num_train_epochs=1,
    per_device_train_batch_size=32,
    per_device_eval_batch_size=32,
    gradient_accumulation_steps=1,
    logging_dir='./logs-short',
    logging_steps=100,
    do_eval=True,
    eval_strategy="steps",
    save_steps=500,
    save_total_limit=2,
)


trainer_short_finetune = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_data,
    eval_dataset=test_data,
)


evaluation_results_before = trainer_short_finetune.evaluate()
print("Loss before fine-tuning:", evaluation_results_before)

trainer_short_finetune.train()

evaluation_results_after = trainer_short_finetune.evaluate()
print("Loss after  fine-tuning:", evaluation_results_after)