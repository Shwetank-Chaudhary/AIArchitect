# Cloud Architecture Generator

Turn a raw business idea into a low-level cloud architecture document. The user enters an idea and picks a cloud provider (Azure or AWS). The backend returns a markdown document covering the folder structure, the cloud services to use, and more. The frontend renders it, including tables and diagrams.

## Repository structure

```text
<repo-name>/
├── backend/     # FastAPI service (LangChain + Ollama / Hugging Face Inference)
└── frontend/    # React + Vite single-page app
```

> Folder names, the entry file (`main.py`) and the model settings below are assumptions. Adjust them to match your repository.

---

## Backend

### Tech stack

- [FastAPI](https://fastapi.tiangolo.com/) for the HTTP API
- [LangChain](https://www.langchain.com/) for prompt and chain orchestration
- [Ollama](https://ollama.com/) for running models locally
- [Hugging Face Inference](https://huggingface.co/docs/huggingface_hub/guides/inference) for hosted model inference

### What it does

It takes a raw business idea and the chosen cloud infrastructure from the user, and generates a markdown document describing the low-level architecture. The document explains the folder structure, the cloud services to use, and related details.

### API

```http
POST /create_architecture
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `raw_text` | string | The raw business idea |
| `cloud_infra` | string | `azure` or `aws` |

Both are sent as Json body

```python
@app.post("/create_architecture")
async def create_architecture(request: Request):
    ...
```

**Response**

```json
{
  "architecture": "# Todo List App: Low-Level Cloud Design\n\n## 1. Overview\n..."
}
```

The `architecture` field holds the markdown. It can include tables, code blocks, and `mermaid` diagrams.

### CORS

The frontend runs on a different origin, so the backend must allow it:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Environment variables

Create `backend/.env` (adjust the names to match your code):

```env
# Hugging Face Inference
HUGGINGFACEHUB_API_TOKEN=your_token_here

# Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=your_model_name
```

---

## Frontend

### Tech stack

- [React](https://react.dev/) (JavaScript) with [Vite](https://vite.dev/)
- [react-markdown](https://github.com/remarkjs/react-markdown) and [remark-gfm](https://github.com/remarkjs/remark-gfm)
- [Mermaid](https://mermaid.js.org/)

### Features

- Business idea input and a **Cloud infra to use** dropdown (`azure` / `aws`)
- **Render** button that calls the backend and shows a loading state
- Markdown output with GitHub-style tables (`remark-gfm`)
- Mermaid code blocks drawn as diagrams, with a raw-code fallback if the diagram is invalid
- Responsive layout with automatic light and dark mode

### Structure

```text
frontend/src/
├── App.jsx       # Form, API call, markdown rendering
├── Mermaid.jsx   # Renders ```mermaid code blocks as SVG diagrams
├── App.css       # All styling (theme tokens, form card, output document)
├── index.css     # Intentionally empty
└── main.jsx      # Vite entry point
```

### Configuration

| Setting | Where | Default |
|---------|-------|---------|
| Backend URL | `API_URL` in `frontend/src/App.jsx` | `http://localhost:8000/create_architecture` |
| Cloud options | `CLOUDS` in `frontend/src/App.jsx` | `["azure", "aws"]` |
| Theme colours | CSS variables at the top of `frontend/src/App.css` | Indigo / blue |

---

## Getting started

### Prerequisites

- [Git](https://git-scm.com/)
- Python 3.10 or later
- Node.js 18 or later
- [Ollama](https://ollama.com/download) installed and running, with your chosen model pulled
- A Hugging Face access token, if the backend uses Hugging Face Inference

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
```

### 2. Start the backend

```bash
cd backend

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Pull the Ollama model (once), then make sure Ollama is running
ollama pull <your-model-name>

# Add your environment variables
cp .env.example .env             # then edit .env

# Run the API
uvicorn main:app --reload --port 8000
```

The API is now at <http://localhost:8000>, and the interactive docs are at <http://localhost:8000/docs>.

### 3. Start the frontend

Open a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open <http://localhost:5173>.

### 4. Use it

1. Describe your business idea in the input.
2. Choose **azure** or **aws** under *Cloud infra to use*.
3. Click **Render** and wait for the generated architecture document.

---

## Frontend scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Start the dev server with hot reload |
| `npm run build` | Create a production build in `frontend/dist/` |
| `npm run preview` | Preview the production build locally |

## Troubleshooting

| Problem | Likely cause |
|---------|--------------|
| "Failed to fetch" in the UI | The backend isn't running, the URL is wrong, or CORS isn't enabled |
| `422` from the backend | Query parameter names don't match `raw_text` and `cloud_infra` |
| Empty output | The response has no `architecture` field |
| Diagram shows as raw code | The Mermaid syntax in the response is invalid |
| Very long ideas fail | Query strings have length limits. Switch the endpoint to a Pydantic model with a JSON body |
| Generation is slow or errors | Check that Ollama is running and the model is pulled, or that your Hugging Face token is valid |
