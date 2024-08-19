from transformers import AutoModelForCausalLM, AutoTokenizer

class AutocompleteModel:
    def __init__(self, model_name=None):
        self.model_name = model_name
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)

    def get_model_and_tokenizer(self):
        return self.model, self.tokenizer