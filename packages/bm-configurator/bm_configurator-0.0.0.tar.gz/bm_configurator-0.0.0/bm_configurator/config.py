from dataclasses import dataclass
from typing import Dict, Any, Type, TypeVar, List, Optional

T = TypeVar('T', bound='BaseModelConfig')

@dataclass
class HardwareRequirements:
    min_ram: int = 4               # В GB
    requires_gpu: bool = False
    min_vram: int = 0              # Для GPU
    disk_space: int = 1            # В GB


@dataclass
class BaseModelConfig:
    name: str
    model_id: str
    requirements: HardwareRequirements
    description: str = ""
    _rank: int = 0
    tags: Optional[List[str]] = None

    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        # Базовые параметры
        base_params = {
            "name": data["name"],
            "model_id": data["model_id"],
            "requirements": HardwareRequirements(**data["requirements"]),
            "description": data.get("description", ""),
            "_rank": data.get("rank", 0),
            "tags": data.get("tags", [])
        }
        return cls(**base_params)

@dataclass
class DiffusionModelConfig(BaseModelConfig):
    image_size: tuple[int, int] = (512, 512)
    default_steps: int = 25
    supports_controlnet: bool = False

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DiffusionModelConfig":
        # Получаем базовые параметры
        base = vars(super().from_dict(data))
        
        # Параметры специфичные для Diffusion
        diffusion_params = {
            "image_size": tuple(data.get("image_size", (512, 512))),
            "default_steps": data.get("default_steps", 25),
            "supports_controlnet": data.get("supports_controlnet", False)
        }

        base.update(diffusion_params)
        
        # Объединяем параметры
        return cls(
            **base
        )


@dataclass
class LLMModelConfig(BaseModelConfig):
    context_window: int = 2048
    prompt_template: str = "{instruction}"
    api_key_env: Optional[str] = None
    model_type: str = "huggingface"

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LLMModelConfig":
        # Получаем базовые параметры
        base = vars(super().from_dict(data))
        
        # Параметры специфичные для LLM
        llm_params = {
            "context_window": data.get("context_window", 2048),
            "prompt_template": data.get("prompt_template", "{instruction}"),
            "api_key_env": data.get("api_key_env"),
            "model_type": data.get("model_type", "huggingface")
        }

        base.update(llm_params)
        
        return cls(**base)