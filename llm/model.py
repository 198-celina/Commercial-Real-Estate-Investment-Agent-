from typing import Dict, Any
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import torch
from config.settings import settings


class LLMModel:
    """千问7B模型封装"""
    
    def __init__(self):
        self.model_path = settings.LLM_MODEL_PATH
        self.lora_path = settings.LLM_LORA_PATH
        self.max_tokens = settings.LLM_MAX_TOKENS
        self.temperature = settings.LLM_TEMPERATURE
        self.tokenizer = None
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """加载模型"""
        try:
            # 加载tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_path,
                trust_remote_code=True
            )
            
            # 配置4-bit量化
            quantization_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.bfloat16
            )
            
            # 加载模型
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_path,
                quantization_config=quantization_config,
                device_map="auto",
                trust_remote_code=True
            )
            
            # 加载LoRA适配器
            if self.lora_path:
                self._load_lora()
            
            print("LLM model loaded successfully")
        except Exception as e:
            print(f"Failed to load LLM model: {e}")
            # 如果加载失败，使用模拟模式
            self.model = None
    
    def _load_lora(self):
        """加载LoRA适配器"""
        try:
            from peft import PeftModel
            self.model = PeftModel.from_pretrained(
                self.model,
                self.lora_path,
                device_map="auto"
            )
            print("LoRA adapter loaded successfully")
        except Exception as e:
            print(f"Failed to load LoRA adapter: {e}")
    
    def generate(self, prompt: str, **kwargs) -> str:
        """生成响应"""
        if not self.model:
            # 模拟响应
            return self._mock_generate(prompt)
        
        try:
            inputs = self.tokenizer(prompt, return_tensors="pt").to("cuda")
            
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=kwargs.get("max_new_tokens", self.max_tokens),
                    temperature=kwargs.get("temperature", self.temperature),
                    do_sample=True,
                    top_p=0.8
                )
            
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            return response
        except Exception as e:
            print(f"LLM generation error: {e}")
            return self._mock_generate(prompt)
    
    def _mock_generate(self, prompt: str) -> str:
        """模拟生成响应"""
        return f"根据您的问题，我已完成分析。这是针对'{prompt[:50]}...'的专业回答。" \
               "由于实际模型未加载，此为模拟响应。在生产环境中，将基于千问7B+LoRA模型" \
               "生成详细的商业地产投资分析报告。"
    
    def chat(self, messages: list, **kwargs) -> Dict[str, Any]:
        """聊天模式"""
        # 构建prompt
        prompt = ""
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if role == "system":
                prompt += f"【系统】{content}\n"
            elif role == "user":
                prompt += f"【用户】{content}\n"
            elif role == "assistant":
                prompt += f"【助手】{content}\n"
        
        prompt += "【助手】"
        
        response = self.generate(prompt, **kwargs)
        
        return {
            "response": response,
            "total_tokens": len(self.tokenizer.encode(response)) if self.tokenizer else 0
        }


llm_model = LLMModel()
