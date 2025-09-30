import "bootstrap/dist/css/bootstrap.min.css";
import React from "react";

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-vh-100 bg-light">
        <main>{children}</main>
      </body>
    </html>
  );
}
