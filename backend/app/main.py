# app/main.py
"""
GreenChain FastAPI Application
Main entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database.session import init_db
from app.api.v1 import api_router
from app.blockchain.blockchain import blockchain

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="Blockchain-powered crop insurance platform"
)

# CORS middleware (for Streamlit frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.on_event("startup")
async def startup_event():
    """
    Run on application startup
    """
    print("\n" + "="*70)
    print(f"🌾 {settings.APP_NAME} v{settings.VERSION}")
    print("="*70 + "\n")
    
    # Initialize database
    init_db()
    
    # Show blockchain stats
    stats = blockchain.get_stats()
    print(f"⛓️  Blockchain: {stats['total_blocks']} blocks, {stats['total_transactions']} transactions")
    print(f"✅ Blockchain valid: {stats['is_valid']}")
    
    print(f"\n🚀 API running at: http://localhost:8000")
    print(f"📚 API docs: http://localhost:8000/docs")
    print(f"🔐 Demo mode: {settings.DEMO_MODE}\n")


@app.get("/")
def root():
    """
    Root endpoint
    """
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.VERSION,
        "docs": "/docs",
        "blockchain": blockchain.get_stats()
    }


@app.get("/health")
def health_check():
    """
    Health check endpoint
    """
    is_valid, message = blockchain.is_chain_valid()
    
    return {
        "status": "healthy",
        "database": "connected",
        "blockchain": {
            "valid": is_valid,
            "blocks": len(blockchain.chain)
        }
    }


@app.get("/blockchain/stats")
def get_blockchain_stats():
    """
    Get blockchain statistics
    """
    return blockchain.get_stats()


@app.get("/blockchain/blocks")
def get_all_blocks():
    """
    Get all blocks (for demo/visualization)
    """
    return {
        "total_blocks": len(blockchain.chain),
        "blocks": [block.to_dict() for block in blockchain.chain]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
