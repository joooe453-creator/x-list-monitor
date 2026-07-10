---
name: x-list-monitor
description: Use when setting up an agent to monitor an X/Twitter List, optionally alongside LinkedIn/company-page sources, for news, research, market intelligence, community tracking, or custom signal monitoring with optional scheduled delivery.
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

This skill helps an agent set up monitoring for an X/Twitter List. It can optionally include LinkedIn sources, but LinkedIn support is always best-effort and capability-dependent.

The user may provide a list number, a list URL, or a natural-language request such as:

- "Monitor this X List for crypto news."
- "Track this list and send important updates to Telegram."
- "Watch this list for market-moving posts."
- "Use this list for content research."
- "I want a daily summary of important posts from this list."

The agent must not assume the user's goal. It should ask onboarding questions, understand the intended use case, estimate expected post volume, explain coverage limitations, recommend an appropriate schedule, and then set up either a one-time run or recurring monitoring if the runtime supports it.

This skill is runtime-agnostic. It can be used in Hermes, OpenClaw, or another capable agent environment. The agent should first inspect available capabilities instead of assuming specific tools exist.


## Step 0 — Connect Grok / xAI Before Monitoring

Before asking for X List IDs, delivery rules, schedules, or LinkedIn sources, the agent should help the user confirm that their runtime can access X data through Grok/xAI.

This is the first setup step because the X monitoring workflow depends on an X-capable search/intelligence backend. If Grok/xAI is not connected, the agent must not promise reliable X List monitoring. Instead, it should guide the user through one of the supported connection paths below.

### Hermes: SuperGrok / Grok Premium OAuth

Use this when the user has a Grok Premium / SuperGrok subscription and wants to connect the account directly without creating a separate paid API key.

Recommended command:

```bash
hermes auth add xai-oauth
```

Then select Grok as the model/provider if desired:

```bash
hermes model
```

Choose the xAI Grok OAuth / SuperGrok provider and a Grok model such as `grok-4.3` if available.

Enable the X search toolset:

```bash
hermes tools enable x_search
```

Restart or start a fresh session after enabling tools:

```text
/reset
```

Verify:

```bash
hermes status
hermes doctor
```

In chat, the agent can also verify by attempting a small `x_search` query if the tool is available.

Notes:

- `x_search` registers when either SuperGrok OAuth is logged in or `XAI_API_KEY` is available.
- OAuth tokens are stored locally by Hermes; users should not paste Grok credentials into chat.
- If OAuth expires or fails, ask the user to run `hermes auth add xai-oauth` again or reauthenticate through `hermes model`.

### Hermes: xAI API Key

Use this when the user has a paid xAI API key instead of, or in addition to, a Grok subscription login.

Set:

```bash
XAI_API_KEY=<your_xai_api_key>
```

The key should live in the Hermes env file, not in the skill, dashboard, cron prompt, or chat transcript. To find the env file:

```bash
hermes config env-path
```

Then enable X search:

```bash
hermes tools enable x_search
```

Restart or start a fresh session.

### OpenClaw: direct Grok/xAI connection

If OpenClaw has a provider/model settings UI, configure xAI/Grok there first. Prefer one of these options, depending on what OpenClaw supports:

1. xAI API key with a Grok model.
2. Built-in SuperGrok/Grok OAuth, if OpenClaw supports it.
3. OpenAI-compatible endpoint pointed at a local Hermes proxy, if OpenClaw supports custom OpenAI-compatible providers.

### OpenClaw via Hermes Proxy

If OpenClaw cannot log into SuperGrok directly but can use an OpenAI-compatible endpoint, use Hermes as a local proxy after logging into SuperGrok in Hermes.

First authenticate Hermes:

```bash
hermes auth add xai-oauth
```

Then run the proxy:

```bash
hermes proxy start --provider xai-oauth --port 8645
```

Configure OpenClaw custom OpenAI-compatible provider:

```text
Base URL: http://127.0.0.1:8645/v1
API key: any non-empty placeholder, for example local-proxy
Model: a Grok model exposed by the proxy, for example grok-4.3 if available
```

