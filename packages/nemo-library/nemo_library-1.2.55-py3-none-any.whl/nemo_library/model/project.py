from dataclasses import asdict, dataclass, field
from typing import List, Optional, Dict
from datetime import datetime


@dataclass
class ColumnInfo:
    id: str
    internalName: str
    displayName: str


@dataclass
class ErrorDetails:
    id: str
    fileOnlyColumns: List[ColumnInfo] = field(default_factory=list)
    metadataOnlyColumns: List[ColumnInfo] = field(default_factory=list)


@dataclass
class Warning:
    id: str
    importWarningType: str
    columnId: str
    metadataDataType: str
    databaseDataType: str
    rowNumber: int
    rawRowNumber: int
    fieldName: str
    fieldNumber: int
    fieldValue: str
    maxLength: int


@dataclass
class DataSourceImportRecord:
    id: str
    uploadId: str
    status: str
    errorType: str
    staDateTime: datetime
    endDateTime: datetime
    startedByUsername: str
    recordsOmittedDueToWarnings: int
    warnings: List[Warning] = field(default_factory=list)
    errorDetails: Optional[ErrorDetails] = None


@dataclass
class Project:
    id: str = ""
    metadataTemplateId: str = ""
    tableName: str = ""
    displayName: str = None
    status: str = ""
    type: str = ""
    description: str = ""
    dataSourceImportErrorType: str = ""
    tenant: str = ""
    expDateFrom: datetime = ""
    expDateTo: datetime = ""
    processDateColumnName: str = ""
    numberOfRecords: int = None
    showInitialConfiguration: bool = True
    autoDataRefresh: bool = True
    dataSourceImportRecords: List[DataSourceImportRecord] = field(default_factory=list)

    def to_dict(self):
        return asdict(self)
