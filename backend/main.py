from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Middleware to handle different origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],    # Vite server
    allow_methods=["*"],                        # TODO: Revisit later to limit allowed methods
    allow_headers=["*"]
)

@app.get("/api/health")
def health():
    return {"status": "ok"}