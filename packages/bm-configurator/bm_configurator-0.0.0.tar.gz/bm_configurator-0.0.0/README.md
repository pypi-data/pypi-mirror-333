
---

# Model Configurator

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**A smart configuration system that collects model specifications in config files and selects suitable options for local deployment on target devices.**

---

## Key Features

- 🗂 **Centralized Model Catalog** - Manage all model specifications in YAML config files
- 🖥 **Device Compatibility Engine** - Automatically detects hardware capabilities:
  - RAM/VRAM availability
  - GPU support and memory
  - Disk space requirements
- 🎯 **Smart Selection** - Recommends optimal models based on:
  - Device constraints
  - Performance priorities
  - Model ranking system
- 🛠 **Extensible Architecture** - Supports multiple model types through config inheritance

---

## Installation

```bash
pip install bm_configurator
```

From source:
```bash
git clone https://github.com/Dmatryus/bm_configurator
cd bm_configurator
pip install .
```

---

## Basic Usage

```python
from pathlib import Path

from bm_configurator import DiffusionModelConfig, LLMModelConfig, ModelConfigurator

configurator = ModelConfigurator(
    model_class=DiffusionModelConfig,
    config_path=Path("./configs/diffusion_models.yaml")
)

configurator.print_available_models()
```

---

## Configuration Example (`models.yaml`)

```yaml
models:
  - name: "Tiny Diffusion"
    model_id: "parlance/diffusion_mini"
    description: "Ultra-light CPU model"
    requirements:
      min_ram: 4
      requires_gpu: false
      disk_space: 1
    tags: ["cpu", "low-res", "fast"]
    image_size: [256, 256]
    default_steps: 15
    rank: 3

  - name: "SD 1.5 Optimized"
    model_id: "runwayml/stable-diffusion-v1-5"
    description: "The balance of quality and speed"
    requirements:
      min_ram: 8
      requires_gpu: true
      min_vram: 4
      disk_space: 2
    tags: ["mid-tier-gpu", "general-use"]
    image_size: [512, 512]
    default_steps: 25
    rank: 2
```
---

## Contribution

We welcome contributions! Please see our [Contribution Guidelines](CONTRIBUTING.md) for:
- Adding new hardware detection methods
- Supporting additional model types
- Improving compatibility checks

---

## License

MIT License. See [LICENSE](LICENSE) for full text.
