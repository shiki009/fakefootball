# fakefootball (vladFM) — Project Instructions

> Satirical football news platform. Vue 3 SPA frontend + FastAPI backend, deployed on Vercel with Neon Postgres.

## Tech Stack

### Backend (Python)
- **Framework**: FastAPI 0.115
- **ORM**: SQLAlchemy 2.0 (synchronous session, `DeclarativeBase`)
- **Database**: PostgreSQL via Neon (production) / SQLite (local dev)
- **AI Content**: Groq SDK (Llama 3.3 70B) for cron-generated posts + agent comments
- **Validation**: Pydantic v2 (`BaseModel`, `model_validate`, `from_attributes = True`)
- **Slugs**: python-slugify
- **Server**: Uvicorn
- **Python**: 3.11+

### Frontend (JavaScript)
- **Framework**: Vue 3.4 (Composition API, `<script setup>`)
- **Router**: Vue Router 4 (`createWebHistory`)
- **State**: Pinia 2.1 (Composition API stores via `defineStore`)
- **HTTP**: Axios (centralized in `src/api.js`)
- **Build**: Vite 5 (`@vitejs/plugin-vue`)
- **Styling**: Custom CSS with CSS variables (dark theme, no Tailwind)

### Deployment
- **Platform**: Vercel (serverless Python + static SPA)
- **Entry**: `api/index.py` re-exports `backend.main:app`
- **Frontend build**: `frontend/dist/` served as static files
- **Cron**: Vercel cron at `/api/cron/generate-posts` (daily 21:15 UTC)

## Directory Structure

```
fakefootball/
├── api/
│   └── index.py              # Vercel serverless entry point
├── backend/
│   ├── main.py               # FastAPI app, middleware, router includes
│   ├── db.py                 # Engine + session factory + get_db dependency
│   ├── models.py             # SQLAlchemy models (Post, Tag, Comment, Vote)
│   ├── schemas.py            # Pydantic response schemas
│   ├── seed.py               # Seed data (posts, tags, comments, votes)
│   ├── cron_generate.py      # AI content generation (Groq + RSS feeds)
│   ├── requirements.txt      # Python dependencies
│   └── routers/
│       ├── posts.py           # GET /api/posts, GET /api/posts/{slug}
│       ├── comments.py        # GET /api/posts/{post_id}/comments
│       ├── votes.py           # GET /api/posts/{post_id}/vote
│       ├── tags.py            # GET /api/tags
│       ├── stats.py           # GET /api/stats
│       ├── regulars.py        # GET /api/regulars, GET /api/regulars/{name}
│       ├── users.py           # GET /api/users/{username}
│       ├── cron.py            # GET /api/cron/generate-posts (secured)
│       └── og.py              # GET /api/og/{slug} (SVG open graph images)
├── frontend/
│   ├── package.json
│   ├── vite.config.js
│   ├── index.html
│   └── src/
│       ├── main.js            # App bootstrap (Pinia + Vue Router)
│       ├── app.vue            # Root layout (header, sidebar, router-view)
│       ├── router.js          # Route definitions
│       ├── api.js             # Axios HTTP client (all API calls)
│       ├── style.css          # Global styles + CSS variables
│       ├── components/        # Reusable UI components
│       │   ├── app-header.vue
│       │   ├── app-footer.vue
│       │   ├── post-card.vue
│       │   ├── vote-buttons.vue
│       │   ├── comment-list.vue
│       │   ├── sort-bar.vue
│       │   ├── pagination.vue
│       │   ├── tag-badge.vue
│       │   ├── tag-list.vue
│       │   ├── stats-widget.vue
│       │   ├── regulars-widget.vue
│       │   └── loading-spinner.vue
│       ├── views/             # Route-level page components
│       │   ├── home.vue
│       │   ├── post.vue
│       │   ├── tag.vue
│       │   ├── user.vue
│       │   ├── regulars.vue
│       │   ├── regular.vue
│       │   ├── about.vue
│       │   ├── sponsor.vue
│       │   └── not-found.vue
│       ├── stores/            # Pinia stores
│       │   ├── posts.js
│       │   ├── tags.js
│       │   └── stats.js
│       └── composables/       # Reusable composition functions
│           ├── timeago.js
│           └── authorlink.js
├── pyproject.toml
├── requirements.txt
├── vercel.json
└── .gitignore
```

