"use client";

import { useEffect, useMemo, useState } from "react";

import { AppShell } from "@/components/app-shell";
import { ChartPanel, MetricStrip } from "@/components/charts";
import { EmptyState, ErrorState, LoadingState, PageHeader } from "@/components/ui";
import { useAuth } from "@/components/auth-provider";
import { apiFetch, getApiError } from "@/lib/api";

type DashboardOut = {
  organization_name: string;
  role: string;
  total_expenses: number;
  approved_spend: number;
  submitted_spend: number;
  pending_approvals: number;
  budgets: {
    budget_id: string;
    name: string;
    limit_amount: number;
    consumed_amount: number;
    utilization_percent: number;
    threshold_percent: number;
  }[];
  category_breakdown: { category: string; amount: number }[];
};

export default function DashboardPage() {
  const { token, profile } = useAuth();
  const [dashboard, setDashboard] = useState<DashboardOut | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!token) return;
    apiFetch<DashboardOut>("/api/finance/dashboard", { token })
      .then(setDashboard)
      .catch((err) => setError(getApiError(err)))
      .finally(() => setLoading(false));
  }, [token]);

  const metrics = useMemo(() => {
    if (!dashboard) return [];
    return [
      { label: "Approved Spend", value: Number(dashboard.approved_spend) },
      { label: "Submitted Spend", value: Number(dashboard.submitted_spend) },
      { label: "Expenses", value: dashboard.total_expenses },
      { label: "Pending", value: dashboard.pending_approvals },
      { label: "Budgets", value: dashboard.budgets.length },
      {
        label: "Budget Alerts",
        value: dashboard.budgets.filter((item) => item.utilization_percent >= item.threshold_percent).length,
      },
    ];
  }, [dashboard]);

  if (loading) return <LoadingState label="Loading dashboard..." />;
  if (error) return <ErrorState label={error} />;
  if (!dashboard) {
    return (
      <AppShell>
        <EmptyState
          title="No finance data yet"
          description="Create a budget or submit your first expense to start building your finance workspace."
        />
      </AppShell>
    );
  }

  return (
    <AppShell>
      <div className="space-y-6">
        <PageHeader
          title={`${dashboard.organization_name} overview`}
          description={`Current role: ${profile?.effective_role}. Spend, budget, and approval signals are combined here for one tenant-aware operating view.`}
        />
        <MetricStrip metrics={metrics} />
        <div className="grid gap-6 xl:grid-cols-2">
          <ChartPanel
            title="Budget utilization"
            kind="bar"
            data={dashboard.budgets.map((item) => ({
              category: item.name,
              total: item.utilization_percent,
            }))}
            xKey="category"
            yKey="total"
          />
          <ChartPanel
            title="Approved spend by category"
            kind="bar"
            data={dashboard.category_breakdown.map((item) => ({
              category: item.category,
              total: Number(item.amount),
            }))}
            xKey="category"
            yKey="total"
          />
        </div>
      </div>
    </AppShell>
  );
}
