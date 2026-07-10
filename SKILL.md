---
name: x-list-monitor
description: Use when setting up an agent to monitor an X/Twitter List for news, research, market intelligence, community tracking, content discovery, or custom signal monitoring, with optional scheduled delivery.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [x, twitter, list-monitoring, social-monitoring, cron, news, research, content-intelligence]
    related_skills: []
---

# X List Monitor

## Overview

This skill helps an agent set up monitoring for an X/Twitter List.

The user may provide a list number, a list URL, or a natural-language request such as:

- "Monitor this X List for crypto news."
- "Track this list and send important updates to Telegram."
- "Watch this list for market-moving posts."
- "Use this list for content research."
- "I want a daily summary of important posts from this list."

The agent must not assume the user's goal. It should ask onboarding questions, understand the intended use case, estimate expected post volume, explain coverage limitations, recommend an appropriate schedule, and then set up either a one-time run or recurring monitoring if the runtime supports it.

This skill is runtime-agnostic. It can be used in Hermes, OpenClaw, or another capable agent environment. The agent should first inspect available capabilities instead of assuming specific tools exist.

## When to Use

Use this skill when the user wants to:

- Monitor an X/Twitter List.
- Turn X List posts into alerts, summaries, dashboards, or archives.
- Track industry media, projects, researchers, KOLs, companies, protocols, security accounts, market feeds, policy feeds, or any custom group of X accounts.
- Create scheduled monitoring with cron or a recurring task.
- Decide what to push, what to archive, and what to ignore.
- Build a reusable workflow from a list ID or list URL.

Do not use this skill for:

- Monitoring a single X account only, unless the account is part of a List workflow.
- Posting to X.
- Managing the user's X account.
- Scraping private or unauthorized content.
- Guaranteeing complete historical backfill without tool support for pagination or bounded retrieval.

## Runtime Capability Check

Before setting up monitoring, the agent should check what the current runtime can do.

### If running in Hermes

Prefer Hermes-native capabilities when available:

- X search / X intelligence tool, such as `x_search`.
- Scheduled jobs via `cronjob`.
- File persistence via local files, JSONL, Markdown, or HTML.
- Delivery via Telegram, Slack, Discord, email, or other configured gateway tools.
- Browser or web tools as fallback when X search is not available.

If creating a scheduled monitor in Hermes, use the `cronjob` tool only after the user confirms that they want recurring monitoring.

### If running in OpenClaw

The agent should inspect available tools and adapt:

- Is there an X search, browser, or API tool?
- Is there a scheduler, cron, recurring-task, or automation feature?
- Is there a messaging or notification tool?
- Is there file storage for state and archives?

If OpenClaw does not expose a scheduling tool, the agent should produce a reusable recurring-task prompt that the user can install manually in their OpenClaw environment.

### If runtime is unknown

The agent must do a capability check before promising automation.

Check whether the environment has:

- X/Twitter search or browser access.
- Ability to fetch from a List by list ID or URL.
- Local file write/read capability for state.
- Scheduler / cron / recurring task support.
- Messaging delivery support.
- Web dashboard or static file publishing support, if requested.

If a capability is missing, explain the limitation and offer a fallback.

## Required User Onboarding Questions

The agent must ask onboarding questions before setting up a recurring monitor.

Prefer asking in a concise form. The user can answer naturally; they do not need to fill a strict form.

### 1. List ID or URL

Ask:

> What X List do you want to monitor? Please provide either the list number or the full X List URL.

Accept:

- A numeric list ID, for example: `1234567890`
- A URL, for example: `https://x.com/i/lists/1234567890`

If the user provides a URL, extract the list ID from the URL.

Do not guess the list ID.

### 2. Intended Use

Ask:

> What is the purpose of monitoring this list? You can answer naturally, for example: breaking news, market intelligence, project updates, security incidents, regulatory news, content research, competitor tracking, community sentiment, or something else.

Use the answer to customize filtering, summary style, and delivery format.

