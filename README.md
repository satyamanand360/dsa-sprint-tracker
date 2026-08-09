# DSA Sprint Tracker

Streamlit version of the Trees → Graphs → Tries → Greedy → DP tracker
(Aug 9 – Sep 15 2026). Pull individual tasks or a whole day's work into
today with ▲/▼ or "Pull tomorrow into today" — the schedule compresses
automatically. Progress is saved to a **free Google Sheet**, so it
survives redeploys and app sleeps on Streamlit Community Cloud (no
paid hosting or persistent volume needed).

## 1. Set up the Google Sheet (one-time, ~5 min)

1. Go to **[Google Cloud Console](https://console.cloud.google.com/)**,
   create a new project (or reuse one) — no billing account required.
2. Enable two APIs for that project: **Google Sheets API** and
   **Google Drive API** (search each in the top search bar → Enable).
3. Go to **IAM & Admin → Service Accounts → Create Service Account**.
   Name it anything (e.g. `dsa-tracker-bot`). Skip granting project
   roles — not needed.
4. Open the new service account → **Keys** tab → **Add Key → Create
   new key → JSON**. This downloads a `.json` credentials file. Keep
   it private — never commit it to GitHub.
5. Create a new **Google Sheet** (sheets.new). Note the long ID in its
   URL: `https://docs.google.com/spreadsheets/d/THIS_PART_IS_THE_ID/edit`
6. Open the downloaded JSON file, copy the `client_email` value
   (looks like `dsa-tracker-bot@your-project.iam.gserviceaccount.com`).
   **Share the Google Sheet with that email address as Editor.**

## 2. Deploy on Streamlit Community Cloud

1. Push `app.py`, `requirements.txt`, and `.streamlit/config.toml` to a
   GitHub repo. **Do not** push the downloaded credentials JSON.
2. Go to **[share.streamlit.io](https://share.streamlit.io)** → sign
   in with GitHub → **New app** → pick the repo → main file `app.py`
   → Deploy.
3. Once deployed, open **App settings → Secrets** and paste (fill in
   from your downloaded JSON and your sheet URL):

   ```toml
   SHEET_ID = "your-sheet-id-from-the-url"

   [gcp_service_account]
   type = "service_account"
   project_id = "your-project-id"
   private_key_id = "..."
   private_key = "-----BEGIN PRIVATE KEY-----\nMIIEvQ...\n-----END PRIVATE KEY-----\n"
   client_email = "dsa-tracker-bot@your-project.iam.gserviceaccount.com"
   client_id = "..."
   auth_uri = "https://accounts.google.com/o/oauth2/auth"
   token_uri = "https://oauth2.googleapis.com/token"
   auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
   client_x509_cert_url = "..."
   ```

   Copy these values straight out of the downloaded JSON file — every
   field maps 1:1. Keep the `\n` characters inside `private_key` as
   literal `\n` (don't turn them into real line breaks).
4. Save. The app reboots and now reads/writes your Google Sheet.
   Progress persists forever, across redeploys and sleep cycles.

## Local run / testing

Local dev works out of the box with **no Google setup required** — if
`SHEET_ID` and `gcp_service_account` aren't found in secrets, the app
automatically falls back to a local `tracker_state.json` file next to
`app.py`.

```bash
pip install -r requirements.txt
streamlit run app.py
```

To test against the real Google Sheet locally too, create
`.streamlit/secrets.toml` with the same content shown in step 2.3
above (this file is gitignored by convention — never commit it).
