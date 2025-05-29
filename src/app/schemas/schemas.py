from pydantic import BaseModel, HttpUrl, AnyUrl
from typing import Optional, List
from datetime import datetime

# Company Schemas


class CompanyBase(BaseModel):
    name: str
    industry: Optional[str] = None
    url: Optional[str] = None
    headcount: Optional[int] = None
    country: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    is_public: Optional[bool] = False


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(CompanyBase):
    name: Optional[str] = None


class Company(CompanyBase):
    id: int

    class Config:
        from_attributes = True

# JobPosting Schemas


class JobPostingBase(BaseModel):
    company_id: int
    title: str
    compensation_min: Optional[float] = None
    compensation_max: Optional[float] = None
    location_type: Optional[str] = None
    employment_type: Optional[str] = None
    description: Optional[str] = None


class JobPostingCreate(JobPostingBase):
    pass


class JobPostingUpdate(JobPostingBase):
    company_id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None


class JobPosting(JobPostingBase):
    id: int

    class Config:
        from_attributes = True


# Job Description Request Schema
class JobDescriptionRequest(BaseModel):
    required_tools: List[str]

class JobDescriptionResponse(BaseModel):
    job_id: int
    description: str
    generated_at: datetime