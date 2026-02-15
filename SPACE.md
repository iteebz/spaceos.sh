# spaceos.sh - Site Purpose

**What:** Internal research publication site from Space company

**Not:** Product site, demo, or public marketing

## Clarity

### spaceos.sh (this site)
- **Audience:** Investors, researchers, technical stakeholders
- **Purpose:** Research publications, methodology, technical deep dives
- **Content:** 
  - SPACE coordination primitive whitepaper
  - Human+AI collaboration findings
  - Multi-agent research (findings, methodology)
  - Thesis, philosophy, technical rationale
- **Vibe:** "Space Research Lab" - empirical, technical, evidence-based
- **Access:** Private - shown in investor meetings, shared selectively

### swarmbrr.com
- **Audience:** Customers, users, public
- **Purpose:** Product site for swarm coordination service
- **Content:**
  - Live swarm dashboard
  - Research findings (public-facing)
  - Methodology & replication guides
- **Vibe:** "Swarm product" - live metrics, production proof
- **Access:** Public - deployable to Cloudflare Pages

## Usage

**Investor meetings:** Show spaceos.sh
- Whitepaper at `/whitepaper` (stats-first, proof-based)
- Research findings at `/swarm/findings`
- Live metrics at `/swarm/live`

**Product demos:** Point to swarmbrr.com
- Same content, different framing
- Product-focused rather than research-focused

## Architecture

Both sites share:
- Astro static generation
- Same content (findings, methodology, metrics)
- Same live stats from Space-OS production

Different positioning:
- spaceos.sh = "Here's our research"
- swarmbrr.com = "Here's the product"

## Migration Status

- [x] swarmbrr.com created with swarm content
- [x] spaceos.sh repositioned as research site
- [ ] Consider: remove `/swarm/*` from spaceos.sh after swarmbrr.com is live
- [ ] Consider: add more research content to spaceos.sh (papers, case studies)