Keep the proxy running while OpenClaw uses it. Do not expose the proxy to the public internet.

### What the agent should ask first

Start onboarding with:

> First, how will this agent access Grok/xAI for X monitoring? Options: Hermes SuperGrok OAuth, Hermes XAI_API_KEY, OpenClaw direct xAI/Grok setup, or OpenClaw through a Hermes local proxy.

Only after this is answered and verified should the agent ask for List IDs, LinkedIn sources, push rules, filters, or cron schedule.

## When to Use

Use this skill when the user wants to:

- Monitor an X/Twitter List.
- Optionally monitor LinkedIn company pages, authorized organization posts, user-supplied LinkedIn URLs, or third-party LinkedIn feeds as best-effort supplemental sources.
- Turn X List posts and optional LinkedIn items into alerts, summaries, dashboards, or archives.
- Track industry media, projects, researchers, KOLs, companies, protocols, security accounts, market feeds, policy feeds, or any custom group of X accounts.
- Create scheduled monitoring with cron or a recurring task.
- Decide what to push, what to archive, and what to ignore.
- Build a reusable workflow from a list ID or list URL.

Do not use this skill for:

- Monitoring a single X account only, unless the account is part of a List workflow.
- Posting to X.
- Managing the user's X account.
- Scraping private or unauthorized content.
- Bypassing login, CAPTCHA, 2FA, paywalls, rate limits, or platform access controls.
- Echoing, committing, logging, or rendering raw LinkedIn cookies after intake. Simple cookie paste may be used for low-risk dedicated accounts when the user accepts the tradeoff.
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
- If LinkedIn is requested: official LinkedIn API access, browser-session access, third-party connector access, RSS/change-detection feed access, or no LinkedIn capability.
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

### 5. Optional LinkedIn Sources

Ask this only if the user mentions LinkedIn, company pages, professional profiles, or mixed social monitoring:

> Do you want to include LinkedIn sources? If yes, please provide company/profile/post URLs or the connector you want to use. LinkedIn monitoring is best-effort and may require official API access, a local logged-in browser session, or a third-party service.

Clarify the source type:

- LinkedIn Company Page controlled by the user or their organization.
- LinkedIn Company Page not controlled by the user.
- LinkedIn personal profile.
- Specific LinkedIn post URLs.
- User-supplied RSS/change-detection feed.
- Third-party connector such as Apify, Bright Data, PhantomBuster, Visualping, or another provider.

Never ask the user to paste raw cookies, passwords, or tokens into chat. If browser-session monitoring is needed, instruct the user to log in interactively in a local browser/profile and keep all session state local.

For no-cost LinkedIn monitoring, ask:

> Do you want to use free local browser-session mode for LinkedIn? If yes, use a dedicated account/browser profile that you own, log in manually, and accept that LinkedIn coverage is best-effort and may fail when sessions expire or challenges appear.

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
  "platform": "x",
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

## LinkedIn Monitoring Strategy

LinkedIn support is optional and must be described as best-effort. The agent must not promise complete monitoring of arbitrary public LinkedIn profiles, company pages, comments, reactions, or posts.

### Preferred Order of Methods

1. **Free local browser-session mode**
   - This is the default no-cost LinkedIn option when the user explicitly wants LinkedIn monitoring and accepts best-effort coverage.
   - The user may use a dedicated LinkedIn account they own and can manually log into locally. Do not ask for passwords or raw cookies in chat.
   - The agent should open or reuse a local browser profile/auth state, let the user complete login manually, then read only content visible to that logged-in browser session.
   - If LinkedIn shows login, 2FA, CAPTCHA, checkpoint, security verification, or account restriction pages, stop and ask the user to complete it manually. Do not bypass challenges.
   - Use conservative polling by default: daily or every 8-12 hours for low volume; every 4-6 hours only if the user accepts higher account/challenge risk. Avoid high-frequency scraping.
   - Store only normalized post records and source URLs. Do not store raw HTML pages unless the user explicitly asks and understands the privacy/compliance risk.

