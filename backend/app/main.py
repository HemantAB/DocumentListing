from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from .core.config import settings
from .api.endpoints.documents import router
from .database import Base, engine, SessionLocal
from .core.logging import setup_logging
from .models.document import Document

logger = setup_logging()

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc"
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root route
@app.get("/")
async def root():
    """
    Redirect to API documentation
    """
    return RedirectResponse(url=f"{settings.API_V1_STR}/docs")

# Health check endpoint
@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy", "api_version": "1.0.0"}

# Include routers
app.include_router(router, prefix=f"{settings.API_V1_STR}/documents", tags=["documents"])

# Create sample data if needed
@app.on_event("startup")
async def create_sample_data():
    db = SessionLocal()
    try:
        # Check if we already have data
        if db.query(Document).count() == 0:
            logger.info("Creating sample documents...")
            sample_documents = [
                {
                    "name": "Meeting Notes.txt",
                    "content": "Discussion points from team meeting:\n- Project timeline review\n- Resource allocation\n- Next steps"
                },
                {
                    "name": "Project Plan.txt",
                    "content": "Q4 Project Timeline:\n1. Requirements gathering\n2. Design phase\n3. Implementation\n4. Testing\n5. Deployment"
                },
                {
                    "name": "API Documentation.txt",
                    "content": "REST API Endpoints:\n- GET /api/v1/users\n- POST /api/v1/users\n- PUT /api/v1/users/{id}\n- DELETE /api/v1/users/{id}"
                },
                {
                    "name": "Project Plan2.txt",
                    "content": "Q2 Project Timeline:\n1. Requirements gathering\n2. Design phase\n3. Implementation\n4. Testing\n5. Deployment"
                },
                {
                    "name": "Project Plan3.txt",
                    "content": "Q1 Project Timeline:\n1. Requirements gathering\n2. Analysis phase\n3. Design phase\n4. Implementation\n5. Testing\n6. Deployment"
                },
                {
                    "name": "Project Plan4.txt",
                    "content": "Q1 Project Timeline:\n1. Requirements gathering\n2. Design phase\n3. Implementation\n4. Testing\n5. Deployment"
                },
                {
                    "name": "Project Plan5.txt",
                    "content": "2025 Q1 Project Timeline:\n1. Requirements gathering\n2. Design phase\n3. Implementation\n4. Testing\n5. Deployment"
                },
                {
                    "name": "Meeting Notes2.txt",
                    "content": "Discussion points from team meeting:\nFinding remedial remedial measures for the issues:\n- Project timeline review\n- Resource allocation\n- Next steps"
                },
                {
                    "name": "Meeting Notes3.txt",
                    "content": "Discussion points from team meeting:\n- Project timeline review\n- Resource allocation\n- Next steps"
                },
                {
                    "name": "Calculate Market return.txt",
                    "content": "Calculate the expected return\n Assume that the following assets are correctly priced according  to securrity market line (CAPM)"
                },
                {
                    "name": "Calculate Market risk.txt",
                    "content": "Calculate the expected market risk\n Assume that the following assets are correctly priced according  to securrity market line (CAPM)"
                }
                
            ]
            
            for doc in sample_documents:
                db_doc = Document(**doc)
                db.add(db_doc)
            
            db.commit()
            logger.info("Sample documents created successfully")
            
    except Exception as e:
        logger.error(f"Error creating sample data: {str(e)}")
        db.rollback()
    finally:
        db.close()

# Register the startup event
app.add_event_handler("startup", create_sample_data)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
    