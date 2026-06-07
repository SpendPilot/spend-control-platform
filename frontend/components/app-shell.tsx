"use client";

import Link from "next/link";
import { useEffect } from "react";
import { usePathname, useRouter } from "next/navigation";
import {
  BadgeIndianRupee,
  FileScan,
  LayoutDashboard,
  Moon,
  ReceiptText,
  Settings2,
  ShieldCheck,
  Sun,
  WalletCards,
} from "lucide-react";
import { useTheme } from "next-themes";

import { useAuth } from "@/components/auth-provider";
import { cn } from "@/lib/utils";

const navigation = [
  { href: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { href: "/expenses", label: "Expenses", icon: ReceiptText },
  { href: "/approvals", label: "Approvals", icon: ShieldCheck },
  { href: "/budgets", label: "Budgets", icon: WalletCards },
  { href: "/documents", label: "Documents", icon: FileScan },
  { href: "/scan", label: "Capture", icon: BadgeIndianRupee },
  { href: "/settings", label: "Settings", icon: Settings2 },
];

export function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();
  const { resolvedTheme, setTheme } = useTheme();
  const { ready, token, profile, logout } = useAuth();

  useEffect(() => {
    if (ready && !token) {
      router.push("/login");
    }
  }, [ready, token, router]);

  if (!ready || !token || !profile) {
    return null;
  }

  return (
    <div className="min-h-screen px-4 py-4 lg:px-6">
      <div className="mx-auto grid min-h-[calc(100vh-2rem)] max-w-[1600px] gap-4 lg:grid-cols-[300px_1fr]">
        <aside className="panel hidden flex-col justify-between p-6 lg:flex">
          <div>
            <div className="rounded-3xl bg-slate-950 p-5 text-white dark:bg-slate-800">
              <div className="text-xs uppercase tracking-[0.35em] text-sky-300">Spend Control</div>
              <div className="mt-3 font-display text-2xl">Finance OS</div>
              <p className="mt-2 text-sm text-slate-300">
                Tenant-aware finance workflows with Entra ID, approvals, budgets, and AI-assisted invoice extraction.
              </p>
            </div>
            <nav className="mt-6 space-y-2">
              {navigation.map((item) => {
                const Icon = item.icon;
                const active = pathname === item.href;
                return (
                  <Link
                    key={item.href}
                    href={item.href}
                    className={cn(
                      "flex items-center gap-3 rounded-2xl px-4 py-3 text-sm transition",
                      active
                        ? "bg-sky-500 text-white shadow-lg shadow-sky-500/20"
                        : "text-slate-600 hover:bg-slate-100 dark:text-slate-300 dark:hover:bg-slate-800",
                    )}
                  >
                    <Icon className="h-4 w-4" />
                    {item.label}
                  </Link>
                );
              })}
            </nav>
          </div>
          <div className="rounded-3xl border border-slate-200/80 p-4 dark:border-slate-800">
            <div className="text-sm text-slate-400">{profile.organization.name}</div>
            <div className="mt-1 font-medium">{profile.user.display_name}</div>
            <div className="text-sm text-slate-500">{profile.effective_role}</div>
          </div>
        </aside>
        <div className="space-y-4">
          <header className="panel flex flex-col gap-4 p-4 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <div className="text-xs uppercase tracking-[0.3em] text-slate-400">Business finance control</div>
              <div className="mt-1 font-display text-2xl">Spend Control Platform</div>
            </div>
            <div className="flex items-center gap-3">
              <button
                className="rounded-2xl border border-slate-200 p-3 dark:border-slate-700"
                onClick={() => setTheme(resolvedTheme === "dark" ? "light" : "dark")}
              >
                {resolvedTheme === "dark" ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
              </button>
              <button
                className="rounded-2xl bg-slate-950 px-4 py-3 text-sm font-medium text-white dark:bg-white dark:text-slate-950"
                onClick={() => void logout().then(() => router.push("/login"))}
              >
                Sign out
              </button>
            </div>
          </header>
          <main>{children}</main>
        </div>
      </div>
    </div>
  );
}
