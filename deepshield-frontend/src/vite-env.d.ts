/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_URL: string
  readonly VITE_INSTAGRAM_APP_ID: string
  readonly VITE_INSTAGRAM_APP_SECRET: string
  readonly VITE_ENABLE_DEEPFAKE_DETECTION: string
  readonly VITE_ENABLE_FAKE_ACCOUNT_DETECTION: string
  readonly VITE_ENABLE_CONTENT_FILTERING: string
  readonly VITE_ENABLE_KYC: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
