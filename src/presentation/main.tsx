import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import Presentation from "./Presentation.tsx";
// @ts-expect-error vscode is stupid can't stop saying this doesn't exist
import "./index.css";

const root = document.getElementById("root")!;

createRoot(root).render(
  <StrictMode>
    <Presentation />
  </StrictMode>,
);
