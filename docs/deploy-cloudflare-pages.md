# Cloudflare Pages Deployment Runbook

## Context

**Decision:** d/957733d1, d/c5da339a  
**Target:** spaceos.sh → Cloudflare Pages (public demo)  
**Status:** Build ready, deploy blocked on human Cloudflare account access

## Prerequisites

- Cloudflare account with Pages enabled
- Domain `spaceos.sh` DNS configured to Cloudflare

## Deployment Steps

### 1. Connect Repository

```bash
# Cloudflare Dashboard → Pages → Create Project
# Select: GitHub → iteebz/spaceos.sh
```

### 2. Configure Build

| Setting | Value |
|---------|-------|
| Framework preset | None (pre-built) |
| Build command | `pnpm build` |
| Build output directory | `dist` |
| Root directory | `/` |
| Node version | 22 |

### 3. Environment Variables

None required (static site).

### 4. Deploy

```bash
# Cloudflare will auto-build on push to main
# Manual trigger: Cloudflare Dashboard → Pages → spaceos-sh → Deployments → Retry
```

### 5. Custom Domain

```bash
# Cloudflare Dashboard → Pages → spaceos-sh → Custom domains
# Add: spaceos.sh
# DNS will auto-configure if domain managed by Cloudflare
```

## Verification

1. Visit `https://spaceos.sh`
2. Verify stats populate from `stats.json` (static snapshot, updated pre-deploy)
3. Test links:
   - `/docs/thesis`
   - `/docs/philosophy`
   - `/docs/walkthrough`
   - `/swarm/papers`
   - `/swarm/findings`
   - `/swarm/live`

## Stats Update Flow

**Current:** Static `stats.json` snapshot  
**Future:** Live API (`api.spacebrr.com/stats`) after fly.io billing resolved

To update stats before deploy:

```bash
cd ~/space/repos/spaceos.sh
# Regenerate stats.json from space.db
space stats --json > dist/stats.json
git add dist/stats.json
git commit -m "chore(stats): refresh pre-deploy snapshot"
git push
```

## Rollback

Cloudflare Pages retains deployment history. Rollback via Dashboard → Deployments → previous version → Rollback.

## Alternative: CLI Deploy

If GUI fails:

```bash
# Install Wrangler
npm install -g wrangler

# Authenticate
wrangler login

# Deploy
cd ~/space/repos/spaceos.sh
pnpm build
wrangler pages deploy dist --project-name=spaceos-sh
```

## Post-Deploy

1. Update d/c5da339a → ACTIONED
2. Verify Product Hunt demo link
3. Monitor Cloudflare Analytics for traffic
