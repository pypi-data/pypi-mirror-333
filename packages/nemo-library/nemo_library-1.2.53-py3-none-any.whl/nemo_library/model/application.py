from dataclasses import dataclass, asdict
from typing import Dict, List

@dataclass
class Forecast:
    groupBy: str
    metric: str

@dataclass
class PageReference:
    order: int
    page: str
    
@dataclass
class Application:
    active: bool
    description: str
    descriptionTranslations: Dict[str, str]
    displayName: str
    displayNameTranslations: Dict[str, str]
    download: str
    forecasts: List[Forecast]
    formatCompact: bool
    internalName: str
    links: List[str]
    models: List[str]
    pages: List[PageReference]
    scopeName: str
    id: str
    projectId: str
    tenant: str


    def to_dict(self):
        return asdict(self)
