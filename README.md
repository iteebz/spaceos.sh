# spaceos.sh

Demo site showcasing Space OS metrics.

## Dev

```bash
just dev
```

## Deploy

Cloudflare Pages auto-deploys on push to main.

**Manual deploy:**
```bash
just build
wrangler pages deploy dist --project-name=spaceos
```

**Setup:**
1. GitHub secrets: `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID`
2. Cloudflare Pages: Create project `spaceos`
3. DNS: Point `spaceos.sh` to Cloudflare Pages domain
