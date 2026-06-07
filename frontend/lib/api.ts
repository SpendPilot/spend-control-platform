import { buildApiUrl } from "@/lib/contracts";

export async function apiFetch<T = any>(
  path: string,
  init?: RequestInit & { token?: string | null },
): Promise<T> {
  const response = await fetch(buildApiUrl(path), {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(init?.token ? { Authorization: `Bearer ${init.token}` } : {}),
      ...(init?.headers ?? {}),
    },
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error(await response.text());
  }

  const payload = await response.json();
  return payload.data as T;
}

export function getApiError(error: unknown): string {
  if (error instanceof Error) return error.message;
  return "Unexpected API error";
}
