# DSA Sprint Tracker

Streamlit version of the Trees → Graphs → Tries → Greedy → DP tracker
(Aug 9 – Sep 15 2026), with drag-forward flexibility: pull individual
tasks or a whole day's work into today, and the schedule compresses
automatically.

## Deploy on Streamlit Community Cloud (free)

1. Create a new **public or private GitHub repo** (e.g. `dsa-sprint-tracker`)
   and push these three files/folders to it:
   - `app.py`
   - `requirements.txt`
   - `.streamlit/config.toml`
2. Go to **[share.streamlit.io](https://share.streamlit.io)** and sign in
   with GitHub.
3. Click **"New app"** → pick your repo → branch `main` → main file path
   `app.py` → **Deploy**.
4. You'll get a URL like `https://your-app-name.streamlit.app` — bookmark
   it on your phone and laptop.

## Local run (to test before deploying)

```bash
pip install streamlit
streamlit run app.py
```

## ⚠️ Important: progress storage

This app saves your checkboxes/notes/reordering to a local file
(`tracker_state.json`) next to `app.py`. That works fine while you're
using the app normally, but on Streamlit Community Cloud the filesystem
is **ephemeral** — if the app goes to sleep from inactivity (roughly 7+
days unused) and later reboots, or if you push a new commit, that file
can be wiped and your progress resets to the original plan.

Given you'll be using this daily, this is usually fine in practice. But
if you want it bullet-proof across redeploys, the simplest upgrade is
swapping the two `load_state()` / `save_state()` functions in `app.py`
for a tiny SQLite file on a persistent volume, or a free service like
Supabase/Google Sheets as the backing store — say the word and I can
wire that in.
