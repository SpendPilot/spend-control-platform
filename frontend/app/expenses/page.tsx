"use client";

import { useEffect, useState } from "react";

import { AppShell } from "@/components/app-shell";
import { EmptyState, ErrorState, LoadingState, PageHeader } from "@/components/ui";
import { useAuth } from "@/components/auth-provider";
import { apiFetch, getApiError } from "@/lib/api";

type ExpenseItem = {
  id: string;
  title: string;
  vendor_name?: string | null;
  amount: number;
  currency: string;
  expense_date: string;
  status: string;
  policy_status: string;
  ai_risk_level?: string | null;
};

export default function ExpensesPage() {
  const { token } = useAuth();
  const [items, setItems] = useState<ExpenseItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!token) return;
    apiFetch<ExpenseItem[]>("/api/finance/expenses", { token })
      .then(setItems)
      .catch((err) => setError(getApiError(err)))
      .finally(() => setLoading(false));
  }, [token]);

  if (loading) return <LoadingState label="Loading expenses..." />;
  if (error) return <ErrorState label={error} />;
  if (!items.length) {
    return (
      <AppShell>
        <EmptyState
          title="No expenses yet"
          description="Use the Capture page to upload a receipt or create an expense from the finance API."
        />
      </AppShell>
    );
  }

  return (
    <AppShell>
      <div className="space-y-6">
        <PageHeader
          title="Expenses"
          description="Submitted and approved spend for your organization, including AI policy hints."
        />
        <div className="grid gap-4">
          {items.map((item) => (
            <div key={item.id} className="panel p-6">
              <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
                <div>
                  <div className="font-display text-2xl">{item.title}</div>
                  <div className="mt-2 text-sm text-slate-500">
                    {item.vendor_name || "Vendor pending"} · {new Date(item.expense_date).toLocaleDateString()}
                  </div>
                </div>
                <div className="text-right">
                  <div className="font-display text-3xl">
                    {item.currency} {Number(item.amount).toFixed(2)}
                  </div>
                  <div className="mt-2 rounded-full bg-slate-100 px-4 py-2 text-xs uppercase tracking-[0.25em] dark:bg-slate-800">
                    {item.status}
                  </div>
                </div>
              </div>
              <div className="mt-4 grid gap-3 sm:grid-cols-3">
                <div className="rounded-2xl bg-slate-100 px-4 py-3 text-sm dark:bg-slate-800/60">
                  Policy: {item.policy_status}
                </div>
                <div className="rounded-2xl bg-slate-100 px-4 py-3 text-sm dark:bg-slate-800/60">
                  AI risk: {item.ai_risk_level || "pending"}
                </div>
                <div className="rounded-2xl bg-slate-100 px-4 py-3 text-sm dark:bg-slate-800/60">
                  ID: {item.id.slice(0, 8)}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </AppShell>
  );
}
