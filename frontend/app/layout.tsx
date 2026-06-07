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
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`${sans.variable} ${display.variable} font-sans antialiased`}>
        <Script id="runtime-config" src="/runtime-config" strategy="beforeInteractive" />
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}

