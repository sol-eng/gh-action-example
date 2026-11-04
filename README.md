# gh-action-example

> [!WARNING]
> This example fails until you configure it. The repository contains placeholder values
> (`https://connect.example.com` and `<content-guid>`) that point to no real Connect server. The
> `publish` workflow runs on every push to `main`, so it fails on each push until you complete
> [Set up before you use this](#set-up-before-you-use-this).

A basic Palmer Penguins [Shiny for Python](https://shiny.posit.co/py/) app used to test publishing to Posit Connect via GitHub Actions, per the [Publishing from GitHub Actions](https://docs.posit.co/connect/user/publishing-github-actions/index.html) docs.

## App

`app.py` renders a scatterplot over the `palmerpenguins` dataset, with sidebar controls for species and X/Y variables.

Run locally:

```bash
uv venv .venv
uv pip install -r requirements.txt -p .venv/bin/python
.venv/bin/python -m shiny run app.py
```

## Set up before you use this

If you fork or copy this repository, complete these steps. Until you do, the `publish` workflow fails.

Trusted Publishing needs two things on your Connect server:

- Connect 2026.07.0 or newer.
- An Enhanced or Advanced license.

If your server does not meet these requirements, the login step fails. In that case, pass `connect-api-key` to `posit-dev/connect-actions/deploy` instead.

1. Deploy the app to your Connect server once with `rsconnect deploy shiny`. This creates the content item and its GUID (a unique content ID).
2. In `.github/workflows/publish.yml`, replace `https://connect.example.com` with your Connect server root URL.
3. In the same file, replace `<content-guid>` with the GUID from step 1.
4. In Connect, open the content, then Settings, Source, Trusted Publishing. Add a trusted publisher for your repository. Use the identifier form described in [Deployment](#deployment).
5. Push a commit to `main`. Open the Actions tab in GitHub to make sure that the `publish` run succeeds.

If the run fails, read the log for the `Deploy to Connect` step. The most common causes are a placeholder value that you did not replace and a trusted publisher that does not match your repository.

## Deployment

Content already exists on Connect (GUID `<content-guid>`), created once via a manual `rsconnect deploy shiny` run. From then on, `.github/workflows/publish.yml` uses [`posit-dev/connect-actions/deploy@main`](https://github.com/posit-dev/connect-actions) to push updates to that same content on every push to `main`.

- Connect server: `https://connect.example.com` (use the server root, not a `/connect` path, which is only part of the browser UI route on some installs)
- App URL: `https://connect.example.com/content/<content-guid>/`

Authentication uses [Trusted Publishing](https://docs.posit.co/connect/user/trusted-publishing/) (OIDC) rather than a stored API key: the workflow requests `id-token: write` permission, and `connect-actions/deploy` exchanges a GitHub OIDC token for a short-lived Connect credential at deploy time. This requires a trusted publisher configured on the content in Connect (Settings → Source → Trusted Publishing) with this repo's identifier — since this repo was created after 2026-07-15, GitHub issues OIDC tokens with immutable numeric subject claims, so the trusted publisher must use the `owner@id/repo@id` form (`<owner>@<owner-id>/<repo>@<repo-id>`) rather than `<owner>/<repo>`.
