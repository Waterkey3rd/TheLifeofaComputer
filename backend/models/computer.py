from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict

class ComputerModel(BaseModel):
    model_id: str = "default_pc"
    display_name: str = "普通笔记本"
    base_health_hardware: int = 100
    base_health_system: int = 100
    cooling_material: str = "silicone"  # silicone | liquid_metal
    is_memory_upgradeable: bool = True
    is_apple_silicon: bool = False
    price_tier: float = 1.0

class ComputerState(BaseModel):
    model_config = ConfigDict(extra='ignore')
    
    health_hardware: int = 100
    health_system: int = 100
    health_storage: int = 100
    health_software: int = 100
    
    # 隐藏属性
    machine_flags: Dict[str, int] = {
        "dust_level": 0,
        "has_malware": 0
    }
