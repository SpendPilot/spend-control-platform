"use client";

import { useEffect, useState } from "react";

import { AppShell } from "@/components/app-shell";
import { ErrorState, LoadingState, PageHeader } from "@/components/ui";
import { useAuth } from "@/components/auth-provider";
import { apiFetch, getApiError } from "@/lib/api";

type Member = {
  id: string;
  user_id: string;
  role: string;
  status: string;
  cost_center?: string | null;
};

type SessionItem = {
  id: string;
  auth_provider: string;
  user_agent?: string | null;
  last_seen_at?: string | null;
  revoked_at?: string | null;
};

export default function SettingsPage() {
  const { authMode, profile, token } = useAuth();
  const [members, setMembers] = useState<Member[]>([]);
  const [sessions, setSessions] = useState<SessionItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!token) return;
    Promise.all([
      apiFetch<Member[]>("/api/admin/members", { token }).catch(() => []),
      apiFetch<SessionItem[]>("/api/admin/sessions", { token }).catch(() => []),
    ])
      .then(([nextMembers, nextSessions]) => {
        setMembers(nextMembers);
        setSessions(nextSessions);
      })
      .catch((nextError) => setError(getApiError(nextError)))
      .finally(() => setLoading(false));
  }, [token]);

  if (loading) return <LoadingState label="Loading tenant settings..." />;
  if (error) return <ErrorState label={error} />;

  return (
    <AppShell>
      <div className="space-y-6">
        <PageHeader
          title="Settings"
          description="Authentication, tenant, role, and active session visibility for the current organization."
        />

        <div className="grid gap-4 xl:grid-cols-2">
          <div className="panel p-6">
            <div className="text-sm uppercase tracking-[0.25em] text-slate-400">Authentication</div>
            <h2 className="mt-2 font-display text-2xl">Session</h2>
            <div className="mt-4 space-y-2 text-sm text-slate-600 dark:text-slate-300">
              <div>User: {profile?.user.display_name}</div>
              <div>Email: {profile?.user.email}</div>
              <div>Role: {profile?.effective_role}</div>
              <div>Mode: {authMode}</div>
              <div>Tenant: {profile?.organization.name}</div>
            </div>
          </div>

          <div className="panel p-6">
            <div className="text-sm uppercase tracking-[0.25em] text-slate-400">Routing</div>
            <h2 className="mt-2 font-display text-2xl">Gateway layout</h2>
            <p className="mt-4 text-sm text-slate-600 dark:text-slate-300">
              Browser traffic is expected to stay same-origin and reach the backend via Azure Front Door, WAF,
              kGateway, and HTTPRoutes that split identity, finance, and document paths.
            </p>
          </div>
        </div>

        <div className="grid gap-4 xl:grid-cols-2">
          <div className="panel p-6">
            <div className="text-sm uppercase tracking-[0.25em] text-slate-400">Members</div>
            <h2 className="mt-2 font-display text-2xl">{members.length} organization memberships</h2>
            <div className="mt-4 space-y-3 text-sm">
              {members.map((member) => (
                <div key={member.id} className="rounded-2xl bg-slate-100 px-4 py-3 dark:bg-slate-800/60">
                  {member.role} · {member.status}
                </div>
              ))}
            </div>
          </div>

          <div className="panel p-6">
            <div className="text-sm uppercase tracking-[0.25em] text-slate-400">Sessions</div>
            <h2 className="mt-2 font-display text-2xl">{sessions.length} tracked sessions</h2>
            <div className="mt-4 space-y-3 text-sm">
              {sessions.map((session) => (
                <div key={session.id} className="rounded-2xl bg-slate-100 px-4 py-3 dark:bg-slate-800/60">
                  {session.auth_provider} · {session.revoked_at ? "revoked" : "active"}
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </AppShell>
  );
}
