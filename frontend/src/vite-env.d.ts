/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_URL: string
  readonly VITE_COPILOT_RUNTIME_URL: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
