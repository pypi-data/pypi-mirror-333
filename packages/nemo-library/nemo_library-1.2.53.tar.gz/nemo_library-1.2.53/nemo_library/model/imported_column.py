from dataclasses import dataclass, asdict, field
from typing import Optional


@dataclass
class ImportedColumn:
    categorialType: bool = False
    columnType: str = "ExportedColumn"
    containsSensitiveData: bool = False
    dataType: str = "string"
    description: str = ""
    displayName: str = None
    formula: str = ""
    groupByColumnInternalName: Optional[str] = field(default_factory=str)
    importName: str = None
    stringSize: int = 0
    unit: str = ""
    internalName: str = None
    parentAttributeGroupInternalName: str = None
    id: str = ""
    projectId: str = ""
    tenant: str = ""

    def to_dict(self):
        return asdict(self)

    def __post_init__(self):
        if self.importName is None:  
            self.importName = self.displayName.lower()

        if self.internalName is None:  
            self.internalName = self.importName          