## Naming Conventions

### Python (Backend)
- **Files**: `snake_case.py` (e.g., `cron_generate.py`)
- **Classes**: `PascalCase` for SQLAlchemy models (`Post`, `Tag`, `Comment`, `Vote`)
- **Pydantic schemas**: `snake_case` (e.g., `post_brief`, `tag_out`, `paginated_posts`)
- **Functions**: `snake_case` (e.g., `list_posts`, `get_post`, `_enrich`)
- **Variables**: `snake_case`
- **SQL tables**: `snake_case`, plural (`posts`, `tags`, `comments`, `votes`, `post_tags`)
- **SQL columns**: `snake_case`
- **Router prefixes**: `/api/{resource}` (e.g., `/api/posts`, `/api/tags`)

### JavaScript / Vue (Frontend)
- **Files**: `kebab-case.vue` / `kebab-case.js` (e.g., `post-card.vue`, `api.js`)
- **Components**: `kebab-case` in templates, imported as `camelCase` (e.g., `import postCard from './components/post-card.vue'`)
- **Functions**: `camelCase` (e.g., `fetchPosts`, `goToTag`, `useTimeAgo`)
- **Stores**: `use{Name}Store` (e.g., `usePostsStore`, `useTagsStore`)
- **CSS classes**: `kebab-case` (e.g., `.post-card`, `.truth-meter`, `.sort-bar`)

## Architecture Patterns

### Backend: Router Pattern

Every router follows this structure:

```python
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from models import Post, Vote, Comment
from schemas import post_brief, paginated_posts

router = APIRouter(prefix="/api/posts", tags=["posts"])

@router.get("", response_model=paginated_posts)
def list_posts(
    sort: str = Query("new", pattern="^(new|top|discussed|controversial)$"),
    page: int = Query(1, ge=1),
    per_page: int = Query(5, ge=1, le=50),
    db: Session = Depends(get_db),
):
    q = db.query(Post)
    total = q.count()
    # ... sorting, pagination, enrichment
    items = _enrich(db, posts)
    return paginated_posts(items=items, total=total, page=page, pages=pages)
```

**Key rules**:
- All routes use `Depends(get_db)` for database sessions
- Response models are Pydantic schemas
- Query parameters validated with `Query()`
- 404 errors raised with `HTTPException(404, "not found")`
- Related data enriched via batch queries (not N+1)

### Backend: Batch Enrichment Pattern

```python
def _enrich(db: Session, posts: list) -> list[post_brief]:
    if not posts:
        return []
    ids = [p.id for p in posts]
    scores = {
        row[0]: row[1]
        for row in db.query(Vote.post_id, func.coalesce(func.sum(Vote.value), 0))
        .filter(Vote.post_id.in_(ids))
        .group_by(Vote.post_id)
        .all()
    }
    # ... build result with enriched data
```

### Backend: Model Pattern

```python
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship, DeclarativeBase
from datetime import datetime, timezone

class Base(DeclarativeBase):
    pass

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    title = Column(String(300), nullable=False)
    slug = Column(String(300), unique=True, nullable=False, index=True)
    content = Column(Text, nullable=False)
    author_name = Column(String(100), nullable=False, default="anonymous")
    is_true_story = Column(Boolean, default=False)
    truth_score = Column(Integer, default=0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    tags = relationship("Tag", secondary=post_tags, back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
```

### Backend: Pydantic Schema Pattern

```python
from pydantic import BaseModel
from datetime import datetime

class tag_out(BaseModel):
    id: int
    name: str
    slug: str
    color: str

    class Config:
        from_attributes = True

class post_brief(BaseModel):
    id: int
    title: str
    slug: str
    author_name: str
    is_true_story: bool
    truth_score: int = 0
    created_at: datetime
    tags: list[tag_out]
    score: int = 0
    comment_count: int = 0

    class Config:
        from_attributes = True
```

