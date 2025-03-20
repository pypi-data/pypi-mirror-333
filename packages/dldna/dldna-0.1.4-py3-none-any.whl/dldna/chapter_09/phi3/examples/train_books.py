import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from transformers import GPT2TokenizerFast
from datasets import load_dataset
import random
import math
from tqdm import tqdm

from dldna.chapter_09.phi3.simple_phi3 import PhiMiniConfig, PhiMiniForCausalLM

#############################################
# Data Preprocessing: Clean text from BookCorpus
#############################################
def simple_clean(example):
    text = example["text"].strip()
    if len(text) == 0:
        text = " "
    example["text"] = text
    return example

#############################################
# Dataset Class
#############################################
class TextDataset(Dataset):
    def __init__(self, texts, tokenizer, max_length):
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.texts = texts

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        encoding = self.tokenizer(
            self.texts[idx],
            truncation=True,
            max_length=self.max_length,
            padding="max_length",
        )
        input_ids = torch.tensor(encoding["input_ids"], dtype=torch.long)
        labels = input_ids.clone()  # In Causal LM, input and labels are the same (shifted after calculation)
        return input_ids, labels

#############################################
# Training Function across multiple epochs (with tqdm)
#############################################
def train(model, dataloader, optimizer, scheduler, epochs, device):
    model.train()
    for epoch in range(1, epochs + 1):
        total_loss = 0.0
        progress_bar = tqdm(dataloader, desc=f"Epoch {epoch}", mininterval=30)
        for batch_idx, (input_ids, labels) in enumerate(progress_bar):
            input_ids = input_ids.to(device)
            labels = labels.to(device)
            optimizer.zero_grad()
            outputs = model(input_ids=input_ids, labels=labels, return_dict=True)
            loss = outputs["loss"]
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
            if (batch_idx + 1) % 100 == 0:
                print(f"Step {batch_idx+1} Loss: {loss.item():.4f}")
            progress_bar.set_postfix({"loss": f"{loss.item():.4f}"})
        scheduler.step()
        avg_loss = total_loss / len(dataloader)
        print(f"Epoch {epoch} Average Loss: {avg_loss:.4f}")

#############################################
# Text Generation Function (use_cache disabled)
#############################################
def generate_text(model, prompt, tokenizer, max_length, device, temperature=1.0, do_sample=True):
    model.eval()
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(device)
    with torch.no_grad():
        # Disable cache (to avoid sequence length mismatch issues with key and value tensors)
        generated_ids = model.generate(
            input_ids=input_ids,
            max_new_tokens=max_length,
            temperature=temperature,
            do_sample=do_sample
        )
    return tokenizer.decode(generated_ids, skip_special_tokens=True)

#############################################
# Final Example: Generate text for multiple prompts
#############################################
def run_generation_examples(model, tokenizer, device):
    prompts = [
        "Once upon a time,",
        "In a world where",
        "The secret to happiness is",
        "Technology has changed",
        "Data science is"
    ]
    print("\nGeneration Examples:")
    for prompt in prompts:
        generated = generate_text(model, prompt, tokenizer, max_length=100, device=device, temperature=0.8)
        print(f"Prompt: {prompt}\nGenerated Text: {generated}\n{'-'*50}")

#############################################
# Main Execution: Load data, train, save model, run examples
#############################################
if __name__ == "__main__":
    # Set Seed
    random.seed(42)
    torch.manual_seed(42)

    device = "cuda:1" if torch.cuda.is_available() else "cpu"

    # Hyperparameters
    max_length = 512
    batch_size = 16
    epochs = 1      # Train for the specified number of epochs
    learning_rate = 1e-3

    # Load tokenizer (vocab_size=50257)
    tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
    # Set pad_token to be the same as eos_token
    tokenizer.pad_token = tokenizer.eos_token

    # Load BookCorpus dataset (1% subset)
    dataset = load_dataset("bookcorpus", split="train[:1%]", trust_remote_code=True)
    dataset = dataset.map(simple_clean, num_proc=24)
    texts = dataset["text"]
    print(f"Loaded {len(texts)} samples from BookCorpus (1% subset).")

    # Configure Dataset and DataLoader
    train_dataset = TextDataset(texts, tokenizer, max_length)
    train_dataloader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

    # Model Configuration: Reconfigure PhiMiniConfig to match the tokenizer
    config = PhiMiniConfig(
        vocab_size=tokenizer.vocab_size,
        hidden_size=512,
        intermediate_size=2048,
        num_hidden_layers=12,
        num_attention_heads=8,
        num_key_value_heads=8,
        max_position_embeddings=1024,
        use_cache=True,          # Use cache during training (the problem is caching during the generation phase)
        use_return_dict=True,
        pad_token_id=tokenizer.pad_token_id,
        bos_token_id=tokenizer.bos_token_id if tokenizer.bos_token_id is not None else tokenizer.eos_token_id,
        eos_token_id=tokenizer.eos_token_id,
    )
    model = PhiMiniForCausalLM(config).to(device)

    # Set up Optimizer and Cosine Annealing Scheduler
    optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs, eta_min=1e-6)

    # Run Training
    # print("Start training...")
    # train(model, train_dataloader, optimizer, scheduler, epochs, device)

    # Save the trained model
    save_path = "./phi_mini_bookcorpus.pt"
    # torch.save(model.state_dict(), save_path)
    # print(f"Model saved: {save_path}")

    # Load the saved model
    loaded_model = PhiMiniForCausalLM(config).to(device)
    loaded_model.load_state_dict(torch.load(save_path, map_location=device))
    loaded_model.eval()

    # Final Example: Run text generation through a separate method
    run_generation_examples(loaded_model, tokenizer, device)