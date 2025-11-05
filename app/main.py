from fastapi import FastAPI
from app.routes.compare_two import router as compare_two_router
from app.routes.compare_multi import router as compare_multi_router
from app.routes.responses import router as responses_router
from app.routes.health import router as health_router

app = FastAPI(title="CPI Automation API")

app.include_router(compare_two_router, prefix="/compare")
app.include_router(compare_multi_router, prefix="/compare")
app.include_router(responses_router, prefix="/responses")
app.include_router(health_router)


