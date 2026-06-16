from dataclasses import dataclass, field
from decimal import Decimal


@dataclass
class Assets:
    total_asset_amount_krw: Decimal
    asset_map: dict[str, list["AssetResp"]] = field(default_factory=dict)

@dataclass
class AssetResp:
    asset_type: str
    asset_name: str
    asset_krw: Decimal
    asset_usd: Decimal