Examples of possible purposes:

- Breaking news.
- Market-moving news.
- Crypto / Web3 industry updates.
- Security incidents, hacks, exploits, phishing, scams.
- Regulatory and policy updates.
- Project or ecosystem monitoring.
- Founder / VC / researcher monitoring.
- Content idea discovery.
- Daily or weekly executive summary.
- Community sentiment.
- Competitor tracking.
- Product or partnership tracking.
- Custom keyword monitoring.

### 3. Expected Post Volume

Ask:

> Roughly how many posts do you expect this list to produce? For example: fewer than 20 posts/day, 20-100/day, 100-300/day, 300+/day, or unknown.

This answer should influence the recommended cron frequency.

If the user does not know, offer to run a one-time test collection first and estimate the volume.

### 4. Delivery Mode

Ask:

> How do you want to receive the monitoring results?

Suggested options:

- Telegram push.
- Slack push.
- Discord push.
- Email summary.
- HTML dashboard.
- Markdown archive.
- JSONL archive.
- Only reply in this chat.
- Other custom delivery.

The agent should check available delivery tools before promising a platform.

### 5. Output Language

Default output language is English unless the user chooses otherwise.

Ask:

> What output language do you prefer? Default is English. You can choose English, Simplified Chinese, Traditional Chinese, bilingual, or follow the original post language.

Suggested options:

- English.
- Simplified Chinese.
- Traditional Chinese.
- English + Chinese bilingual.
- Follow original language.
- Custom.

### 6. Filtering Standard

Ask:

> What should be pushed versus only archived? You can describe the standard naturally.

Offer examples:

- Push all new posts.
- Push only important posts.
- Push only breaking news.
- Push only market-moving posts.
- Push only security / exploit / risk posts.
- Push only regulatory / policy posts.
- Push only data-worthy posts.
- Push only posts useful for content creation.
- Archive everything, but only push highlights.
- Custom keywords to include or exclude.

### 7. Replies, Retweets, and Quotes

Ask:

> Should replies, retweets, and quote tweets be included?

Suggested defaults:

- Replies: archive only by default, do not push unless the user wants them.
- Retweets: archive only by default, unless they amplify important information.
- Quote tweets: include when they add useful context or signal.
- Duplicates: merge or suppress repeated coverage by default.

The user may override these defaults.

### 8. Recurring Monitoring / Cron

Ask:

> Do you want to enable recurring monitoring with cron or scheduled runs?

Options:

- No, just run once.
- Yes, every 1 hour.
- Yes, every 2 hours.
- Yes, every 4 hours.
- Yes, every 8 hours.
- Yes, daily.
- Custom schedule / cron expression.

The agent must explain that longer intervals may increase the chance of missed coverage for high-volume lists.

## Completeness and Coverage Gaps

The agent must not promise 100% complete X List coverage unless the runtime/tooling supports complete pagination, reliable API access, and bounded backfill.

Use this explanation when discussing cron frequency:

> X List monitoring is usually best-effort. If the list is high-volume or the monitoring interval is too long, search/API results may be capped and some posts may be missed. To reduce this risk, use shorter cron intervals, save state such as `seen_post_ids` or `latest_post_id`, and run bounded backfill when there is a large gap.

Important factors:

- X search or API result limits.
- Pagination availability.
- Rate limits, auth limits, or spending limits.
- Number of accounts in the List.
- Post volume.
- Reply / retweet / quote volume.
- Time since the previous run.
- Whether state is persisted.
- Whether bounded backfill is used.

### Recommended Frequency by Volume

Use the user's expected post volume to recommend a schedule.

General guidance:

- Fewer than 20 posts/day:
  - Daily or every 8 hours is usually acceptable.
- 20-100 posts/day:
  - Every 4-8 hours.
- 100-300 posts/day:
  - Every 1-4 hours.
- 300+ posts/day:
  - Every 1 hour or shorter if supported.
  - Consider narrowing filters or splitting the list.
