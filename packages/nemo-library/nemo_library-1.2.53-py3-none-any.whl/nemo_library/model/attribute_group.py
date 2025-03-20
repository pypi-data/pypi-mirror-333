from dataclasses import dataclass, asdict
from typing import Dict


@dataclass
class AttributeGroup:
    attributeGroupType: str
    defaultMetricGroup: bool
    defaultDefinedColumnGroup: bool
    displayName: str
    displayNameTranslations: Dict[str, str]
    isCoupled: bool
    internalName: str
    parentAttributeGroupInternalName : str
    id: str
    projectId: str
    tenant: str

    def to_dict(self):
        return asdict(self)
