from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import logging

from src.app.db.session import Base, engine
from src.app.models.models import Company, JobPosting

logger = logging.getLogger(__name__)


def init_db() -> None:
    try:
        # Create tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except SQLAlchemyError as e:
        logger.error(f"Error creating database tables: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during database initialization: {str(e)}")
        raise


if __name__ == "__main__":
    init_db() 