- Unknown volume:
  - Run a one-time test first.
  - Recommend every 4 hours as a starting point until volume is measured.

Explain trade-offs:

- More frequent runs reduce missed-post risk but consume more tool/API quota.
- Less frequent runs are cheaper and quieter but may miss high-volume activity.
- For important monitoring, start with a shorter interval and adjust after observing volume.

## List ID Handling

The agent should normalize the List input.

If the user gives:

```text
https://x.com/i/lists/1234567890
```

Extract:

```text
1234567890
```

If the user gives:

```text
1234567890
```

Use it directly.

If the input is ambiguous, ask the user to confirm.

Do not store the list ID in global memory. Store it only in the monitor's local state or scheduled job configuration.

## Collection Strategy

The agent should collect first, then filter.

Recommended record fields:

```json
{
  "post_id": "",
  "list_id": "",
  "author_handle": "",
  "author_name": "",
  "created_at": "",
  "text": "",
  "url": "",
  "type": "original | reply | retweet | quote | unknown",
  "quoted_post": null,
  "retweeted_post": null,
  "language": "",
  "matched_filters": [],
  "importance": "high | medium | low",
  "push_eligible": true,
  "summary": "",
  "collected_at": ""
}
```

Minimum fields:

- `post_id`
- `author_handle`
- `created_at`
- `text`
- `url`
- `type`
- `collected_at`

For recurring monitors, persist:

- JSONL archive of collected posts.
- State file with `seen_post_ids`.
- Latest known post ID or timestamp.
- Last successful run time.
- Last capture status.
- Delivery log if external push is used.

## Query Strategy

If the runtime has X search capability, use list-based queries where possible.

Examples:

```text
list:<LIST_ID>
list:<LIST_ID> since:YYYY-MM-DD until:YYYY-MM-DD
list:<LIST_ID> filter:links
list:<LIST_ID> filter:quote
list:<LIST_ID> filter:nativeretweets
```

Exact query syntax may vary by runtime and tool.

For high-volume lists:

- Query smaller time windows.
- Stop at known duplicate post IDs.
- Merge exact records by `post_id`.
- Use bounded follow-up queries when a page appears capped.
- Do not ingest citation-only or URL-only hints unless a full exact record is retrieved.

For unknown volume:

- Run a one-time test.
- Estimate volume.
- Recommend a cron interval.
- Ask the user to confirm before scheduling.

## Filtering Strategy

Filtering should be customized based on the user's stated purpose.

### General Importance Signals

High-priority signals may include:

- Breaking news.
- Market-moving events.
- Security incidents.
- Exploits, hacks, scams, phishing campaigns.
- Regulatory actions or policy changes.
- Funding, acquisition, listing, delisting.
- Major product launches.
- Mainnet, testnet, protocol upgrade, governance decision.
- Major partnership or integration.
- Strong data signal: volume, TVL, users, transactions, revenue, fees, market share, stablecoin supply, RWA size, flows, rankings.
- Repeated coverage by multiple credible sources.
- Posts that match user-defined keywords.

Low-priority signals may include:

- Generic engagement posts.
- Memes with no monitoring value.
- Duplicate media coverage with no new facts.
- Routine replies.
- Emoji-only or link-only posts.
- Pure promotional content unless the user wants it.
- Posts outside the stated purpose.

### Default Filtering Behavior

Unless the user says otherwise:

- Archive all collected exact records.
- Push only medium/high-value posts.
- Do not push ordinary replies.
- Do not push routine retweets.
- Include quote tweets when they add new context.
- Merge or suppress duplicate coverage.
- Keep a coverage summary so the user knows what was collected and what was filtered out.

## Delivery Formats

The agent should adapt output to the user's selected delivery channel and language.

### Concise Alert Format

```text
[Priority] <Category> — @author

Summary:
<short summary in selected language>

Why it matters:
<one sentence>

Original:
<post URL>
```

### News Digest Format

