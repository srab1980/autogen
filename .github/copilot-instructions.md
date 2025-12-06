# AI Agent Instructions for This Repository

This workspace currently has no source files. This guide scaffolds how AI agents should discover architecture and workflows once the repo content is present. Replace placeholders with concrete details after the codebase is loaded.

## Discovery Checklist (run first)
- Scan for manifests: `package.json`, `pyproject.toml`, `requirements.txt`, `Cargo.toml`, `go.mod`.
- Check CI: `.github/workflows/**` for build/test commands and env.
- Inspect entrypoints: `src/**`, `app/**`, `main.*`, `server.*`, CLI under `bin/**`.
- Look for infra: `Dockerfile`, `docker-compose.yml`, `Makefile`, `terraform/**`.
- Read docs: `README.md` and any `AGENT.md`, `.cursorrules`, `.windsurfrules`, `.clinerules`.

## How To Infer Architecture
- Identify primary language from manifests and dominant directories (e.g., `src`, `lib`).
- Map service boundaries by locating separate apps/packages and their build targets.
- Trace data flow from entrypoints (HTTP handlers, CLI commands, event consumers) to storage (DB clients, file IO, external APIs).
- Note framework conventions (e.g., Next.js pages, FastAPI routers, Express middlewares) and where routing/controllers live.

## Workflow Extraction
- Prefer CI-defined commands as canonical. Replicate `jobs.build/test` steps locally.
- If `package.json` exists, read `scripts` for run/test/lint. If Python, check `Makefile`, `tox.ini`, `noxfile.py`, or `pytest.ini`.
- Debugging: collect non-obvious env vars from `.env`, CI secrets names, or config files.
- Containers: if `Dockerfile`/`compose` exist, document the build/run commands and service names.

## Conventions To Record
- Project-specific coding patterns found in helpers/util modules; reference exact files and functions.
- Error handling and logging libraries and wrappers; show examples from code.
- Testing style: unit vs integration layout, fixtures location, and coverage thresholds from configs.
- Configuration management: how settings are loaded (env, YAML/JSON, pydantic, dotenv), and precedence.

## Integration Points
- External APIs/SDKs: list client modules and base URLs/regions.
- Messaging/queues: topic names, producers/consumers, retry strategy.
- Datastores: connection libraries, migration tooling and locations.

## When Content Is Available
- Update this file with concrete references: paths, commands, and short examples per section.
- Keep it concise (20–50 lines) with links to key files and exact script names.
- Merge existing guidance if a prior `.github/copilot-instructions.md` exists; preserve valuable specifics and deprecate outdated parts.

## Quick Commands (PowerShell)
Use these to explore once files exist:
```pwsh
Get-ChildItem -Recurse -File | Select-Object -First 50
Select-String -Path **/* -Pattern "TODO|FIXME|HACK" -SimpleMatch
Get-ChildItem -Recurse -Filter package.json | ForEach-Object { Get-Content $_ }
Get-ChildItem -Recurse -Filter pyproject.toml | ForEach-Object { Get-Content $_ }
```

---
If this folder is not the intended repo, please open the correct project directory or provide the repository path. Once the codebase is present, I will replace this scaffold with precise, project-specific instructions.