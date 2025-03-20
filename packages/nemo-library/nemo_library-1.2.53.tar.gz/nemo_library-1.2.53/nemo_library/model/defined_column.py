from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class DefinedColumn:
    categorialType: bool
    columnType: str
    containsSensitiveData: bool
    dataType: str
    description: str
    displayName: str
    formula: str
    groupByColumnInternalName: Optional[str]
    importName: str
    stringSize: int
    unit: str
    internalName: str
    parentAttributeGroupInternalName : str
    id: str
    projectId: str
    tenant: str

    def to_dict(self):
        return asdict(self)
