from pathlib import Path
import yaml
import psutil
from typing import List, Type, TypeVar, Dict, Any, Optional
from config import BaseModelConfig
import subprocess
import os
import warnings as warn

T = TypeVar('T', bound='BaseModelConfig')

class ModelConfigurator:
    def _load_models(self, path: Path) -> List[T]:
        with open(path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
            return [self.model_class.from_dict(m) for m in data.get("models", [])]

    
    @staticmethod
    def _find_cuda_library() -> bool:
        """Поиск CUDA библиотек в стандартных путях"""
        cuda_paths = [
            "/usr/local/cuda/lib64",
            "/usr/lib/x86_64-linux-gnu",
            "C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA\\v*\bin"
        ]
        
        for path in cuda_paths:
            if any(os.path.isfile(os.path.join(path, lib)) 
               for lib in ["libcudart.so", "cudart64_*.dll"]):
                return True
        return False
    
    def _get_gpu_info(self) -> Dict[str, Any]:
        try:
            import torch
            return {
                "has_cuda": torch.cuda.is_available(),
                "vram_gb": torch.cuda.get_device_properties(0).total_memory // (1024**3) if torch.cuda.is_available() else 0
            }
        except Exception:
            pass
        try:
            result = subprocess.run(
                ['nvidia-smi', '--query-gpu=memory.total', '--format=csv,noheader,nounits'],
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True,
                check=True
            )
            if result.returncode == 0:
                vram_mb = int(result.stdout.strip().split('\n')[0])
                return {
                    "has_cuda": True,
                    "vram_gb": vram_mb // 1024
                }
        except (FileNotFoundError, subprocess.CalledProcessError, ValueError):
            pass

        if os.environ.get("CUDA_VISIBLE_DEVICES"):
            warn.warn("VRAM not found default value is 6.")
            return {"has_cuda": True, "vram_gb": 6}

        try:
            cuda_lib = self._find_cuda_library()
            if cuda_lib:
                warn.warn("VRAM not found default value is 6.")
                return {"has_cuda": True, "vram_gb": 6}
        except OSError:
            pass

        return {"has_cuda": False}


    def _get_system_info(self) -> Dict[str, Any]:
        gpu_info = self._get_gpu_info()
        
        return {
            "ram_gb": psutil.virtual_memory().total // (1024**3),
            "gpu_available": gpu_info["has_cuda"],
            "vram_gb": gpu_info.get("vram_gb", 0),
            "disk_space_gb": psutil.disk_usage("/").free // (1024**3),
            "cpu_cores": psutil.cpu_count(logical=False)
        }

    def __init__(self, model_class: Type[T], config_path: Path):
        self.model_class = model_class
        self.models = self._load_models(config_path)
        self.system_info = self._get_system_info()
    
    def _is_model_compatible(self, model: T) -> bool:
        req = model.requirements
        sys = self.system_info
        
        checks = [
            sys["ram_gb"] >= req.min_ram,
            sys["disk_space_gb"] >= req.disk_space,
            not req.requires_gpu or sys["gpu_available"],
            not req.requires_gpu or sys["vram_gb"] >= req.min_vram
        ]
        
        return all(checks)
    
    def get_available_models(self, 
                            filter_tags: Optional[List[str]] = None) -> List[T]:
        compatible = []
        
        for model in self.models:
            if not self._is_model_compatible(model):
                continue
                
            if filter_tags and not any(tag in model.tags for tag in filter_tags):
                continue
                
            compatible.append(model)
        
        return sorted(compatible, key=lambda x: (x._rank))
    
    def print_available_models(self, filter_tags: Optional[List[str]] = None):
        models = self.get_available_models(filter_tags)
        
        print("\n" + "="*50)
        print("System specifications:")
        print(f"- RAM: {self.system_info['ram_gb']}GB")
        print(f"- GPU: {'Available' if self.system_info['gpu_available'] else 'Not available'}")
        if self.system_info['gpu_available']:
            print(f"- VRAM: {self.system_info['vram_gb']}GB")
        print(f"- Disk space: {self.system_info['disk_space_gb']}GB")
        print("="*50)

        print(f"\n\nCompatible models ({self.model_class.__name__}):")

        if not models:
            print("No models matching the system requirements were found.")
            return
        
        for i, model in enumerate(models, 1):
            print(f"\nModel #{i}: {model.name}")
            print(f"Rank: {model._rank}")
            print(f"ID: {model.model_id}")
            print(f"Description: {model.description}")
            print("Requirements:")
            print(f"- Min RAM: {model.requirements.min_ram}GB")
            if model.requirements.requires_gpu:
                print(f"- Requires a GPU with VRAM: {model.requirements.min_vram}GB")
            print(f"- Disk space: {model.requirements.disk_space}GB")
            print(f"Tags: {', '.join(model.tags)}")
            print("-"*50)