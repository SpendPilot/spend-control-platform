"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

import { AppShell } from "@/components/app-shell";
import { EmptyState, ErrorState, LoadingState, PageHeader } from "@/components/ui";
import { useAuth } from "@/components/auth-provider";
import { apiFetch, getApiError } from "@/lib/api";

type DocumentItem = {
  document: {
    id: string;
    filename: string;
    status: string;
    created_at: string;
  };
  latest_scan?: {
    risk_level: string;
    summary: string;
  } | null;
};

export default function DocumentsPage() {
  const { token } = useAuth();
  const [items, setItems] = useState<DocumentItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!token) return;
    apiFetch<DocumentItem[]>("/api/documents", { token })
      .then(setItems)
      .catch((err) => setError(getApiError(err)))
      .finally(() => setLoading(false));
  }, [token]);

  if (loading) return <LoadingState label="Loading documents..." />;
  if (error) return <ErrorState label={error} />;
  if (!items.length) {
    return (
      <AppShell>
        <EmptyState
          title="No documents uploaded"
          description="Use the Scan page to upload a policy, contract, invoice, or supporting document."
        />
      </AppShell>
    );
  }

  return (
    <AppShell>
      <div className="space-y-6">
        <PageHeader
          title="Documents"
          description="Receipts, invoices, and supporting files stay linked to the finance workspace and keep the latest AI scan attached."
        />
        <div className="grid gap-4">
          {items.map((item) => (
            <Link
              key={item.document.id}
              href={`/documents/${item.document.id}`}
              className="panel block rounded-3xl p-6 transition hover:-translate-y-0.5"
            >
              <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
                <div>
                  <div className="font-display text-2xl">{item.document.filename}</div>
                  <div className="mt-2 text-sm text-slate-500">
                    Uploaded {new Date(item.document.created_at).toLocaleString()}
                  </div>
                </div>
                <div className="rounded-full bg-slate-100 px-4 py-2 text-xs uppercase tracking-[0.25em] dark:bg-slate-800">
                  {item.latest_scan?.risk_level ?? item.document.status}
                </div>
              </div>
              <p className="mt-4 text-sm text-slate-600 dark:text-slate-300">
                {item.latest_scan?.summary ?? "No scan result yet. Open the detail page to trigger analysis."}
              </p>
            </Link>
          ))}
        </div>
      </div>
    </AppShell>
  );
}
