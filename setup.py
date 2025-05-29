from setuptools import setup, find_packages

setup(
    name="ai_recruiter",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "fastapi==0.109.2",
        "uvicorn==0.27.1",
        "sqlalchemy==2.0.27",
        "pydantic==2.6.1",
        "pydantic-settings==2.1.0",
        "python-dotenv==1.0.1",
        "psycopg2-binary==2.9.9",
        "alembic==1.13.1",
        "openai==1.61.0"
    ]
) 