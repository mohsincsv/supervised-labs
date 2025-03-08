import json
from typing import List
from data_classes.flow import Flow


def save_flows(flows: List[Flow], filename: str = "flows.json"):
    with open(filename, "w") as f:
        json.dump([flow.to_dict() for flow in flows], f)


def load_flows(filename: str = "flows.json") -> List[Flow]:
    try:
        with open(filename, "r") as f:
            return [Flow.from_dict(flow_dict) for flow_dict in json.load(f)]
    except FileNotFoundError:
        return []