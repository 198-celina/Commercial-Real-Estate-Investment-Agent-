from typing import Dict
from peft import PeftModel, PeftConfig
from transformers import AutoModelForCausalLM


class LoRAAdapter:
    """LoRA适配器"""
    
    def __init__(self, model_path: str, lora_path: str = None):
        self.model_path = model_path
        self.lora_path = lora_path
        self.model = None
        self.config = None
    
    def load_lora_config(self) -> PeftConfig:
        """加载LoRA配置"""
        if not self.lora_path:
            return None
        
        try:
            self.config = PeftConfig.from_pretrained(self.lora_path)
            return self.config
        except Exception as e:
            print(f"Failed to load LoRA config: {e}")
            return None
    
    def apply_lora(self, base_model: AutoModelForCausalLM) -> AutoModelForCausalLM:
        """将LoRA适配器应用到基础模型"""
        if not self.lora_path:
            return base_model
        
        try:
            model = PeftModel.from_pretrained(
                base_model,
                self.lora_path,
                device_map="auto"
            )
            print("LoRA adapter applied successfully")
            return model
        except Exception as e:
            print(f"Failed to apply LoRA adapter: {e}")
            return base_model
    
    def merge_and_unload(self) -> AutoModelForCausalLM:
        """合并LoRA权重并卸载适配器"""
        if not self.model:
            return None
        
        try:
            merged_model = self.model.merge_and_unload()
            print("LoRA weights merged successfully")
            return merged_model
        except Exception as e:
            print(f"Failed to merge LoRA weights: {e}")
            return self.model
