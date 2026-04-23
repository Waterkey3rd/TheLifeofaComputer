from models.player import PlayerState
from typing import Dict, Any

def apply_outcome(state: PlayerState, stat_changes: Dict[str, Any]):
    # Apply changes
    h = state.health_status
    a = state.attributes
    hd = h.hardware_details
    
    for key, val in stat_changes.items():
        if key == "health_hardware": 
            h.hardware += val
            hd.fan += val
            hd.shell += val
        elif key == "hw_cpu": hd.cpu += val
        elif key == "hw_disk": hd.disk += val
        elif key == "hw_ram": hd.ram += val
        elif key == "hw_screen": hd.screen += val
        elif key == "hw_fan": hd.fan += val
        elif key == "hw_shell": hd.shell += val
        elif key == "health_system": h.system += val
        elif key == "health_storage": h.storage += val
        elif key == "health_software": h.software += val
        elif key == "mental_state": a.mental_state += val
        elif key == "wealth": a.wealth += val
        elif key == "cyber_sense": a.cyber_sense += val
        
        # Recalculate average hardware health based on parts
        parts = [hd.cpu, hd.disk, hd.ram, hd.screen, hd.fan, hd.shell]
        h.hardware = max(0, min(100, sum(parts) // len(parts)))
    
    # Boundary clamps
    def clamp(v, limit=100): return max(0, min(v, limit))
    h.hardware = clamp(h.hardware)
    h.system = clamp(h.system)
    h.storage = clamp(h.storage)
    h.software = clamp(h.software)
    a.mental_state = clamp(a.mental_state)
    a.wealth = max(0, a.wealth)

def end_of_day_calculation(state: PlayerState):
    """
    Daily calculation of passive modifiers.
    """
    inv = state.inventory
    flags = state.hidden_flags
    
    # Natural decay
    if "dust_level" not in flags.machine_flags:
        flags.machine_flags.append("dust_level")
        
    dust_level = flags.machine_flags.count("dust_level")
    
    # Passive items logic
    damage = dust_level
    if "散热支架" in inv:
        damage = max(0, damage - 3)
    
    state.health_status.hardware = max(0, state.health_status.hardware - damage)
    
    if "炫酷机械键盘" in inv:
        state.attributes.mental_state = min(100, state.attributes.mental_state + 5)
        
    return state
