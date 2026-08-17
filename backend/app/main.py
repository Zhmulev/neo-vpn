from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import engine, Base
from app.models import User, VPNServer, ProxyConfig
from app.api import auth, vpn, proxy, payment

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="NEO VPN API",
    description="Backend for NEO VPN + Proxy Utility",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(vpn.router)
app.include_router(proxy.router)
app.include_router(payment.router)

@app.get("/")
async def root():
    return {"status": "ok", "service": "NEO VPN API"}

@app.get("/health")
async def health():
    return {"status": "healthy"}