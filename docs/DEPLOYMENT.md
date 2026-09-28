# GitHub / Vercel deployment

Repository: https://github.com/NestaLoda/agrohydrolatest

Deploy the repository root. `vercel.json` builds `frontend` with its lockfile,
serves `frontend/dist`, and routes `/api/*` to the existing FastAPI app through
`api/index.py`. Python 3.12 is pinned in `.python-version`; `requirements.txt`
contains runtime dependencies. Local ingestion/testing additionally needs
`requirements-dev.txt` (the historical complete lockfile is retained).

Exact dataset and source bytes matter to the scientific provenance checks.
`.gitattributes` disables newline conversion. Do not reformat source datasets.

## Cloud storage boundary

Calculations, climate data, comparison views, Jury Mode, and PDF export use the
existing scientific engine. Noto Sans and its SIL Open Font License are bundled
for Turkish PDF output on Linux as well as Windows.

Vercel calculation caches and SQLite run metadata live under the system temporary
directory. They are disposable and are not durable research evidence. The health
endpoint reports `persistent_field_records: false` in this environment. Endpoints
that upload PWN evidence or write/compare PRE/POST research records return an
explicit 409 directing users to the persistent local application. They must not
silently claim successful durable storage. Local behavior stays persistent.

Private local observations, frozen runs, SQLite files, environments, credentials,
dependency directories and temporary outputs are excluded from Git. Presentation
deliverables and project documentation are included in Git but excluded from the
Vercel upload/function bundle. No scientific data is relabelled as a measurement.

## Verification

Run `npm run build --prefix frontend`, `.venv/Scripts/python.exe -m pytest`, then
verify `/api/health`, Turkey calculation, North calculation/reference, both PDF
exports and the desktop UI on the deployed domain. Do not run mobile tests.

Deploy with `vercel --prod --yes`; use `vercel git connect` to keep future GitHub
pushes connected. Latest actual results and URLs are in `ANA_CHAT_TESLIM.txt`.

Reference: https://vercel.com/docs/functions/runtimes/python
Font source: https://github.com/notofonts/noto-fonts
