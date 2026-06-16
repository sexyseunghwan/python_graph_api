from dataclasses import dataclass, field


@dataclass
class ConsumeInfo:
    total_cost: float
    start_date: str
    end_date: str
    consume_res_list: list[float] = field(default_factory=list)
