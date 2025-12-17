import "dotenv/config";
import cors from "cors";
import express, { Request, Response } from "express";
import {
  CopilotRuntime,
  ExperimentalEmptyAdapter,
  copilotRuntimeNodeHttpEndpoint,
} from "@copilotkit/runtime";
import { LangGraphHttpAgent } from "@copilotkit/runtime/langgraph";

const app = express();
const port = process.env.PORT || 4000;
const corsOrigins = (process.env.CORS_ORIGINS || "http://localhost:5173")
  .split(",")
  .map((origin) => origin.trim());

app.use(cors({ origin: corsOrigins, credentials: true }));

const serviceAdapter = new ExperimentalEmptyAdapter();
const backendUrl = process.env.BACKEND_URL || "http://localhost:8000";

const runtime = new CopilotRuntime({
  agents: {
    sample_agent: new LangGraphHttpAgent({
      url: `${backendUrl}/copilotkit/sample_agent`,
    }),
    joke_agent: new LangGraphHttpAgent({
      url: `${backendUrl}/copilotkit/joke_agent`,
    }),
  },
});

const copilotHandler = copilotRuntimeNodeHttpEndpoint({
  runtime,
  serviceAdapter,
  endpoint: "/copilotkit",
});

app.use("/copilotkit", (req: Request, res: Response) => {
  return copilotHandler(req, res);
});

app.listen(port, () => {
  console.log(`Runtime server running on http://localhost:${port}`);
});
