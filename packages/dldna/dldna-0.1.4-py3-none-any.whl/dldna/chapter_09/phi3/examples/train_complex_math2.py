import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
import random
from typing import Optional
from tqdm import tqdm

from dldna.chapter_09.phi3.simple_phi3 import PhiMiniConfig, PhiMiniForCausalLM

def create_advanced_arithmetic_data(num_samples: int, max_value: int, max_terms: int = 4, max_length: int = 60) -> list:
    data = []

    def generate_expression(num_terms: int, nested: bool = False) -> tuple[str, int]:
        if num_terms == 1:
            value = random.randint(-max_value, max_value)
            return (f"({value})", value) if value < 0 else (str(value), value)

        op = random.choice(['+', '-', '*'])
        num_left_terms = random.randint(1, num_terms - 1)
        num_right_terms = num_terms - num_left_terms

        left_expr, left_result = generate_expression(num_left_terms, True)
        right_expr, right_result = generate_expression(num_right_terms, True)

        if op in ('+', '-') and ('*' in left_expr or '*' in right_expr):
            left_expr = f"({left_expr})"
            right_expr = f"({right_expr})"
        elif nested and random.random() < 0.5:
            left_expr = f"({left_expr})"
            right_expr = f"({right_expr})"

        if right_expr.startswith('-') and not (right_expr.startswith('(') and right_expr.endswith(')')):
            right_expr = f"({right_expr})"

        expr = f"{left_expr}{op}{right_expr}"

        try:
            result = eval(expr)
            if not isinstance(result, int):
                raise ValueError("Result is not an integer")
            return expr, result
        except (SyntaxError, TypeError, OverflowError):
            return "", 0

    attempts = 0
    max_attempts = num_samples * 100

    while len(data) < num_samples and attempts < max_attempts:
        attempts += 1
        num_terms = random.randint(2, max_terms)
        expr, result = generate_expression(num_terms)
        if expr:
            sample = f"{expr}={result}<eos>"
            if len(sample) <= max_length:
                data.append(sample)

    if attempts == max_attempts:
        print(f"Warning: max attempts reached. Generated {len(data)} out of {num_samples} samples.")

    return data


def create_tokenizer() -> dict:
    vocab = {}
    for i in range(10):
        vocab[str(i)] = i
    vocab['+'] = 10
    vocab['-'] = 11
    vocab['*'] = 12
    vocab['='] = 13
    vocab['<pad>'] = 14
    vocab['<eos>'] = 15
    vocab['('] = 16
    vocab[')'] = 17
    return vocab

def create_reverse_tokenizer(tokenizer: dict) -> dict:
    return {v: k for k, v in tokenizer.items()}

def tokenize_sample(sample: str, tokenizer: dict) -> list:
    tokens = []
    i = 0
    while i < len(sample):
        if sample[i] == '<':
            j = sample.find('>', i)
            if j != -1:
                token = sample[i:j+1]
                if token in tokenizer:
                    tokens.append(token)
                    i = j + 1
                    continue
        tokens.append(sample[i])
        i += 1
    return tokens

# --- Dataset Class (CORRECTED) ---
class ComplexArithmeticDataset(Dataset):
    def __init__(self, data: list, seq_length: int, tokenizer: dict):
        self.data = data
        self.seq_length = seq_length
        self.tokenizer = tokenizer

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        text = self.data[idx]
        tokens = tokenize_sample(text, self.tokenizer)
        if len(tokens) < self.seq_length:
            tokens = tokens + ['<pad>'] * (self.seq_length - len(tokens))
        else:
            tokens = tokens[:self.seq_length]
        token_ids = [self.tokenizer[token] for token in tokens]
        input_ids = torch.tensor(token_ids, dtype=torch.long)
        # NO SHIFTING HERE! Return input_ids as both input and label
        return input_ids, input_ids

# --- Training Function (CORRECTED) ---
def train(model, dataloader, optimizer, scheduler, epochs, device):
    model.train()
    for epoch in range(epochs):
        total_loss = 0.0
        for _ , (input_ids, labels) in enumerate(tqdm(dataloader, mininterval=30)):
            input_ids = input_ids.to(device)
            labels = input_ids.to(device)  # Use input_ids as labels
            optimizer.zero_grad()
            outputs = model(input_ids=input_ids, labels=labels, return_dict=True)
            loss = outputs["loss"]
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        scheduler.step()
        current_lr = scheduler.get_last_lr()[0]
        print(f"Epoch {epoch+1}/{epochs}, Avg Loss: {total_loss/len(dataloader):.4f}, LR: {current_lr:.6f}")

