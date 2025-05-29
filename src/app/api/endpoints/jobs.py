from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from src.app.db.session import get_db
from src.app.models.models import Company, JobPosting
from src.app.schemas import schemas 
from openai import OpenAI


router = APIRouter()


@router.post("/", response_model=schemas.JobPosting)
def create_job_posting(job: schemas.JobPostingCreate, db: Session = Depends(get_db)):
    # verify company exists
    company = db.query(Company).filter(
        Company.id == job.company_id).first()
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")

    db_job = JobPosting(**job.model_dump())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job


@router.get("/", response_model=List[schemas.JobPosting])
def read_job_postings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    jobs = db.query(JobPosting).offset(skip).limit(limit).all()
    return jobs


@router.get("/{job_id}", response_model=schemas.JobPosting)
def read_job(job_id: int, db: Session = Depends(get_db)):
    db_job = db.query(JobPosting).filter(
        JobPosting.id == job_id).first()
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return db_job


@router.put("/{job_id}", response_model=schemas.JobPosting)
def update_job_posting(job_id: int, job: schemas.JobPostingUpdate, db: Session = Depends(get_db)):
    db_job = db.query(JobPosting).filter(
        JobPosting.id == job_id).first()
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    update_data = job.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_job, field, value)

    db.commit()
    db.refresh(db_job)
    return db_job


@router.delete("/{job_id}")
def delete_job(job_id: int, db: Session = Depends(get_db)):
    db_job = db.query(JobPosting).filter(
        JobPosting.id == job_id).first()
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    db.delete(db_job)
    db.commit()
    return {"status": "success", "message": "Job deleted successfully"}

#  create a post call that takes id description accepts a json body with following structure 
@router.post("/{job_id}/description", response_model=schemas.JobDescriptionResponse)
def create_job_description(job_id: int, request: schemas.JobDescriptionRequest, db: Session = Depends(get_db)):
    db_job = db.query(JobPosting).filter(
        JobPosting.id == job_id).first()
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    
    if request.required_tools is None:
        raise HTTPException(status_code=400, detail="Required tools are required")
    
    tools_string = "\n".join(request.required_tools)
    
    prompt = f"""
        First, check if the tools: {tools_string} are valid and exist before using them, if tool doesn't exist do not use it.
        Based on the provided tools, create a brief job description for the position of {db_job.title}.
        Make sure to incorporate these required tools: {tools_string}
    """
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Using a valid model name
        messages=[
            {"role": "system", "content": "You are a professional job description writer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=100
    )
    
    # Update the job description in the database
    db_job.description = response.choices[0].message.content
    db.commit()
    db.refresh(db_job)
    
    return schemas.JobDescriptionResponse(
        job_id=job_id,
        description=response.choices[0].message.content,
        generated_at=datetime.now()
    )