2. **Official LinkedIn API, when available**
   - Use OAuth and approved scopes.
   - Organization posts can be polled with LinkedIn Posts API only when the authenticated user has the required organization role and approved permissions such as `r_organization_social`.
   - Organization social-action webhooks can be used for company pages the authenticated user administers, but require permissions such as `rw_organization_admin` and only cover supported event types.
   - Arbitrary public profile/page monitoring is not generally supported by official APIs.

3. **User-supplied third-party connector**
   - Use only if the user already has or wants a provider account. This is not the default for no-cost setup.
   - Accept only user-owned API keys/tokens via environment variables or runtime secret stores.
   - Suitable options may include Apify Actors, Bright Data, PhantomBuster, Visualping, or user-provided RSS/change-detection feeds.
   - Treat connector output as best-effort and connector-specific. Record provider, query/input, fetched time, item count, and limitations.
   - Do not hardcode or print tokens. Redact all secrets as `[REDACTED]`.

4. **Generic webpage/RSS/change detection**
   - If the user supplies a feed URL or change-detection service output, poll that feed as a generic source.
   - This is useful for lightweight notifications but should not be treated as structured or complete LinkedIn monitoring.

### LinkedIn Cookie and Session Safety

Do not teach users to copy raw LinkedIn cookies out of DevTools or browser extensions. Raw cookie export is equivalent to exporting a login session and creates unnecessary leakage risk. The supported free setup is interactive login into a dedicated local browser profile that the agent reuses locally.

LinkedIn cookies and browser auth state are secrets. Treat all cookies for `linkedin.com` and `.linkedin.com` as sensitive, especially:

```text
li_at
li_a
JSESSIONID
PLAY_SESSION
li_rm
bscookie
bcookie
liap
lidc
li_gc
lang
UserMatchHistory
AnalyticsSyncHistory
aam_uuid
```

Rules:

- Prefer a dedicated local browser profile for LinkedIn monitoring, for example `.auth/linkedin-browser/` or an equivalent runtime-specific profile directory.
- Never ask the user to paste cookies into chat.
- Never commit browser profiles, `storageState` JSON, `.auth/` directories, screenshots of account/security pages, or cookie dumps.
- Add auth-state directories to `.gitignore` if files are created.
- Never log `Cookie:` or `Set-Cookie:` headers.
- Redact cookie names and values as `[REDACTED]` in all reports.
- Provide a way to delete local auth state if the runtime created it.
- Do not send cookies or browser storage to LLM prompts, dashboards, GitHub, Netlify, or third-party services.
- If the user wants to use a small/dedicated account, describe the risk plainly: sessions can expire, automation can trigger challenges, and the account can be restricted. Do not guarantee reliability or account safety.

### Free Local Session Setup Instructions

When a user wants the free LinkedIn mode, guide them through a local-session setup instead of cookie extraction:

1. Create or choose a dedicated LinkedIn account owned by the user.
2. Create a dedicated local browser profile for monitoring, separate from the user's main browser profile.
3. Open LinkedIn in that profile and let the user log in manually.
4. If LinkedIn asks for 2FA, CAPTCHA, checkpoint, or security verification, the user completes it manually in the browser.
5. Store the browser profile/auth state only on the local machine in an ignored path such as `.auth/linkedin-browser/`.
6. Add `.auth/`, `storageState.json`, and any browser-profile directories to `.gitignore`.
7. The agent may reuse that local profile for future checks but must not print, export, or transmit cookies.
8. If the session expires, ask the user to open the same browser profile and log in again.

Acceptable wording:

> I won't ask you to paste cookies. Please log into LinkedIn manually in this dedicated local browser profile. I will reuse the local session if the runtime supports it. If LinkedIn challenges the session, I will pause and ask you to resolve it manually.

For simple cookie mode, it is acceptable to tell the user to provide the LinkedIn session cookie for their dedicated account, but keep extraction guidance brief and safety-focused: use a dedicated account, copy only that account's LinkedIn session cookie, paste it once, and expect to replace it when expired. Do not teach bypassing checkpoints, CAPTCHA, 2FA, rate limits, or other access controls. If a runtime can generate browser auth state instead, that is also acceptable and must still be treated as a local secret: ignored by git, never printed, never committed, and never sent to a model or dashboard.

