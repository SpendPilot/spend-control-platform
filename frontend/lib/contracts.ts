export function buildApiUrl(path: string): string {
  const base =
    typeof window !== "undefined" && window.__APP_CONFIG__
      ? window.__APP_CONFIG__.apiBaseUrl
      : process.env.NEXT_PUBLIC_API_BASE_URL?.trim() || "";
  return `${base}${path.startsWith("/") ? path : `/${path}`}`;
}

