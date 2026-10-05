# apify-jp-law-search

Apify Actor (work in progress) that searches Japanese laws and fetches articles from the official e-Gov 法令API v2 (`laws.e-gov.go.jp/api/2`).

`tests/fixtures/` holds real API responses captured on 2026-10-05: a law search for 消費税法 and 消費税法 第30条. Tests run against these fixtures.

## Input

| Field | Example | Notes |
|---|---|---|
| `lawTitle` | `消費税法` | Part of a law title. Either this or `lawIds` is required. |
| `lawIds` | `["363AC0000000108"]` | Exact e-Gov law IDs |
| `articles` | `["30", "第57条の4"]` | Optional. `30`, `第30条` and `57_4` are all accepted. |
| `maxLaws` | `5` | 1–100 |

## Output (dataset)

- `type: "law"`: `lawId`, `lawNum`, `lawTitle`, `lawTitleKana`, `category`, `promulgationDate`, `enforcementDate`, `revisionId`, `url`
- `type: "article"`: the law fields plus `articleNum`, `articleTitle`, `articleCaption`, `paragraphs[{num, text, items}]`, and `text` (the full article as plain text)

## Development

```bash
python3 -m unittest discover -s tests   # fixture-based tests, no network
```

Local run (verified 2026-10-05): input `{"lawTitle":"消費税法","articles":["30","第57条の4"],"maxLaws":1}` returns 第三十条 (13 paragraphs) and 第五十七条の四 (7 paragraphs).