### Frontend: Vue SFC Pattern (Composition API)

```vue
<script setup>
import { ref, onMounted, computed } from 'vue'
import { usePostsStore } from '../stores/posts.js'
import api from '../api.js'
import postCard from '../components/post-card.vue'

const postsStore = usePostsStore()

onMounted(() => {
  postsStore.fetchPosts()
})
</script>

<template>
  <div>
    <postCard v-for="p in postsStore.posts" :key="p.id" :post="p" />
  </div>
</template>

<style scoped>
.card { /* component-scoped styles */ }
</style>
```

### Frontend: Pinia Store Pattern

```javascript
import { ref } from 'vue'
import { defineStore } from 'pinia'
import api from '../api.js'

export const usePostsStore = defineStore('posts', () => {
  const posts = ref([])
  const loading = ref(false)

  async function fetchPosts() {
    loading.value = true
    try {
      const data = await api.getPosts()
      posts.value = data.items
    } finally {
      loading.value = false
    }
  }

  return { posts, loading, fetchPosts }
})
```

### Frontend: API Client Pattern

```javascript
import axios from 'axios'
const http = axios.create({ baseURL: '/api' })

export default {
  getPosts(sort = 'new', tag = null, page = 1) {
    const params = { sort, page }
    if (tag) params.tag = tag
    return http.get('/posts', { params }).then(r => r.data)
  },
  getPost(slug) {
    return http.get(`/posts/${slug}`).then(r => r.data)
  },
}
```

### Frontend: Composable Pattern

```javascript
export function useTimeAgo(dateStr) {
  const date = new Date(dateStr)
  const now = new Date()
  const seconds = Math.floor((now - date) / 1000)
  // ... interval logic
  return 'just now'
}
```

## Styling Approach

Custom CSS with CSS variables (dark theme). No CSS framework. All variables defined in `frontend/src/style.css`:

```css
:root {
  --bg: #0d1117;
  --bg-card: #161b22;
  --bg-hover: #1c2333;
  --border: #30363d;
  --text: #e6edf3;
  --text-muted: #8b949e;
  --green: #22c55e;
  --accent: #3fb950;
  --upvote: #f97316;
  --downvote: #6366f1;
  --font-mono: 'IBM Plex Mono', monospace;
  --font-body: 'Inter', sans-serif;
}
```

Component styles are scoped via `<style scoped>` in Vue SFCs.

## Database Schema

### Tables

| Table | Description | PK Type |
|-------|-------------|---------|
| `posts` | News articles with title, slug, content, truth_score | Integer |
| `tags` | Category tags (Transfer, Stats, Absurd, etc.) | Integer |
| `post_tags` | Many-to-many junction (post_id, tag_id) | Composite |
| `comments` | User comments on posts | Integer |
| `votes` | Upvotes/downvotes per post per fingerprint | Integer |

### Conventions
- Integer primary keys (auto-increment)
- `created_at` columns use `DateTime` with `datetime.now(timezone.utc)` default
- Relationships defined via SQLAlchemy `relationship()` with `back_populates`
- Cascade deletes: `cascade="all, delete-orphan"` on parent relationships
- Unique constraints: `UniqueConstraint("post_id", "fingerprint")` on votes
- Slugs: unique, indexed, generated via `python-slugify`

### No Auth / No Multi-tenancy
- This is a public, read-only site with no user authentication
- No `workspace_id` scoping, no RLS
- Votes use browser fingerprints, not user accounts
- Comments use `author_name` strings, not user FKs

## Build & Dev Commands

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
```

### Frontend
```bash
cd frontend
npm install
npm run dev          # Vite dev server on port 5174
npm run build        # Build to frontend/dist/
```

### Full Stack (local)
```bash
# Terminal 1: Backend
cd backend && uvicorn main:app --reload --port 8001

