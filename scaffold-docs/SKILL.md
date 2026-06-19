---
name: scaffold-docs
description: Scaffold or refresh an MkDocs + Material documentation site for any
  project — plain markdown, C/C++, or Python. Run from inside the target repo
  root. Detects (or takes) a project profile, copies the generic docs kit, fills
  per-project values from the repo and git remote, wires the right API backend,
  and verifies with a strict build.
---

# scaffold-docs

Give any repository a clean MkDocs + Material documentation site. This is the
language-agnostic sibling of the suite-specific `pycemrg-docs` skill: the 8-step
spine is identical, but everything language-specific is read from a **profile
descriptor** in `assets/profiles/` instead of being hardcoded.

This skill is the **orchestrator**; the stateless template data lives in
`assets/`. Run it **from inside the target project's repo root** — it operates on
the current working directory and never takes a folder argument. Bundled
templates are referenced relative to this skill's own directory (`assets/...`);
target files are written relative to the user's cwd.

## Profiles (the data contract)

A profile is a small YAML descriptor that tells the orchestrator how to treat the
repo. v1 ships three, in `assets/profiles/`:

| Profile | For | API backend | Publish |
|---|---|---|---|
| `markdown` | docs-only / handbook / notes / spec | none | none |
| `cpp` | C / C++ (CMake, Make, Meson) | Doxygen via `mkdoxy` | none |
| `python` | Python lib/app (non-suite) | `mkdocstrings` (opt-in) | PyPI (opt-in) |

Read the chosen profile and let its fields drive every branch below — never
inline language assumptions into the steps. The fields are: `root_markers`,
`root_marker_mode`, `engine`, `api_backend`, `api_backend_default_enabled`,
`install_deps` (`base`/`api`), `system_deps`, `publish`,
`publish_default_enabled`, `nav_default`.

> For a pycemrg-suite library, use the **`pycemrg-docs`** skill instead — it adds
> the CEMRG branding and the suite palette registry this generic skill omits.

## The generic / per-project rule (respect it throughout)

- **Generic — copy byte-for-byte, never edit per project:** the `mkdocs.yml`
  `theme` / `markdown_extensions` / `plugins` blocks (minus the per-project API
  backend entry), and the workflow files.
- **Per-project — fill per repo:** `site_name`, `site_description`, `site_url`,
  `repo_url`, `repo_name`, the `palette` colours, and the `nav` contents.
- The `nav` spine order is fixed; the profile's `nav_default` lists which
  sections apply. Delete sections the project lacks; **never reorder**.

## Step 0 — Resolve the profile

1. If the user passed an explicit profile (`/scaffold-docs cpp`), use it.
2. Otherwise auto-detect: for each profile in `assets/profiles/`, test its
   `root_markers` against the cwd (exact filename match, or glob when
   `root_marker_mode: glob`). Exact-marker profiles (`python`, `cpp`) win over
   the glob fallback (`markdown`).
3. If two exact profiles match (e.g. a C++ project with a `setup.py` helper) or
   none match, **ask the user** which profile to use. Never guess silently.
4. Confirm the resolved profile to the user before proceeding.

## Step 1 — Preflight

1. Confirm the cwd is the intended repo root using the resolved profile's
   `root_markers`. For the `markdown` profile, require a git repo plus at least
   one `*.md`. If the check fails, stop and tell the user to run from the root.
2. Detect **fresh scaffold vs. refresh**: do `mkdocs.yml` and/or `docs/` already
   exist? Record which — it changes the write paths (Step 3) and the palette/nav
   handling (Step 4).
3. Read the repo's `CLAUDE.md` and/or `README` if present — the preferred source
   for the two content tables (Design principles, Key domain terms). Note whether
   it is rich or thin; thin/absent triggers the inference fallback in Step 5.
4. Read the git remote (`git remote get-url origin`) to derive owner/repo, and
   the project manifest (`pyproject.toml` name/description for python; project
   name from `CMakeLists.txt`/`README` for cpp; `README` H1 for markdown).

## Step 2 — Inventory existing docs (before writing anything)

List everything already present so write paths are decided by fact:

- Does `./mkdocs.yml` exist? Does `./docs/` exist, and what is in it (every file —
  `getting-started/`, `guides/`, `cli/`, custom `api/*` pages)?
- Do `./.github/workflows/docs.yml` / publish workflow exist?

Classify the run: **fresh scaffold** (no `mkdocs.yml` and no `docs/`) vs.
**refresh** (either exists). Report the inventory. Anything you find that the
skill does not explicitly write below is **out of scope — never delete, move, or
rewrite it.**

## Step 3 — Copy the machinery (profile-gated)

The split is structural, not discretionary.

**Generic machinery — safe to write/overwrite:**

- `assets/workflows/docs.yml` → `./.github/workflows/docs.yml`. Then edit the
  two install steps from the profile (Step 4) — drop the system-deps step when
  `system_deps` is empty.
- `assets/workflows/publish-pypi.yml` → `./.github/workflows/publish.yml`
  **only when** `publish: pypi` and the user opts in (ask;
  `publish_default_enabled` is the default answer).
- `assets/mkdocs.base.yml` → `./mkdocs.yml` **only on a fresh scaffold.** On a
  **refresh**, do not copy it; treat it as a merge in Step 4 — preserve the
  existing `nav`, `palette`, and `site_*` fields and only add missing generic
  keys.

