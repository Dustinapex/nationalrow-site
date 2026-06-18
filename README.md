# National ROW — Website

Marketing and lead-capture site for National ROW (National Right-of-Way), an eminent-domain
and condemnation consulting firm representing property owners nationwide.

Single-page static site. No build step, no framework — just static files served as-is.

## Files
| File | Purpose |
|------|---------|
| `index.html` | The entire website (HTML, CSS, and JS in one file; logo embedded inline) |
| `national-row-logo.png` | Logo (used for social/share cards and structured data) |
| `og-image.png` | 1200×630 social share image |
| `favicon.ico`, `favicon.png`, `apple-touch-icon.png` | Browser/device icons |
| `robots.txt` | Crawler rules + sitemap reference |
| `sitemap.xml` | Sitemap for search engines |
| `llms.txt` | Plain-text site summary for AI/search discovery |

## Deploy (Vercel + GitHub)
1. Push these files to the repo root on GitHub.
2. In Vercel: **Add New → Project → Import** this repo. Framework Preset: **Other**. Deploy.
3. Every push to GitHub auto-deploys to the same URL.

## Custom domain (Cloudflare DNS)
- Add `nationalrow.com` and `www.nationalrow.com` in **Vercel → Settings → Domains**.
- In Cloudflare DNS, add the A record (apex) and CNAME (www) Vercel provides.
- Set both records to **DNS only (grey cloud)**, not proxied.

## Lead form
The Case review form posts to FormSubmit and emails submissions to **info@nationalrow.com**.
The first submission on the live site triggers a one-time activation email — click "Activate Form"
once and all future submissions arrive automatically.

## Updating the site
Replace `index.html` (or any file) in this repo. Vercel redeploys automatically.
