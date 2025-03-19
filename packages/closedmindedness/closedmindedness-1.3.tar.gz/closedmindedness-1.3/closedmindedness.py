from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import PeftModel
import torch
import numpy as np

base_model_id = 'teknium/OpenHermes-2.5-Mistral-7B'
ft_model_id = 'mamakos/CMClassifier'

class classifier:
  def __init__(self):
      bnb_config = BitsAndBytesConfig(load_in_4bit=True,
                                      bnb_4bit_quant_type='nf4',
                                      bnb_4bit_compute_dtype=torch.bfloat16,
                                      bnb_4bit_use_double_quant=False)

      base_model = AutoModelForCausalLM.from_pretrained(base_model_id,
                                                        quantization_config=bnb_config,
                                                        device_map={'': 'cuda'},
                                                        trust_remote_code=True)
      
      self.tokenizer = AutoTokenizer.from_pretrained(base_model_id,
                                                     add_bos_token=True,
                                                     trust_remote_code=True)
            
      self.ft_model = PeftModel.from_pretrained(base_model, ft_model_id)
      self.ft_model.eval()
  
  
  def predict(self, texts):
      if isinstance(texts, str):
          texts = [texts]

      prompts = [self.get_prompt(text) for text in texts]
      
      probs = np.zeros(len(texts))
      
      with torch.no_grad():
          for i in range(len(texts)):
              tokenized_prompt = self.tokenizer(prompts[i], return_tensors='pt').to('cuda')
            
              output = self.ft_model.generate(**tokenized_prompt, 
                                              pad_token_id=self.tokenizer.eos_token_id,
                                              max_new_tokens=1,
                                              do_sample=False,
                                              return_dict_in_generate=True, 
                                              output_scores=True)
            
              transition_score = self.ft_model.compute_transition_scores(output.sequences, 
                                                                         output.scores, 
                                                                         normalize_logits=True)
            
              prob = np.exp(transition_score[0][0].cpu().numpy())
              response = self.tokenizer.decode(output.sequences[:, -1][0])
              if response == 'No':
                  prob = 1 - prob
              probs[i] = prob
              
      return probs
  
  def get_prompt(self, text):
      prompt = f'''<|im_start|>system
You are a helpful assistant.
<|im_end|>
<|im_start|>user
Classify this text as to whether it displays closed-mindedness: "{text}"
If this text displays closed-mindedness, your response must be "Yes".
If this text doesn\'t display closed-mindedness, your response must be "No".
<|im_end|>
<|im_start|>assistant
'''

      return prompt
  