### Advanced Local Cookie Secret Mode

Use this mode only when the user explicitly wants a free cookie-based LinkedIn monitor and accepts the account/session risk.

For non-technical users with a dedicated low-risk account, simple chat-based cookie handoff is acceptable if the user chooses convenience over strict secrecy. The agent must still not echo the cookie, must immediately save it to local secret storage or an ignored local secret file, and must never include it in summaries, dashboards, logs, commits, cron prompts, or model prompts.

Use two modes:

- **Simple cookie mode (default for non-technical teammates):** the user pastes the LinkedIn session cookie into the agent once; the agent stores it locally, validates it, and asks for a fresh cookie when it expires.
- **Safer hidden-input mode:** if the runtime supports hidden prompts or OS secret-store prompts, prefer that path, but do not block setup if the user only knows how to paste the cookie into chat for a dedicated small account.

Recommended storage design:

1. Store the LinkedIn session material in the operating system secret store when available:
   - macOS: Keychain.
   - Linux: Secret Service / `pass` / encrypted credential store.
   - Windows: Credential Manager.
2. If no OS secret store is available, store an encrypted local file outside the repo, with restrictive permissions such as owner-read/write only. Never store it in the skill repo, dashboard repo, workspace archive, or shared folder.
3. Store only the minimum session material needed by the selected runtime. Prefer runtime browser auth state over a raw `Cookie:` header. If a cookie secret is unavoidable, store it as a local secret value referenced by name, not as plaintext in prompts or config.
4. Keep a local metadata file with non-secret fields only:
   - `method`: `browser_profile | os_keychain | encrypted_file`
   - `source_count`
   - `last_validated_at`
   - `last_refresh_required_at`
   - `status`: `valid | expired | challenged | unknown`
   - never include cookie values.
5. Add all local auth paths to `.gitignore`, for example `.auth/`, `storageState.json`, `linkedin-cookie.enc`, and browser profile directories.

Agent-managed cookie intake flow for less technical users:

1. Ask the user to use a dedicated LinkedIn account, not their main account.
2. Ask the user to paste the LinkedIn session cookie or full `Cookie:` header once.
3. When the cookie appears, do not echo it back. Do not quote it in the response. Do not include it in tool output summaries.
4. Save it immediately to the local secret store or ignored local secret file. On macOS, the included helper `scripts/store_linkedin_cookie_macos.py` can store the value in Keychain with hidden input; if the user already pasted the cookie in chat, the agent may store that value locally without printing it.
5. Validate the stored session by checking LinkedIn login status with a lightweight request/browser check.
6. If validation succeeds, reply only with non-secret status such as: `LinkedIn session saved locally. Validation: success.`
7. If validation fails, reply only with non-secret status and ask for a fresh cookie from the same dedicated account.
8. Record only non-secret metadata: method, source count, last validated time, and status.

If the runtime supports a hidden prompt or OS secret-store UI, prefer it. But for dedicated small-account workflows, normal chat handoff is allowed for simplicity, as long as the agent never repeats, logs, commits, renders, or forwards the cookie.

Runtime behavior:

1. Load the cookie/session only inside the local process.
2. Immediately redact it from logs and tool outputs. Never echo it.
3. Validate login with a lightweight LinkedIn page check before collection.
4. If the session is valid, collect only the configured public/company/profile/post pages visible to that account.
5. If the session appears expired, challenged, rate-limited, or redirected to login, do not keep retrying aggressively.
6. Mark LinkedIn coverage as partial/failed, continue X monitoring if configured, and ask the user to refresh the LinkedIn session manually.

Fallback / renewal flow:

- Do not "find" or obtain cookies from third parties, leaked sources, shared accounts, or other users.
- The only supported replacement cookie/session is a new session generated by the same user's dedicated LinkedIn account through manual local login.
- If cookie mode fails, open or instruct the user to open the dedicated local LinkedIn browser profile, log in again, complete any verification manually, then update the local secret store or browser auth state.
- After refresh, run a small validation check before resuming scheduled monitoring.
- If repeated challenges occur, reduce LinkedIn polling frequency or disable LinkedIn sources while keeping X monitoring active.

