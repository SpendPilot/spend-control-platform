"use client";

import { useEffect, useMemo, useState } from "react";

import { AppShell } from "@/components/app-shell";
import { EmptyState, ErrorState, LoadingState, PageHeader } from "@/components/ui";
import { useAuth } from "@/components/auth-provider";
import { apiFetch, getApiError } from "@/lib/api";

type BudgetItem = {
  id: string;
  name: string;
  amount: number;
  currency: string;
  start_date: string;
  end_date: string;
  alert_threshold_percent: number;
  spent_amount: number;
  category?: { name: string } | null;
};

export default function BudgetsPage() {
  const { token } = useAuth();
  const [items, setItems] = useState<BudgetItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!token) return;
    apiFetch<BudgetItem[]>("/api/finance/budgets", { token })
      .then(setItems)
      .catch((err) => setError(getApiError(err)))
      .finally(() => setLoading(false));
  }, [token]);

  const totals = useMemo(() => {
    const budgeted = items.reduce((sum, item) => sum + Number(item.amount), 0);
    const consumed = items.reduce((sum, item) => sum + Number(item.spent_amount), 0);
    return { budgeted, consumed };
  }, [items]);

  if (loading) return <LoadingState label="Loading budgets..." />;
  if (error) return <ErrorState label={error} />;
  if (!items.length) {
    return (
      <AppShell>
        <EmptyState
          title="No budgets configured"
          description="Create a budget through the finance API or bootstrap one during onboarding."
        />
      </AppShell>
    );
  }

  return (
    <AppShell>
      <div className="space-y-6">
        <PageHeader
          title="Budgets"
          description="Active controls for planned spend versus approved spend by budget window and category."
        />
        <div className="grid gap-4 md:grid-cols-2">
          <div className="panel p-6">
            <div className="text-sm uppercase tracking-[0.25em] text-slate-400">Planned</div>
            <div className="mt-3 font-display text-4xl">INR {totals.budgeted.toFixed(2)}</div>
          </div>
          <div className="panel p-6">
            <div className="text-sm uppercase tracking-[0.25em] text-slate-400">Consumed</div>
            <div className="mt-3 font-display text-4xl">INR {totals.consumed.toFixed(2)}</div>
          </div>
        </div>
        <div className="grid gap-4">
          {items.map((item) => {
            const utilization = item.amount ? (Number(item.spent_amount) / Number(item.amount)) * 100 : 0;
            return (
              <div key={item.id} className="panel p-6">
                <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
                  <div>
                    <div className="font-display text-2xl">{item.name}</div>
                    <div className="mt-2 text-sm text-slate-500">
                      {item.category?.name || "All categories"} · {new Date(item.start_date).toLocaleDateString()} to{" "}
                      {new Date(item.end_date).toLocaleDateString()}
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="font-display text-2xl">
                      {item.currency} {Number(item.spent_amount).toFixed(2)} / {Number(item.amount).toFixed(2)}
                    </div>
                    <div className="mt-2 text-sm text-slate-500">
                      Threshold {item.alert_threshold_percent}% · Utilization {utilization.toFixed(1)}%
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </AppShell>
  );
}