Note the rename: assets store workflows flat in `workflows/`; they land in
`.github/workflows/` (and `publish-pypi.yml` → `publish.yml`).

**Content skeletons — copy ONLY into a path that does not already exist:**

- `assets/docs/index.md` → `./docs/index.md`
- `assets/docs/api/index.md` → `./docs/api/index.md` **only when the profile's
  `api_backend` is not `none`** (a markdown project gets no API section).

On a **refresh** where either already exists, do not copy the skeleton over it.
Leave the file and, in Step 5, edit it in place to fill genuine gaps (with the
user's confirmation).

## Step 4 — Fill the per-project markers in `mkdocs.yml`

On a fresh scaffold you fill the freshly copied base; on a refresh you edit the
existing `mkdocs.yml` in place. Either way, leave generic blocks byte-for-byte
identical and only touch per-project keys.

- `site_name`, `site_description`, `site_url`, `repo_url`, `repo_name` — derive
  from the git remote and manifest. `site_url` follows
  `https://<owner>.github.io/<repo>/`; `<owner>` is the GitHub owner/org from the
  remote. On a refresh, keep any real existing value; only fill markers/gaps.
- **`palette` primary/accent** — there is no suite registry here. On a **fresh
  scaffold**, ask the user for a Material colour, or pick a sensible default
  (e.g. `indigo`/`blue`) and tell them how to change it. On a **refresh** with a
  real existing palette, preserve it; only fill if it is still a `FILL-IN`
  marker.
- **API backend wiring** — if `api_backend` is enabled (ask, defaulting to
  `api_backend_default_enabled`): merge the matching snippet into the `plugins:`
  list — `assets/api-backends/mkdocstrings.snippet.yml` (python) or
  `assets/api-backends/doxygen/mkdoxy.snippet.yml` (cpp, and copy the `Doxyfile`
  only if the user wants standalone Doxygen). If `none`, leave `plugins:` as the
  generic default.
- **Install steps in `docs.yml`** — fill "Install MkDocs and plugins" from
  `install_deps.base` plus `install_deps.api` when the API backend is enabled.
  Keep the "Install system dependencies" step only when `system_deps` is
  non-empty (cpp → `doxygen`); otherwise delete that step.
- `nav` — start from the profile's `nav_default`, keep the order.
  - **Fresh scaffold:** include the `nav_default` sections, dropping any the
    repo does not actually have pages for yet.
  - **Refresh:** preserve existing `nav` entries (they point at real pages); only
    add an entry for a section you are newly creating.

## Step 5 — Populate content

- `docs/index.md` — fill the four-section skeleton: What this project does /
  Where to go next / Design principles (table) / Key domain terms (table). Remove
  "Where to go next" links to sections this profile dropped (e.g. API/CLI for
  markdown).
- `docs/api/index.md` (only when `api_backend != none`) — group the public
  modules/symbols into themed Module / What it does / Page tables. For an enabled
  backend, this index curates a map into the generated per-symbol pages.
- **Refresh safety:** for any page that already existed (per Step 2), do not
  regenerate from the skeleton — edit in place to fill genuine gaps only, and
  surface the proposed edits at the Step 6 gate. Only fully author a page the
  skill itself just created as empty.
- **Source for the two tables:** lift Design principles and Key domain terms from
  the repo's `CLAUDE.md`/`README` when rich enough.
- **Thin-source fallback:** if those tables cannot be lifted, infer them from the
  code (public modules, docstrings/headers, layout) and clearly mark inferred
  values as needing confirmation in Step 6 — do not silently ship guesses, and do
  not fail.

## Step 6 — Inference + confirm gate

Present **one** summary before writing final content: resolved profile; site
fields; chosen palette (assigned or preserved); whether the API backend and
publish workflow are enabled; the proposed contents of both tables (flagging
anything inferred); and — on a refresh — an explicit list of which existing files
you propose to edit, with a diff. Get explicit approval, then write. Never
overwrite an existing page without that approval.

## Step 7 — Verify

1. Run `mkdocs build --strict` from the repo root. This is the real CI gate; it
   **fails on broken internal links**. Report the result.
   - Local build needs the profile's deps: `pip install` of `install_deps.base`
     (+ `.api`), and for cpp the `doxygen` binary on PATH. Surface missing
     commands rather than assuming they are installed.
2. Grep the written files for leftover `FILL-IN` markers and report any as
   incomplete.

## Step 8 — Closing manual checklist

The skill cannot perform these one-time repo-settings actions. Print the ones
that apply to the resolved profile:

- **GitHub Pages (all profiles):** repo Settings → Pages → Source =
  "GitHub Actions" (not a branch), or `docs.yml` deploys nothing.
- **PyPI (python + publish only):** add the repo secret `PYPI_API_TOKEN`
  (a project-scoped PyPI token), or `publish.yml` cannot upload on release.
- Confirm the site goes live at `site_url` after the first push to `main`.

## Adding a new profile later

Drop a new descriptor in `assets/profiles/` (e.g. `node.yml`) following the same
field set, add an API-backend snippet under `assets/api-backends/` if it needs
one, and the orchestration above works unchanged — that is the whole point of the
profile contract. Hold to the Rule of Three before generalising further.