def generate_text(model, start_text, tokenizer, reverse_tokenizer, max_length, device, temperature=0.6):
    model.eval()
    token_ids = [tokenizer[token] for token in tokenize_sample(start_text, tokenizer)]
    input_ids = torch.tensor(token_ids, dtype=torch.long).unsqueeze(0).to(device)
    generated = list(tokenize_sample(start_text, tokenizer))
    with torch.no_grad():
        for _ in range(max_length - len(token_ids)):
            outputs = model(input_ids=input_ids, return_dict=True)
            logits = outputs["logits"][:, -1, :] / temperature
            probs = F.softmax(logits, dim=-1)
            top_k_probs, top_k_indices = torch.topk(probs, k=5, dim=-1)
            next_token_id = top_k_indices[0, torch.multinomial(top_k_probs, num_samples=1).item()].item()
            next_token = reverse_tokenizer[next_token_id]
            if next_token in ['<eos>', '<pad>']:
                break
            generated.append(next_token)
            input_ids = torch.cat([input_ids, torch.tensor([[next_token_id]], dtype=torch.long).to(device)], dim=1)
    return "".join(generated)

# --- Main Execution ---
if __name__ == "__main__":
    random.seed(42)
    torch.manual_seed(42)

    device = "cuda" if torch.cuda.is_available() else "cpu"

    # Hyperparameters
    num_samples = 200000
    max_value = 50
    seq_length = 30
    batch_size = 24
    epochs = 30
    learning_rate = 1e-3
    max_terms = 8
    max_length = 60

    # Data Generation
    complex_data = create_advanced_arithmetic_data(num_samples, max_value, max_terms, max_length)
    print("Training data examples:")
    for i in range(10):
        print(f"Sample {i+1}: {complex_data[i]}")

    # Create tokenizer and reverse tokenizer
    tokenizer = create_tokenizer()
    reverse_tokenizer = create_reverse_tokenizer(tokenizer)
    updated_vocab_size = len(tokenizer)

    # Configure Dataset and DataLoader
    dataset = ComplexArithmeticDataset(complex_data, seq_length, tokenizer)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    # PhiMini Model Configuration
    config = PhiMiniConfig(
        vocab_size=updated_vocab_size,
        hidden_size=256,
        intermediate_size=512,
        num_hidden_layers=8,
        num_attention_heads=8,
        num_key_value_heads=8,
        max_position_embeddings=256,
        use_cache=True,
        use_return_dict=True,
    )
    config.pad_token_id = tokenizer["<pad>"]
    config.eos_token_id = tokenizer["<eos>"]

    # Create PhiMini For CausalLM Model
    model = PhiMiniForCausalLM(config).to(device)
    print("Total Trainable Parameters:", sum(p.numel() for p in model.parameters() if p.requires_grad))

    # weight tying
    model.lm_head.weight = model.transformer.embed_tokens.weight

    optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate, weight_decay=0.01)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs, eta_min=1e-6)

    # Model Training
    print("Start training...")
    train(model, dataloader, optimizer, scheduler, epochs, device)

    # Save Model
    save_path = "phimini_advanced_math_v7.pt"
    torch.save(model.state_dict(), save_path)
    print(f"Model saved: {save_path}")

    # Load Saved Model
    loaded_model = PhiMiniForCausalLM(config).to(device)
    loaded_model.load_state_dict(torch.load(save_path, map_location=device))
    loaded_model.eval()

    # Generate and Print Results with Test Set, Calculate Accuracy
    print("\nTest sample generation results:")
    test_samples = random.sample(complex_data, 50)
    correct_count = 0
    for sample in test_samples:
        prompt = sample.split('=')[0] + '='
        generated = generate_text(loaded_model, prompt, tokenizer, reverse_tokenizer, seq_length, device, temperature=0.1)  # Reduce temperature for testing
        answer = sample.split('=')[1].replace('<eos>', '')

        if generated.split('=')[1] == answer:
            correct_count += 1
        print(f"Prompt: '{prompt}' --> Generated result: '{generated}'  (Correct answer: {sample})")

    accuracy = (correct_count / len(test_samples)) * 100
    print(f"\nOverall accuracy: {accuracy:.2f}% ({correct_count}/{len(test_samples)})")