# gh-action-example

A basic Palmer Penguins [Shiny for Python](https://shiny.posit.co/py/) app used to test publishing to Posit Connect via GitHub Actions, per the [Publishing from GitHub Actions](https://docs.posit.co/connect/user/publishing-github-actions/index.html) docs.

## App

`app.py` renders a scatterplot over the `palmerpenguins` dataset, with sidebar controls for species and X/Y variables.

Run locally:

```bash
uv venv .venv
uv pip install -r requirements.txt -p .venv/bin/python
.venv/bin/python -m shiny run app.py
```

## Deployment

Content already exists on Connect (GUID `<content-guid>`), created once via a manual `rsconnect deploy shiny` run. From then on, `.github/workflows/publish.yml` uses [`posit-dev/connect-actions/deploy@main`](https://github.com/posit-dev/connect-actions) to push updates to that same content on every push to `main`.

- Connect server: `https://connect.example.com` (use the server root, not a `/connect` path, which is only part of the browser UI route on some installs)
- App URL: `https://connect.example.com/content/<content-guid>/`

Authentication uses [Trusted Publishing](https://docs.posit.co/connect/user/trusted-publishing/) (OIDC) rather than a stored API key: the workflow requests `id-token: write` permission, and `connect-actions/deploy` exchanges a GitHub OIDC token for a short-lived Connect credential at deploy time. This requires a trusted publisher configured on the content in Connect (Settings → Source → Trusted Publishing) with this repo's identifier — since this repo was created after 2026-07-15, GitHub issues OIDC tokens with immutable numeric subject claims, so the trusted publisher must use the `owner@id/repo@id` form (`<owner>@<owner-id>/<repo>@<repo-id>`) rather than `<owner>/<repo>`.
