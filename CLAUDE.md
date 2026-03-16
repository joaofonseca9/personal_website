# Personal Website / CV

Jekyll personal website + CV deployed to GitHub Pages.

## Architecture

- `_data/data.yml` is the single source of truth for CV content
- Jekyll templates in `_includes/` render the website from `data.yml`
- `generate_cv_pdf.py` reads `data.yml` and generates `cv_harvard.tex` for PDF export
- GitHub Actions builds both the Jekyll site and compiles the LaTeX PDF

## Key Files

| File | Purpose |
|------|---------|
| `_data/data.yml` | CV content (experience, education, skills, publications) |
| `generate_cv_pdf.py` | Python script to generate LaTeX from data.yml |
| `.github/workflows/deploy.yml` | CI/CD: Jekyll build + LaTeX compile + GitHub Pages deploy |
| `_includes/*.html` | Jekyll partial templates |
| `_config.yml` | Jekyll site configuration |

## Development

- Local website: `bundle exec jekyll serve`
- Generate LaTeX: `python generate_cv_pdf.py` (PDF compilation needs a LaTeX distribution)
- Deploy: push to `main` triggers GitHub Actions

## Important Notes

- `_includes/skills.html` is hardcoded with icons/tech stack -- it is NOT driven by `data.yml`. Changes to skills require updating both files.
- The PDF pipeline uses `xu-cheng/latex-action@v3` with pdflatex (no lualatex/fontspec dependencies).
