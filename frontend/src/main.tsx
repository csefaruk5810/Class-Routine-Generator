import React from "react";
import ReactDOM from "react-dom/client";

function App() {
  return (
    <main style={{ fontFamily: "Georgia, serif", padding: "2rem" }}>
      <h1>Automated Class Routine Generator</h1>
      <p>Frontend scaffold is ready for feature implementation.</p>
    </main>
  );
}

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