Suggested user-facing wording:

> Your LinkedIn cookie/session looks expired or challenged. I did not print or transmit it. Please open the dedicated LinkedIn monitoring browser profile, log in manually with the account you own, complete any verification, then tell me to retry. I will validate the renewed local session and continue. X monitoring can continue independently.

### LinkedIn Record Fields

Normalize LinkedIn items into the same archive pipeline as X posts, but keep platform-specific fields:

```json
{
  "platform": "linkedin",
  "source_type": "company_page | profile | post_url | connector | rss | browser",
  "source_url": "",
  "author_name": "",
  "author_url": "",
  "created_at": "",
  "text": "",
  "url": "",
  "provider": "official_api | apify | brightdata | phantombuster | visualping | rss | browser | other",
  "provider_item_id": "",
  "importance": "high | medium | low",
  "push_eligible": true,
  "summary": "",
  "collected_at": "",
  "coverage_note": "best-effort; method-specific limitations"
}
```

### LinkedIn Coverage Caveat

Use wording like:

> LinkedIn monitoring is best-effort. Official APIs are permission-limited, public pages may be incomplete or login-gated, browser sessions can expire or trigger challenges, and third-party connectors vary by provider. I will report LinkedIn capture status separately from X capture status and will not treat failed LinkedIn access as "no new posts."

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

The agent should adapt output to the user's selected delivery channel. Default dashboard/digest language is English unless the user explicitly requests otherwise.

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
  "sources": {
    "x_list_id": "",
    "linkedin_sources": []
  },
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
Monitor X List <LIST_ID> for <PURPOSE>. Include optional LinkedIn sources only if configured by the user.

User preferences:
- Output language: English unless explicitly overridden
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
3. If LinkedIn sources are configured, collect them through the selected method and report LinkedIn coverage separately.
4. Collect exact records before filtering.
5. De-duplicate X records by post_id and LinkedIn records by provider_item_id or URL.
6. Archive all collected exact records.
7. Classify each new record by importance and category.
8. Push only records matching the user's filtering standard.
9. Report X and LinkedIn coverage status separately from post count.
10. If no push-worthy posts exist but archive was updated, provide a concise archive summary unless the user requested silent no-news runs.
11. Update state after successful archive write.
12. Do not claim complete coverage if the tool result was capped, rate-limited, challenge-gated, or partial.
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
English unless explicitly overridden.

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
3. If configured, fetch LinkedIn sources through the selected best-effort method and report separate coverage.
4. De-duplicate by post_id for X and provider_item_id/URL for LinkedIn.
5. Archive exact records.
6. Classify by category and importance.
7. Deliver only matching posts.
8. Update state.
9. Report collected count, pushed count, archive-only count, and separate X/LinkedIn coverage status.
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

11. **Treating LinkedIn like X.**  
   LinkedIn has different access controls, API permissions, login walls, session challenges, and third-party connector limitations. Always label LinkedIn as best-effort and report its coverage separately.

12. **Leaking LinkedIn cookies or auth state.**  
   Cookies such as `li_at`, `JSESSIONID`, `bscookie`, and browser storage can impersonate the user. Never print, store in the repo, or send them to dashboards/LLMs.

## Verification Checklist

Before finishing setup, confirm:

- [ ] List ID or URL was provided and normalized.
- [ ] User stated the monitoring purpose.
- [ ] Output defaults to English unless the user explicitly requested otherwise.
- [ ] User selected delivery mode.
- [ ] Runtime delivery capability was checked.
- [ ] Filtering standard was confirmed.
- [ ] Reply / retweet / quote handling was confirmed.
- [ ] Expected post volume was asked or estimated by test run.
- [ ] Cron preference was confirmed.
- [ ] Recommended frequency included a coverage-gap caveat.
- [ ] State/archive strategy was defined.
- [ ] If LinkedIn sources were configured, the method, permissions, coverage caveat, and secret/cookie redaction policy were confirmed.
- [ ] For recurring monitoring, the scheduled prompt is self-contained.
- [ ] The agent did not promise complete coverage unless full pagination/backfill is available.