```text
X List Monitor Digest

List: <LIST_ID>
Window: <start> to <end>
Collected: <N> posts
Pushed highlights: <M>
Filtered/archive-only: <K>
Coverage: <success / partial / failed>

Top updates:
1. <summary + URL>
2. <summary + URL>
3. <summary + URL>

Notes:
<coverage gaps, rate limits, or duplicate handling>
```

### Content Research Format

```text
Potential content idea:
<topic>

Source post:
<URL>

Summary:
<what happened>

Why it may be useful:
<content angle>

Suggested hook:
<possible post/article hook>

Data to verify:
<metrics or external sources needed>
```

### Archive-Only Format

If the user only wants archive/state:

```text
Run complete.

Collected: <N> new posts
Archived: <N>
Pushed: 0
State updated: yes/no
Coverage: <success / partial / failed>
Archive path: <path if available>
```

## State and Archive Requirements

For recurring monitoring, the agent should maintain state. Do not rely only on memory.

Recommended files:

```text
x_list_<LIST_ID>/
  state.json
  archive.jsonl
  delivery_log.jsonl
  README.md
```

Recommended `state.json` fields:

```json
{
  "list_id": "",
  "purpose": "",
  "output_language": "English",
  "delivery_mode": "",
  "filtering_standard": "",
  "include_replies": false,
  "include_retweets": false,
  "include_quotes": true,
  "seen_post_ids": [],
  "latest_post_id": "",
  "latest_post_time": "",
  "last_successful_run_at": "",
  "last_capture_status": "",
  "last_new_count": 0,
  "last_pushed_count": 0,
  "last_archive_only_count": 0
}
```

Do not save list-specific state in long-term user memory. Use local files or the scheduler job configuration.

## Hermes Setup Recipe

When running in Hermes and the required tools are available:

1. Ask onboarding questions.
2. Normalize the List ID.
3. Run a one-time test capture.
4. Estimate post volume.
5. Recommend a schedule.
6. Ask whether to enable cron.
7. If the user confirms, create a `cronjob`.
8. Deliver to the chosen target if configured.
9. Persist state and archive files.

### Hermes Cron Prompt Template

Use a self-contained prompt when creating a recurring job.

```text
Monitor X List <LIST_ID> for <PURPOSE>.

User preferences:
- Output language: <LANGUAGE>
- Delivery mode: <DELIVERY_MODE>
- Filtering standard: <FILTERING_STANDARD>
- Include replies: <YES/NO>
- Include retweets: <YES/NO>
- Include quote tweets: <YES/NO>
- Duplicate handling: <MERGE/SEND_ALL>
- Expected volume: <EXPECTED_VOLUME>

Run requirements:
1. Load state from the monitor state file if available.
2. Query the X List for new posts since the previous run.
3. Collect exact records before filtering.
4. De-duplicate by post_id.
5. Archive all collected exact records.
6. Classify each new record by importance and category.
7. Push only records matching the user's filtering standard.
8. Report coverage status separately from post count.
9. If no push-worthy posts exist but archive was updated, provide a concise archive summary unless the user requested silent no-news runs.
10. Update state after successful archive write.
11. Do not claim complete coverage if the tool result was capped, rate-limited, or partial.
```

Recommended Hermes schedule examples:

```text
every 1h
every 2h
every 4h
0 */8 * * *
0 9 * * *
```

Choose based on expected volume and user preference.

## OpenClaw / Generic Agent Setup Recipe

When running in OpenClaw or another agent runtime:

1. Check available tools.
2. If X search is available, use list-based queries.
3. If browser access is available but no X API exists, explain that browser-based monitoring may be less reliable.
4. If scheduler support exists, ask the user whether to create a recurring task.
5. If scheduler support does not exist, output a reusable recurring-task prompt.
6. If external delivery tools are unavailable, output results in the current chat or write local files if possible.

### Generic Recurring Task Prompt

