# Owner steps: publish this Actor on Apify

Sources: Apify docs pages ([GitHub integration](https://docs.apify.com/platform/integrations/github), [Publishing](https://docs.apify.com/platform/actors/publishing), [Set up monetization](https://docs.apify.com/actors/monetize/set-up-monetization), [Manage payouts](https://docs.apify.com/platform/actors/publishing/monetize/monthly-payouts)). They were checked through search extracts because the docs site is not reachable from Claude's environment, so exact button names may differ slightly.

1. **Create the Actor from GitHub.** In [Apify Console](https://console.apify.com), go to Actors (or Development) → create a new Actor → link a Git repository → GitHub → `ayukari/apify-jp-law-search`. Apify reads `.actor/actor.json` and the Dockerfile and rebuilds on every push.
2. **Build and test.**
   - Run the build.
   - Then do a run with the default input (`lawTitle: 消費税法`, `articles: ["30"]`). The dataset should show 1 article record for 第三十条.
   - Tell Claude the result, including the run's compute units (CU) if shown, so the prices can be checked.
3. **Fill in the Publication tab.** Paste the display information from `STORE_LISTING.md`.
4. **Set up monetization.** Publication → Monetization:
   - Billing details and payout method (PayPal or Wise; the minimum payout is $20)
   - "Set up monetization" → pay-per-event → use the events and prices from `STORE_LISTING.md`
5. **Publish to Store.**
6. **Identity verification (KYC).** Upload an ID with your legal name before the first payout. Payout invoices are issued on the 11th of each month.
