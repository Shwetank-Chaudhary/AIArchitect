import { useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import Mermaid from "./Mermaid";
import "./App.css";

const API_URL = "http://localhost:8000/create_architecture"; // change to your backend endpoint
const CLOUDS = ["azure", "aws"];

export default function App() {
  const [idea, setIdea] = useState("");
  const [cloud, setCloud] = useState(CLOUDS[0]);
  const [markdown, setMarkdown] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleRender = async () => {
    if (!idea.trim()) {
      setError("Describe your business idea first.");
      return;
    }
    setLoading(true);
    setError("");
    setMarkdown("");
    try {
      const res = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ raw_text: idea.trim(), cloud_infra: cloud }),
      });
      if (!res.ok) throw new Error(`Backend returned ${res.status}`);
      const data = await res.json();
      setMarkdown(data.architecture ?? "");
    } catch (e) {
      setError(`Could not generate the design. ${e.message}`);
    } finally {
      setLoading(false);
    }
  };

  const components = {
    code({ className, children, ...props }) {
      const lang = /language-(\w+)/.exec(className || "")?.[1];
      const text = String(children).replace(/\n$/, "");
      if (lang === "mermaid") return <Mermaid chart={text} />;
      return (
        <code className={className} {...props}>
          {children}
        </code>
      );
    },
    table: ({ children }) => (
      <div className="table-wrap">
        <table>{children}</table>
      </div>
    ),
  };

  return (
    <main className={`page ${markdown ? "has-result" : ""}`}>
      <section className="form">
        <h1>What are you building?</h1>
        <label htmlFor="idea">Business idea</label>
        <input
          id="idea"
          type="text"
          value={idea}
          placeholder="e.g. A todo list app that syncs across devices"
          onChange={(e) => setIdea(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && !loading && handleRender()}
        />

        <label htmlFor="cloud">Cloud infra to use</label>
        <select id="cloud" value={cloud} onChange={(e) => setCloud(e.target.value)}>
          {CLOUDS.map((c) => (
            <option key={c} value={c}>
              {c}
            </option>
          ))}
        </select>

        <button onClick={handleRender} disabled={loading}>
          {loading ? "Rendering…" : "Render"}
        </button>
        {error && <p className="error" role="alert">{error}</p>}
      </section>

      {markdown && (
        <article className="output">
          <ReactMarkdown remarkPlugins={[remarkGfm]} components={components}>
            {markdown}
          </ReactMarkdown>
        </article>
      )}
    </main>
  );
}