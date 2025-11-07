from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import compare_two, compare_multi, responses, manage_files

app = FastAPI(title="🚀 iFlow Automation API")

# CORS (allow all for local)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "🚀 iFlow Automation API is running!"}

# include routes
app.include_router(compare_two.router)
app.include_router(compare_multi.router)
app.include_router(responses.router)
app.include_router(manage_files.router)
