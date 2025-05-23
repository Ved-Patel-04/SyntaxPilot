
import warnings
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

warnings.filterwarnings("ignore", category=FutureWarning)


def load_model_and_tokenizer(model_path="bigrun2", base_tokenizer="gpt2"):
    tokenizer = GPT2Tokenizer.from_pretrained(base_tokenizer)
    tokenizer.pad_token = tokenizer.eos_token
    model = GPT2LMHeadModel.from_pretrained(model_path)
    model.eval()
    return model, tokenizer

def generate_completion(model, tokenizer, context, partial_line,
                        max_new_tokens=30, do_sample=True, temperature=0.2,
                        top_k=10, top_p=0.9, repetition_penalty=1.2,
                        no_repeat_ngram_size=3):
    full_prompt = context + partial_line
    inputs = tokenizer(
        full_prompt,
        return_tensors="pt",
        add_special_tokens=True
    )
    input_ids = inputs["input_ids"]
    attention_mask = inputs["attention_mask"]

    gen_pad_token_id = tokenizer.pad_token_id if tokenizer.pad_token_id is not None else tokenizer.eos_token_id

    with torch.no_grad():
        gen_ids = model.generate(
            input_ids,
            attention_mask=attention_mask,
            max_new_tokens=max_new_tokens,
            do_sample=do_sample,
            eos_token_id=tokenizer.eos_token_id,
            pad_token_id=gen_pad_token_id,
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
            repetition_penalty=repetition_penalty,
            no_repeat_ngram_size=no_repeat_ngram_size,
        )

    new_tokens = gen_ids[0, input_ids.shape[-1]:]
    completion_text = tokenizer.decode(new_tokens, skip_special_tokens=True)

    return partial_line + completion_text


if __name__ == "__main__":
    MODEL_DIR = "bigrun2"


    llm_model, llm_tokenizer = load_model_and_tokenizer(model_path=MODEL_DIR)

    example_context = (
        "{\n} WIDGET;\n\tresult->center.x = atof(coord[0]);\n\tPG_RETURN_CSTRING(str);\n\tPoint\t   *point = PG_GETARG_POINT_P(0);"
    )
    example_partial_line = "PointPGetD"

    completion_result = generate_completion(
        llm_model,
        llm_tokenizer,
        example_context,
        example_partial_line
    )

    another_completion = generate_completion(
        llm_model,
        llm_tokenizer,
        "import numpy as np\n\ndef calculate_mean(data):\n    ",
        "avg = np.mean"
    )
    print("\nCompletion:")
    print(another_completion)