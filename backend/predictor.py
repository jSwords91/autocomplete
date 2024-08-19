import torch
import torch.nn.functional as F
from transformers import AutoModelForCausalLM, AutoTokenizer

class Predictor:
    def __init__(self, model: AutoModelForCausalLM, tokenizer: AutoTokenizer):
        self.model = model
        self.tokenizer = tokenizer

    def predict_next_words(self, text, top_k=10):
        input_ids = self.tokenizer.encode(text, return_tensors="pt")

        with torch.no_grad():
            outputs = self.model(input_ids)
            predictions = outputs[0]

        next_token_logits = predictions[0, -1, :]
        top_k_logits, top_k_indices = torch.topk(next_token_logits, top_k)
        top_k_probs = F.softmax(top_k_logits, dim=-1)

        results = []

        for i in range(top_k):
            token = self.tokenizer.decode([top_k_indices[i]])
            prob = top_k_probs[i].item()
            results.append((token, prob))

        return results