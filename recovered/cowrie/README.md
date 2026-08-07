# Recovered: Cowrie / "Financial Intelligence Engine"

## What this is

This directory holds what could be recovered of the **Cowrie** app. Read the
provenance section before assuming this is the app itself — it is not.

| File | What it is |
| --- | --- |
| `vaultfinance-prototype.html` | A complete, runnable single-file demo, extracted verbatim from the AI Studio design chat |
| `design-conversation.txt` | The full 14-message design conversation the prototype came from |

## Provenance

The `mobkilishi/Cowrie` GitHub repo has exactly one commit ("Initial commit"),
containing only the Google AI Studio boilerplate `README.md`. No application
source was ever pushed there — confirmed against full (unshallowed) history and
all remote refs.

The recovered material here comes instead from Google Drive:

- **File:** `Building a Financial Intelligence Engine`
  (`application/vnd.google-makersuite.prompt`, 120,530 bytes)
- **Drive ID:** `1qhp5EWs45vmkQLVebIpOttfIbXMCUpoa`
- Created 2026-06-19, last modified 2026-06-22

## Important: this is the precursor, not Cowrie

The AI Studio applet named **Cowrie** is described in
`applet_access_history.json` as:

> A local-first, private personal and business money tracker in Naira (₦) with
> in-browser OCR, optional Gemini receipt reading, and data export.

The prototype recovered here has **none** of that. It has no OCR, no Gemini
integration, no data export, and no persistence at all — despite the
"LOCAL-ONLY ENCRYPTION" badge in the header, the transaction list is a
hardcoded `useState` array and nothing is written to storage. It is the design
sketch that *preceded* Cowrie, produced mid-conversation, and it is still
branded "VaultFinance".

The built Cowrie applet lives in AI Studio's own backend
(applet id `c71b1c0e-481c-46d0-a0dc-1ec2864c95d5`), which is not reachable from
Drive or GitHub. To get the real source, export it from AI Studio directly.

## Running the prototype

Open `vaultfinance-prototype.html` in a browser. No build step.

Caveats, all inherited from the original and left unmodified:

- Loads React, Babel standalone, Tailwind, Lucide and Recharts from CDNs, so it
  needs a network connection and will not work offline.
- Compiles JSX in the browser via Babel standalone — fine for a demo, not for
  production.
- Only the `dashboard` and `import` tabs render anything. The `inventory`
  ("Trends") and `settings` ("Vault") nav items are dead — no matching branch
  exists in `App`.
- The "Scan Receipt", "Market Voice", "Browse Files" and "Save to Local Vault"
  buttons are non-functional; the modal does not write back to `transactions`.
- `useEffect` is imported but never used. `Recharts` is loaded but never used.
- Seed data is dated 2023 and denominated in ₦ against flour/lunch examples,
  not the beef/spices/freight commodities discussed later in the conversation.

## What the conversation settles

Worth keeping even though the code is thin — the design decisions are the
durable part:

- **Cash flow** tracking, not inventory.
- **Separate vaults** per user; sharing distributes the code, not the data.
- Bank statement as the source of truth, with a "Cash Hole" reconciliation to
  reconstruct the unlogged year.
- Landed cost = purchase + freight, tracked per unit (₦/kg) to rank vendors.
- Priority commodities: **beef, spices, freight**.

The conversation ends on an unanswered question — whether market logging should
be voice notes or a quick calculator.
