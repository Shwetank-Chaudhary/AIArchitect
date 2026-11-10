from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/create_architecture")
async def create_architecture(request: Request):
    from agents.Architect import Architect
    from agents.Repromptor import Repromptor
    data = await request.json()
    raw_text = data.get("raw_text")
    cloud_infra = data.get("cloud_infra")
    new_prompt = Repromptor(model = "qwen3:1.7b", llm_type = "ollama").agent_node(raw_text)
    architect = Architect(model = "qwen3:1.7b", llm_type = "ollama")
    architecture = architect.agent_node(new_prompt, cloud_infra)
    return JSONResponse(content={"architecture": architecture},
                        status_code=200)