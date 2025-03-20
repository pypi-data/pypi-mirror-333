from typing import TypedDict
from typing import Generic, TypeVar, Mapping
from datetime import datetime

UMeta = TypeVar("UMeta", bound=Mapping | None)
StoreIdx = TypeVar("StoreIdx", bound=Mapping | str | int | None)


class FlowRunData(TypedDict, Generic[UMeta, StoreIdx], total=False):
    # asset bound data
    metadata: UMeta
    asset_name: str
    flow_name: str
    module_name: str | None

    # runtime data
    ds: str
    ts: str
    data_interval_start: datetime
    data_interval_end: datetime
    parents: dict[str, "FlowRunData"] | None

    # generated data
    store_entry_idx: StoreIdx | None
    # data_interval_start: datetime
