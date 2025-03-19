from abc import ABC
from typing import Dict, Any, Protocol, runtime_checkable
from dataclasses import dataclass

@dataclass
class ActionContext:
    instance_id: str
    customer_id: str
    current_state: str
    next_state: str
    workflow_context: Dict[str, Any]
    action_data: Dict[str, Any]

class ActionRunner(ABC):
    async def run_action(self, action_type: str, context: ActionContext) -> bool:
        pass
