from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator

class ClassificationSchema(BaseModel):
    """
    Schema for classification data from Visma Lon HR.
    Represents classification information from the VISMALØN table IP_KODE.
    """
    
    ClassificationRID: str = Field(..., description="Unique key for use of OData")
    VersionNumber: str = Field(..., description="Used to control the update of data (internal Datahub field)")
    CustomerID: str = Field(..., description="Customer ID")
    ContentTypeCode: str = Field(..., description="Ex. 350")
    ClassificationCode: str = Field(..., description="Ex. 6 digit Disco-08 code")
    StartDate: datetime = Field(..., description="Start date")
    EndDate: Optional[datetime] = Field(None, description="End date")
    ClassificationName: str = Field(..., description="Name of IP_kode")
    CreateTime: datetime = Field(..., description="Timestamp for creating the registration")
    UpdateTime: datetime = Field(..., description="Timestamp for latest update of the registration")
    
    @field_validator('StartDate', 'EndDate', 'CreateTime', 'UpdateTime', mode='before')
    @classmethod
    def parse_datetime(cls, v: Optional[str]) -> Optional[datetime]:
        """Parse datetime fields from string"""
        if not v:
            return None
        try:
            return datetime.fromisoformat(v.replace('Z', '+00:00'))
        except (ValueError, AttributeError):
            return None
    
    class Config:
        from_attributes = True
        populate_by_name = True 