import { useEffect, useId, useState } from "react";
import mermaid from "mermaid";

mermaid.initialize({ startOnLoad: false, theme: "neutral" });

export default function Mermaid({ chart }) {
  const id = "m" + useId().replace(/:/g, "");
  const [svg, setSvg] = useState("");
  const [failed, setFailed] = useState(false);

  useEffect(() => {
    let cancelled = false;
    mermaid
      .render(id, chart)
      .then(({ svg }) => !cancelled && (setSvg(svg), setFailed(false)))
      .catch(() => !cancelled && setFailed(true));
    return () => {
      cancelled = true;
    };
  }, [chart, id]);

  if (failed) return <pre><code>{chart}</code></pre>;
  return <div className="mermaid-box" dangerouslySetInnerHTML={{ __html: svg }} />;
}