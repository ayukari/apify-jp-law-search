"""Apify Actor entry point: search Japanese laws and fetch articles via e-Gov API v2."""
import asyncio

from apify import Actor

from .egov import EgovClient, normalize_article, summarize_law


def plan(inp):
    """Validate input and return (title, law_ids, articles, max_laws). Raises ValueError on bad input."""
    title = (inp.get("lawTitle") or "").strip()
    law_ids = [x.strip() for x in inp.get("lawIds") or [] if x.strip()]
    articles = [str(a).strip().replace("条の", "_").replace("第", "").replace("条", "") for a in inp.get("articles") or [] if str(a).strip()]
    max_laws = int(inp.get("maxLaws") or 5)
    if not title and not law_ids:
        raise ValueError("Give lawTitle or lawIds.")
    return title, law_ids, articles, max(1, min(max_laws, 100))


async def main():
    async with Actor:
        inp = await Actor.get_input() or {}
        try:
            title, law_ids, articles, max_laws = plan(inp)
        except ValueError as e:
            await Actor.fail(status_message=str(e))
            return
        client = EgovClient()
        laws = []
        if law_ids:
            for law_id in law_ids:
                res = await asyncio.to_thread(client.search_laws, law_id=law_id, limit=1)
                laws += [summarize_law(x) for x in res.get("laws", [])]
        else:
            res = await asyncio.to_thread(client.search_laws, title=title, limit=max_laws)
            laws = [summarize_law(x) for x in res.get("laws", [])]
        Actor.log.info(f"Matched {len(laws)} law(s)")

        if not articles:
            for law in laws:
                await Actor.push_data({"type": "law", **law}, charged_event_name="law-result")
            return

        for law in laws:
            for art in articles:
                try:
                    data = await asyncio.to_thread(client.get_article, law["lawId"], art)
                except Exception as e:  # missing article for this law, network error, etc.
                    Actor.log.warning(f"{law['lawTitle']} 第{art}条: {e}")
                    continue
                rec = normalize_article(data)
                if rec:
                    await Actor.push_data({"type": "article", **rec}, charged_event_name="article-result")
