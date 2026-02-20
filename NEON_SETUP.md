# Neon Postgres Setup (Persistent DB on Vercel)

The app uses **SQLite** locally and **Neon Postgres** in production when `DATABASE_URL` is set.

## What you need to do

### 1. Create a Neon database

1. Go to [console.neon.tech](https://console.neon.tech) and sign up (free tier available).
2. Create a new project (e.g. `fakefootball`).
3. Copy the **connection string** from the Connect dialog (branch, role, database). It looks like:
   ```
   postgresql://user:password@ep-xxx.region.aws.neon.tech/dbname?sslmode=require
   ```

### 2. Add `DATABASE_URL` to Vercel

1. Open your Vercel project → **Settings** → **Environment Variables**.
2. Add:
   - **Key:** `DATABASE_URL`
   - **Value:** paste your Neon connection string
   - **Environments:** Production (and Preview if you want)

### 3. Redeploy

Trigger a new deployment (push to Git or redeploy in Vercel). On startup the app will:
- Create tables in Postgres
- Run the seed (tags, posts, comments, votes)

---

## Alternative: Vercel Marketplace Integration

1. In Vercel: **Integrations** → **Add Integration** → search **Neon Postgres**.
2. Follow the wizard to connect Neon to your project. `DATABASE_URL` will be set automatically.
3. Redeploy.

---

## Cron: AI-generated posts (Groq)

A cron job runs **daily at 8:00 UTC** and generates 1–2 fake/real football news posts via Groq. Each post also gets ~5 comments from the regulars (maroco, Kolodin, shiki, etc.) acting as agents in character. Users can add their own comments and vote as usual.

### Required env vars

1. **GROQ_API_KEY** – Get a free key at [console.groq.com](https://console.groq.com)
2. **CRON_SECRET** – Random string to secure the cron endpoint (Vercel sends it as `Authorization: Bearer <secret>`)

Add both in Vercel → Settings → Environment Variables. Without `GROQ_API_KEY`, the cron does nothing. Without `CRON_SECRET` on Vercel, the endpoint returns 401.

### Manual trigger

You can call the endpoint manually (with the `Authorization: Bearer <CRON_SECRET>` header):

```
GET https://your-app.vercel.app/api/cron/generate-posts
```

---

## Local development

Without `DATABASE_URL`, the app uses SQLite (file: `backend/fakefootball.db`). No changes needed for local dev.
