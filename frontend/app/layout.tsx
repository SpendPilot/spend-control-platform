import type { Metadata } from "next";
import { IBM_Plex_Sans, Space_Grotesk } from "next/font/google";
import Script from "next/script";

import "./globals.css";
import { Providers } from "@/app/providers";

const sans = IBM_Plex_Sans({
  subsets: ["latin"],
  variable: "--font-sans",
  weight: ["400", "500", "600", "700"],
});

const display = Space_Grotesk({
  subsets: ["latin"],
  variable: "--font-display",
  weight: ["500", "700"],
});

export const metadata: Metadata = {
  title: "Business AI Document Scanner",
  description: "Simplified business document scanning with Entra ID and Azure AI",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  const runtimeConfig = {
    apiBaseUrl: process.env.NEXT_PUBLIC_API_BASE_URL || "/api",
    authMode: process.env.NEXT_PUBLIC_AUTH_MODE || "entra",
    entraFrontendClientId: process.env.NEXT_PUBLIC_ENTRA_FRONTEND_CLIENT_ID || "",
    entraBackendClientId: process.env.NEXT_PUBLIC_ENTRA_BACKEND_CLIENT_ID || "",
    entraApiScope: process.env.NEXT_PUBLIC_ENTRA_API_SCOPE || "",
    entraAuthority: process.env.NEXT_PUBLIC_ENTRA_AUTHORITY || "",
  };

  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`${sans.variable} ${display.variable} font-sans antialiased`}>
        <Script
          id="runtime-config"
          strategy="beforeInteractive"
          dangerouslySetInnerHTML={{
            __html: `window.__APP_CONFIG__ = ${JSON.stringify(runtimeConfig)};`,
          }}
        />
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}

