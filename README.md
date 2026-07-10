# x-list-monitor

A runtime-agnostic agent skill for monitoring X/Twitter Lists.

This skill helps an AI agent ask the right onboarding questions, understand the user's monitoring purpose, estimate expected post volume, recommend a cron frequency, set filtering rules, and optionally configure scheduled delivery.

It is designed to work with Hermes, OpenClaw, or other capable agent runtimes.

## What it does

- Accepts an X List ID or URL.
- Asks the user what the list is for instead of assuming the category.
- Asks expected post volume and uses it to recommend a monitoring interval.
- Explains that X List monitoring is usually best-effort and may miss posts if intervals are too long or search/API results are capped.
- Supports one-time runs or recurring cron/scheduled monitoring.
- Supports flexible delivery targets such as Telegram, Slack, Discord, email, dashboards, Markdown, JSONL, or current-chat replies.
- Encourages stateful deduplication with `seen_post_ids` / `latest_post_id`.
- Separates capture status, archived records, pushed records, filtered records, and coverage gaps.

## Installation

### Hermes Agent

Install directly from the raw `SKILL.md` URL:

```bash
hermes skills install https://raw.githubusercontent.com/joooe453-creator/x-list-monitor/main/SKILL.md
```

Then start a session and ask:

```text
Use the x-list-monitor skill. I want to monitor this X List: https://x.com/i/lists/<LIST_ID>
```

Or:

```text
Use x-list-monitor to track list <LIST_ID>. Ask me what settings you need before creating any cron job.
```

### OpenClaw / generic agent runtimes

Copy the contents of `SKILL.md` into your agent's skill, instruction, or workflow system.

The skill is intentionally not tied to Hermes-only tools. It tells the agent to detect runtime capabilities and adapt to whatever tools are available.


## Step 0: connect Grok / xAI first

Before giving the agent an X List ID, connect a Grok/xAI backend. This is the first step because X monitoring depends on an X-capable search/intelligence tool.

### Hermes with Grok Premium / SuperGrok

```bash
hermes auth add xai-oauth
hermes tools enable x_search
```

Then restart/start a fresh session and verify:

```bash
hermes status
hermes doctor
```

Optional: choose Grok as the main model:

```bash
hermes model
```

Select the xAI Grok OAuth / SuperGrok provider and a Grok model such as `grok-4.3` if available.

### Hermes with xAI API key

Set `XAI_API_KEY` in the Hermes env file:

```bash
hermes config env-path
```

Then enable the X search tool:

```bash
hermes tools enable x_search
```

### OpenClaw

Configure xAI/Grok in OpenClaw first if it supports direct provider setup. If OpenClaw only supports OpenAI-compatible custom endpoints, log into SuperGrok through Hermes and run:

```bash
hermes proxy start --provider xai-oauth --port 8645
```

Then configure OpenClaw with:

```text
Base URL: http://127.0.0.1:8645/v1
API key: local-proxy
Model: grok-4.3 or another model exposed by the proxy
```

Keep the proxy running while OpenClaw uses it.

## Recommended onboarding flow

The agent should ask the user:

1. How will the agent access Grok/xAI? Hermes SuperGrok OAuth, Hermes XAI_API_KEY, OpenClaw direct setup, or OpenClaw via Hermes proxy?
2. What X List ID or URL should be monitored?
3. What is the purpose of monitoring this list?
4. Roughly how many posts does the list produce per day?
5. How should results be delivered?
6. What output language should be used?
7. What should be pushed versus only archived?
8. Should replies, retweets, and quote tweets be included?
9. Should recurring cron/scheduled monitoring be enabled?

## Completeness caveat

X List monitoring should usually be treated as best-effort.

High-volume lists, long intervals, result caps, auth limits, rate limits, and missing pagination can cause coverage gaps. To reduce missed posts, use shorter intervals and maintain state such as `seen_post_ids` or `latest_post_id`.

General schedule guidance:

- Fewer than 20 posts/day: daily or every 8 hours.
- 20-100 posts/day: every 4-8 hours.
- 100-300 posts/day: every 1-4 hours.
- 300+ posts/day: every 1 hour or split/tighten the list.
- Unknown volume: run a one-time test first.

## License

MIT