```text
Task: Monitor X List <LIST_ID>.

Purpose:
<PURPOSE>

Output language:
<LANGUAGE>

Delivery:
<DELIVERY_MODE>

Filtering rules:
<FILTERING_STANDARD>

Include/exclude:
- Replies: <YES/NO>
- Retweets: <YES/NO>
- Quote tweets: <YES/NO>
- Duplicates: <MERGE/SEND_ALL>

State:
Maintain seen_post_ids and latest_post_id if file storage is available.
Archive all exact records before filtering.
Do not rely on chat memory for deduplication.

Coverage:
This monitor is best-effort. If results are capped, rate-limited, or partial, report the coverage gap instead of saying there were no posts.

Each run:
1. Load previous state.
2. Fetch new posts from the X List.
3. De-duplicate by post_id.
4. Archive exact records.
5. Classify by category and importance.
6. Deliver only matching posts.
7. Update state.
8. Report collected count, pushed count, archive-only count, and coverage status.
```

## One-Time Test Run

If the user is unsure about expected volume or filtering standard, perform a one-time test first.

A good test run should report:

```text
Test run complete.

List: <LIST_ID>
Window checked: <time window>
Collected posts: <N>
Estimated daily volume: <estimate if possible>
Suggested cron interval: <recommendation>
Suggested filtering: <recommendation>
Potential coverage risk: <low / medium / high>
```

Then ask:

> Do you want to enable recurring monitoring with this schedule?

## Schedule Recommendation Logic

Use this logic after a test run or user-provided estimate:

```text
if expected_posts_per_day < 20:
    recommend daily or every 8 hours
elif expected_posts_per_day <= 100:
    recommend every 4-8 hours
elif expected_posts_per_day <= 300:
    recommend every 1-4 hours
else:
    recommend every 1 hour, splitting the list, or tightening filters
```

If the user wants high-confidence coverage, recommend a shorter interval.

If the user wants low noise and low cost, recommend a longer interval with stricter filtering and an explicit coverage caveat.

## Coverage Reporting

Every run should separate:

- Capture status.
- New exact records collected.
- Records archived.
- Records pushed.
- Records filtered out.
- Coverage gaps or tool errors.

Do not say "no new posts" if capture failed.

Use:

```text
Coverage: failed or partial due to <reason>.
```

instead of:

```text
No new posts.
```

when the tool failed or returned incomplete data.

## Common Pitfalls

1. **Assuming the List type.**  
   Always ask the user what the List is for.

2. **Not asking expected volume.**  
   Cron frequency depends heavily on post volume.

3. **Promising complete coverage.**  
   X List monitoring is often best-effort unless full pagination/backfill is available.

4. **Waiting too long between runs on high-volume lists.**  
   Long intervals can miss posts due to result caps.

5. **Filtering before archiving.**  
   Archive exact records first, then filter for delivery.

6. **Using memory for deduplication.**  
   Use state files or scheduler state, not long-term chat memory.

7. **Ignoring delivery capability.**  
   Check whether Telegram, Slack, Discord, email, or other delivery tools are actually configured.

8. **Creating cron without consent.**  
   Always ask the user whether they want recurring monitoring.

9. **Treating capture failure as zero activity.**  
   Failed capture means unknown activity, not no posts.

10. **Over-pushing low-value posts.**  
   For most users, archive everything but push only posts that match the stated purpose.

## Verification Checklist

Before finishing setup, confirm:

- [ ] List ID or URL was provided and normalized.
- [ ] User stated the monitoring purpose.
- [ ] User selected or confirmed output language.
- [ ] User selected delivery mode.
- [ ] Runtime delivery capability was checked.
- [ ] Filtering standard was confirmed.
- [ ] Reply / retweet / quote handling was confirmed.
- [ ] Expected post volume was asked or estimated by test run.
- [ ] Cron preference was confirmed.
- [ ] Recommended frequency included a coverage-gap caveat.
- [ ] State/archive strategy was defined.
- [ ] For recurring monitoring, the scheduled prompt is self-contained.
- [ ] The agent did not promise complete coverage unless full pagination/backfill is available.