# Terminal 2: Frontend (proxies /api to backend via vite.config.js)
cd frontend && npm run dev
```

### Production (Vercel)
```bash
# Defined in vercel.json:
# Install: uv pip install --system -r requirements.txt && cd frontend && npm install
# Build:   cd frontend && npm install && npm run build
```

## Route Structure

### API Routes (Backend)
```
GET  /api/posts                          → paginated post list (sort, tag, page)
GET  /api/posts/{slug}                   → single post detail
GET  /api/posts/{post_id}/comments       → comments for a post
GET  /api/posts/{post_id}/vote           → vote score for a post
GET  /api/tags                           → all tags
GET  /api/stats                          → site-wide statistics
GET  /api/regulars                       → all regular commenters
GET  /api/regulars/{name}                → single regular's profile
GET  /api/users/{username}               → user profile (posts, comments, votes)
GET  /api/cron/generate-posts            → cron: generate AI content (secured)
GET  /api/og/{slug}                      → SVG open graph image
```

### Frontend Routes
```
/                          → home.vue (post feed with sort/filter)
/post/:slug                → post.vue (post detail + comments)
/tag/:slug                 → tag.vue (filtered by tag)
/user/:username            → user.vue (user profile)
/regulars                  → regulars.vue (all regulars)
/regulars/:name            → regular.vue (regular profile)
/about                     → about.vue
/sponsor                   → sponsor.vue
/:pathMatch(.*)*           → not-found.vue (404)
```

## Domains

posts, tags, comments, votes, regulars (community members), users, stats, cron (AI generation), og (open graph images)

## Key Utilities

- `get_db()` — SQLAlchemy session dependency (FastAPI `Depends`)
- `_enrich(db, posts)` — batch enrichment for vote scores + comment counts
- `api.js` — centralized Axios HTTP client for all API calls
- `useTimeAgo(dateStr)` — composable for relative time formatting
- `authorLink(name)` — composable mapping regular names to profile URLs
- `isRegular(name)` — checks if an author is a known regular

## Agent Pipelines

5 pipelines, 16 agent files. Full documentation in `.claude/agents/README.md`.

### Quick Reference

| Pipeline | Command | When | Stages |
|----------|---------|------|--------|
| **Feature** | `@ff-orchestrator` | New feature (3+ layers) | planner → architect → db → backend → frontend → tester → reviewer |
| **Bugfix** | `@ff-bug-orchestrator` | Bug, unknown root cause | triager → fixer → tester → reviewer |
| **Hotfix** | `@ff-hotfix-orchestrator` | Bug, known root cause | fixer → reviewer |
| **Refactor** | `@ff-refactor-orchestrator` | Restructure code | analyzer → executor → tester → reviewer |
| **Migration** | `@ff-migration-orchestrator` | DB-only changes | db-engineer → backend → tester → reviewer |

### Choosing the Right Pipeline

```
"I need a new feature"                    → @ff-orchestrator
"Something is broken, not sure why"       → @ff-bug-orchestrator
"Something is broken, I know the cause"   → @ff-hotfix-orchestrator
"I want to restructure this code"         → @ff-refactor-orchestrator
"I need to change the database schema"    → @ff-migration-orchestrator
"Single-file fix, trivial change"         → just do it directly
```

### Artifact Directories

Each pipeline writes to its own directory under `.planning/` (gitignored):

```
.planning/
├── features/{slug}/      ← feature pipeline
├── bugs/{slug}/          ← bugfix pipeline
├── hotfixes/{slug}/      ← hotfix pipeline
├── refactors/{slug}/     ← refactor pipeline
└── migrations/{slug}/    ← migration pipeline
```

### Running Individual Agents

Any agent can run standalone without a pipeline:

```
@ff-bug-triager Investigate why vote scores are wrong on the post list
@ff-reviewer Review backend/routers/posts.py against conventions
@ff-refactor-analyzer Map all dependencies of backend/schemas.py
@ff-db-engineer Create migration for a "bookmarks" table
```
