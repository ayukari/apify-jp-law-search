# Apify Store listing (draft)

Copy-paste material for the Apify Console → Actor → Publication tab. Owner reviews before publishing.

## Display information

- **Title:** Japanese Law Search (e-Gov 法令API)
- **Short description (EN):** Search Japanese laws by title and get clean article text from the official e-Gov 法令API v2. No API key needed.
- **Short description (JA):** 日本の法令を名前で検索し、条文を整形済みテキスト（項・号つき）で取得します。e-Gov 法令API v2 の公式データを使用。APIキー不要。
- **Categories:** Developer tools, AI, Other (pick what the Console offers)
- **Icon:** a simple 「法」 or a book icon (owner's choice)

## README for the Store page

### What it does
Searches Japan's official law database (e-Gov 法令API v2, operated by the Digital Agency) and returns structured JSON:

- **Law metadata:** law ID, law number (法令番号), title, kana, category, promulgation date, latest enforcement date, and the e-Gov URL
- **Article text:** article number, title, caption (見出し), paragraphs (項) with items (号/イロハ), and the full article as plain text

### Typical uses
- Feed exact statutory text into **LLM / RAG pipelines**, instead of relying on the model's memory of Japanese law
- **Compliance checks:** pull the current wording of 消費税法, インボイス rules (第57条の4), 労働基準法, etc.
- **Monitoring:** run on a schedule and compare `enforcementDate` / `revisionId` to detect amendments

### Input
| Field | Example | Notes |
|---|---|---|
| `lawTitle` | 消費税法 | Part of the title. Use this or `lawIds`. |
| `lawIds` | ["363AC0000000108"] | Exact law IDs |
| `articles` | ["30", "第57条の4"] | Optional. Leave empty for metadata only. |
| `maxLaws` | 5 | 1–100 |

### Output example (article)
```json
{
  "type": "article",
  "lawTitle": "消費税法",
  "lawNum": "昭和六十三年法律第百八号",
  "articleTitle": "第五十七条の四",
  "articleCaption": "（適格請求書発行事業者の義務）",
  "paragraphs": [{"num": 1, "text": "…", "items": ["　一　…"]}],
  "text": "第五十七条の四（適格請求書発行事業者の義務）\n…",
  "url": "https://laws.e-gov.go.jp/law/363AC0000000108"
}
```

### Notes
- The data comes from the official e-Gov 法令API. This Actor does not modify the legal text. It only restructures it.
- This is **not legal advice**. Always check the official source for legal decisions.
- Requests are rate-limited politely (≥0.5 s between calls) to respect the public API.

## Pricing proposal (pay-per-event)

The Actor already emits two events (`law-result`, `article-result`) through `Actor.push_data(..., charged_event_name=...)`.

| Event | Proposed price | Rationale |
|---|---|---|
| `article-result` | $0.005 per article ($5 / 1,000) | Main value: cleaned statutory text |
| `law-result` | $0.001 per law ($1 / 1,000) | Metadata only; cheap enough for monitoring use |

- The creator receives 80% of revenue **minus platform usage costs** (Apify Store Publishing Terms §10.2.1, verified in R2). This Actor is light (HTTP plus JSON only), so platform costs per run should be small. Check the first real runs' compute usage in the Console before finalizing prices.
- These prices are a **starting proposal**, not market-tested. Adjust after the first week of usage data.
