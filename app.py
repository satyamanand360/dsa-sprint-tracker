import json
import os
import re
import uuid
from datetime import date, timedelta

import streamlit as st

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
st.set_page_config(page_title="DSA Sprint Tracker", page_icon="✅", layout="centered")

START_DATE = date(2026, 8, 9)
DEADLINE = date(2026, 9, 15)

PLAYLIST_TOTALS = {"trees": 54, "graphs": 56, "tries": 7, "greedy": 13, "dp": 50}
TOTAL_VIDEOS = sum(PLAYLIST_TOTALS.values())

PHASE_META = {
    "trees": {"label": "Trees", "color": "#4f9d69"},
    "graphs": {"label": "Graphs", "color": "#4f7cff"},
    "tries": {"label": "Tries", "color": "#c77dff"},
    "greedy": {"label": "Greedy", "color": "#ffb454"},
    "dp": {"label": "DP", "color": "#ff6b6b"},
}

DEFAULT_PLAN_RAW = [
    ("trees", "Videos 1–8 · Traversals", ["Watch/re-watch videos 1–8", "Implement: recursive Pre/In/Post order", "Implement: iterative Pre/In (1 stack)", "Implement: iterative Postorder (2-stack & 1-stack)"]),
    ("trees", "Videos 9–16 · Views & Variants", ["Watch/re-watch videos 9–16", "Implement: top/bottom/left/right view", "Implement: boundary & vertical order traversal"]),
    ("trees", "Videos 17–24 · Tree Properties", ["Watch/re-watch videos 17–24", "Implement: height, diameter, balanced check", "Implement: max path sum, same/symmetric tree, LCA, max width"]),
    ("trees", "Videos 25–32 · More Problems", ["Watch/re-watch videos 25–32", "Implement: children sum property, nodes at distance K", "Implement: burn tree, count complete-BT nodes, serialize/deserialize"]),
    ("trees", "Videos 33–40 · Morris + BST Intro", ["Watch videos 33–40 (new ground)", "Implement: Morris inorder/preorder traversal", "Implement: construct tree from traversals, BST search/insert"]),
    ("trees", "Videos 41–48 · BST Core", ["Watch videos 41–48", "Implement: delete node in BST, validate BST", "Implement: ceil/floor, construct BST from preorder, kth smallest/largest"]),
    ("trees", "Videos 49–54 · BST Advanced + Buffer", ["Watch videos 49–54", "Implement: two sum in BST, recover BST, largest BST in BT", "Catch up on any of videos 1–54 not yet implemented"]),

    ("graphs", "Videos 1–5 · Graph Basics", ["Watch videos 1–5", "Implement: adjacency list/matrix, BFS, DFS", "Implement: number of provinces"]),
    ("graphs", "Videos 6–10 · BFS/DFS Applications", ["Watch videos 6–10", "Implement: flood fill, rotten oranges", "Implement: cycle detection — undirected (BFS & DFS)"]),
    ("graphs", "Videos 11–15 · Matrix Problems", ["Watch videos 11–15", "Implement: 0/1 matrix nearest cell, surrounded regions", "Implement: number of enclaves, distinct islands"]),
    ("graphs", "Videos 16–20 · Word Ladder & Bipartite", ["Watch videos 16–20", "Implement: word ladder I & II", "Implement: bipartite graph check (BFS/DFS)"]),
    ("graphs", "Videos 21–25 · Topo Sort", ["Watch videos 21–25", "Implement: cycle detection — directed (DFS)", "Implement: topo sort DFS & BFS (Kahn's)"]),
    ("graphs", "Videos 26–30 · Ordering Applications", ["Watch videos 26–30", "Implement: course schedule I & II, alien dictionary", "Implement: shortest path in DAG"]),
    ("graphs", "Videos 31–35 · Dijkstra", ["Watch videos 31–35", "Implement: shortest path unit-weight, Dijkstra's algorithm", "Implement: print shortest path (Dijkstra)"]),
    ("graphs", "Videos 36–40 · Shortest Path Practice", ["Watch videos 36–40", "Implement: binary maze, path with min effort", "Implement: cheapest flights within K stops, Bellman-Ford"]),
    ("graphs", "Videos 41–44 · Bellman-Ford & Floyd", ["Watch videos 41–44", "Implement: network delay time, ways to arrive at destination", "Implement: Floyd-Warshall algorithm"]),
    ("graphs", "Videos 45–48 · MST & DSU", ["Watch videos 45–48", "Implement: city with smallest neighbors, MST intro", "Implement: Prim's algorithm, DSU basics"]),
    ("graphs", "Videos 49–52 · Kruskal's & DSU Apps", ["Watch videos 49–52", "Implement: Kruskal's algorithm", "Implement: accounts merge, number of islands II"]),
    ("graphs", "Videos 53–56 · SCC + Buffer", ["Watch videos 53–56", "Implement: Kosaraju's algorithm, bridges, articulation points", "Catch up on any of videos 1–56 not yet implemented"]),

    ("tries", "Videos 1–4 · Trie Fundamentals", ["Watch videos 1–4", "Implement: Trie — insert/search/startsWith", "Implement: Trie-II — count distinct substrings"]),
    ("tries", "Videos 5–7 · Trie on Bits + Buffer", ["Watch videos 5–7", "Implement: max XOR of two numbers, max XOR with array element", "Catch up + practice 3–4 extra trie problems"]),

    ("greedy", "Videos 1–3 · Greedy Basics", ["Watch videos 1–3", "Implement: N meetings in one room", "Implement: jump game, jump game II"]),
    ("greedy", "Videos 4–6 · Scheduling I", ["Watch videos 4–6", "Implement: minimum number of platforms", "Implement: job sequencing problem, candy"]),
    ("greedy", "Videos 7–9 · Scheduling II", ["Watch videos 7–9", "Implement: shortest job first (SJF)", "Implement: min cost to cut a stick, fractional knapsack"]),
    ("greedy", "Videos 10–13 · Intervals + Buffer", ["Watch videos 10–13", "Implement: valid parenthesis string, insert & merge intervals", "Implement: non-overlapping intervals + catch up on pending"]),

    ("dp", "Videos 1–4 · 0/1 Knapsack", ["Watch videos 1–4", "Implement: recursive brute force → memoization", "Implement: tabulation + space optimization"]),
    ("dp", "Videos 5–8 · Knapsack Variants I", ["Watch videos 5–8", "Implement: subset sum, equal subset partition", "Implement: count subsets with given sum, min subset sum diff"]),
    ("dp", "Videos 9–12 · Knapsack Variants II", ["Watch videos 9–12", "Implement: count partitions with given diff, target sum", "Implement: number of dice rolls with target sum"]),
    ("dp", "Videos 13–16 · Unbounded Knapsack", ["Watch videos 13–16", "Implement: rod cutting, coin change (max coins)", "Implement: coin change (min coins), max ribbon cut"]),
    ("dp", "Videos 17–20 · LCS Pattern I", ["Watch videos 17–20", "Implement: longest common subsequence, print LCS", "Implement: longest common substring"]),
    ("dp", "Videos 21–24 · LCS Pattern II", ["Watch videos 21–24", "Implement: shortest common supersequence", "Implement: min insertions/deletions, longest palindromic subsequence"]),
    ("dp", "Videos 25–28 · LCS Pattern III", ["Watch videos 25–28", "Implement: min insertions to make palindrome", "Implement: LCS of 3 strings, longest repeating subsequence"]),
    ("dp", "Videos 29–32 · DP on Strings", ["Watch videos 29–32", "Implement: sequence pattern matching, wildcard matching", "Implement: edit distance"]),
    ("dp", "Videos 33–36 · MCM Pattern I", ["Watch videos 33–36", "Implement: matrix chain multiplication (recursive/memo/tab)", "Implement: min cost to cut a stick, burst balloons"]),
    ("dp", "Videos 37–40 · MCM Pattern II", ["Watch videos 37–40", "Implement: boolean parenthesization (evaluate to true)", "Implement: palindrome partitioning II, scramble string"]),
    ("dp", "Videos 41–44 · DP on Stocks", ["Watch videos 41–44", "Implement: buy/sell stock I & II", "Implement: buy/sell stock III & IV"]),
    ("dp", "Videos 45–47 · Stocks Wrap + Fibonacci Revise", ["Watch videos 45–47", "Implement: cooldown & transaction fee variants", "Quick revise: climbing stairs, house robber, frog jump"]),
    ("dp", "Videos 48–50 · LIS Pattern + Final Buffer", ["Watch videos 48–50", "Implement: LIS (memo, tab, binary search), number of LIS, largest divisible subset", "Clear ANY unimplemented video from all 5 playlists — this is the hard cutoff"]),
]


def fresh_plan():
    return [
        {
            "id": str(uuid.uuid4()),
            "phase": phase,
            "title": title,
            "tasks": [{"id": str(uuid.uuid4()), "text": t, "done": False} for t in tasks],
            "notes": "",
        }
        for phase, title, tasks in DEFAULT_PLAN_RAW
    ]


# ---------------------------------------------------------------------------
# Persistence — Google Sheets in production, local JSON file for local dev
# ---------------------------------------------------------------------------
LOCAL_FALLBACK_FILE = "tracker_state.json"


def _sheets_configured():
    try:
        return "gcp_service_account" in st.secrets and "SHEET_ID" in st.secrets
    except Exception:
        return False


@st.cache_resource(show_spinner=False)
def _get_worksheet():
    import gspread
    from google.oauth2.service_account import Credentials

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"], scopes=scopes
    )
    client = gspread.authorize(creds)
    sh = client.open_by_key(st.secrets["SHEET_ID"])
    try:
        ws = sh.worksheet("tracker_data")
    except Exception:
        ws = sh.add_worksheet(title="tracker_data", rows=10, cols=2)
    return ws


def load_state():
    if _sheets_configured():
        try:
            ws = _get_worksheet()
            val = ws.acell("A1").value
            if val:
                return json.loads(val)
            return fresh_plan()
        except Exception as e:
            st.warning(f"Couldn't load saved progress from Google Sheets, starting fresh: {e}")
            return fresh_plan()
    if os.path.exists(LOCAL_FALLBACK_FILE):
        try:
            with open(LOCAL_FALLBACK_FILE) as f:
                return json.load(f)
        except Exception:
            pass
    return fresh_plan()


def save_state():
    if _sheets_configured():
        try:
            ws = _get_worksheet()
            ws.update_acell("A1", json.dumps(st.session_state.days))
            return
        except Exception as e:
            st.warning(f"Couldn't save progress to Google Sheets: {e}")
            return
    try:
        with open(LOCAL_FALLBACK_FILE, "w") as f:
            json.dump(st.session_state.days, f)
    except Exception as e:
        st.warning(f"Couldn't save progress: {e}")


if "days" not in st.session_state:
    st.session_state.days = load_state()


def date_for_index(i):
    return START_DATE + timedelta(days=i)


# ---------------------------------------------------------------------------
# Mutations (used as widget callbacks)
# ---------------------------------------------------------------------------
def toggle_task(day_idx, task_idx):
    days = st.session_state.days
    days[day_idx]["tasks"][task_idx]["done"] = not days[day_idx]["tasks"][task_idx]["done"]
    save_state()


def move_task(day_idx, task_idx, direction):
    days = st.session_state.days
    target = day_idx + direction
    if target < 0 or target >= len(days):
        return
    task = days[day_idx]["tasks"].pop(task_idx)
    if direction < 0:
        days[target]["tasks"].append(task)
    else:
        days[target]["tasks"].insert(0, task)
    if len(days[day_idx]["tasks"]) == 0:
        days.pop(day_idx)
    save_state()


def pull_next_into_today(day_idx):
    days = st.session_state.days
    if day_idx + 1 >= len(days):
        return
    nxt = days.pop(day_idx + 1)
    days[day_idx]["tasks"].extend(nxt["tasks"])
    days[day_idx]["title"] = days[day_idx]["title"] + " + " + nxt["title"]
    save_state()


def update_notes(day_id, widget_key):
    for d in st.session_state.days:
        if d["id"] == day_id:
            d["notes"] = st.session_state[widget_key]
            break
    save_state()


def reset_plan():
    st.session_state.days = fresh_plan()
    save_state()


# ---------------------------------------------------------------------------
# Stats
# ---------------------------------------------------------------------------
def compute_stats():
    days = st.session_state.days
    total_tasks = sum(len(d["tasks"]) for d in days)
    done_tasks = sum(sum(1 for t in d["tasks"] if t["done"]) for d in days)

    today = date.today()
    today_idx = next((i for i in range(len(days)) if date_for_index(i) == today), None)
    if today_idx is None and days and date_for_index(len(days) - 1) < today:
        today_idx = len(days) - 1

    streak = 0
    if today_idx is not None:
        for i in range(today_idx, -1, -1):
            d = days[i]
            if d["tasks"] and all(t["done"] for t in d["tasks"]):
                streak += 1
            else:
                break
    return total_tasks, done_tasks, streak


def videos_left():
    days = st.session_state.days
    done = 0.0
    for d in days:
        matches = re.findall(r"Videos (\d+)–(\d+)", d["title"])
        count = sum(int(b) - int(a) + 1 for a, b in matches)
        frac = (sum(1 for t in d["tasks"] if t["done"]) / len(d["tasks"])) if d["tasks"] else 0
        done += count * frac
    return max(0, round(TOTAL_VIDEOS - done))


# ---------------------------------------------------------------------------
# Styling
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
    .stApp { background-color: #0f1117; }
    .block-container { padding-top: 2rem; max-width: 760px; }
    .phase-tag {
        display:inline-block; font-size:11px; text-transform:uppercase; letter-spacing:0.06em;
        padding:2px 8px; border-radius:6px; font-weight:600; margin-right:8px;
    }
    .day-date { color:#8b90a3; font-size:12px; }
    .today-badge { color:#fff; font-size:11px; font-weight:700; }
    .rail-wrap { display:flex; height:10px; border-radius:6px; overflow:hidden; border:1px solid #2a2f3f; margin-bottom:4px;}
    .rail-seg { height:100%; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.title("DSA Sprint — Trees → Graphs → Tries → Greedy → DP")
st.caption(
    "All 180 videos across 5 playlists, watched **and** implemented. "
    "Hard cutoff **15 Sep 2026** — pull work forward and finish sooner."
)

days = st.session_state.days
total_tasks, done_tasks, streak = compute_stats()
finish_date = date_for_index(len(days) - 1) if days else None

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Days to cutoff", max(0, (DEADLINE - date.today()).days))
c2.metric("Projected finish", finish_date.strftime("%d %b") if finish_date else "Done! 🎉")
c3.metric("Day streak", streak)
c4.metric("Tasks cleared", f"{round(done_tasks / total_tasks * 100) if total_tasks else 100}%")
c5.metric("Videos left", videos_left())

# progress rail
if days:
    total_original = (DEADLINE - START_DATE).days + 1
    seg_html = "".join(
        f'<div class="rail-seg" style="width:{100/total_original:.3f}%; '
        f'background:{PHASE_META.get(d["phase"], {}).get("color", "#565b6e")}"></div>'
        for d in days
    )
    st.markdown(f'<div class="rail-wrap">{seg_html}</div>', unsafe_allow_html=True)

st.divider()

# ---------------------------------------------------------------------------
# Toolbar
# ---------------------------------------------------------------------------
filter_labels = ["All"] + [m["label"] for m in PHASE_META.values()]
filter_ids = ["all"] + list(PHASE_META.keys())
tb1, tb2 = st.columns([5, 1])
with tb1:
    chosen_label = st.radio("Filter", filter_labels, horizontal=True, label_visibility="collapsed")
active_filter = filter_ids[filter_labels.index(chosen_label)]
with tb2:
    st.button("↺ Reset", on_click=reset_plan, use_container_width=True)

st.info(
    "Use ▲ / ▼ next to a task to pull it into the previous/next day, or **Pull tomorrow into today** "
    "on a card. Empty days vanish and everything after shifts one date earlier — pulling work forward "
    "shortens your finish date."
)

# ---------------------------------------------------------------------------
# Day cards
# ---------------------------------------------------------------------------
if not days:
    st.success("🎉 Every video across all 5 playlists is watched and implemented. Plan complete.")
else:
    today = date.today()
    last_phase = None
    for i, d in enumerate(days):
        if active_filter != "all" and d["phase"] != active_filter:
            continue

        meta = PHASE_META.get(d["phase"], {"label": d["phase"], "color": "#565b6e"})
        if active_filter == "all" and d["phase"] != last_phase:
            st.markdown(f"#### :{'green' if d['phase']=='trees' else 'blue'}[{meta['label']}]" if False else f"**{meta['label']}**")
            last_phase = d["phase"]

        this_date = date_for_index(i)
        is_today = this_date == today
        done_count = sum(1 for t in d["tasks"] if t["done"])

        with st.container(border=True):
            top_l, top_r = st.columns([5, 1])
            with top_l:
                badge = f'<span class="phase-tag" style="background:{meta["color"]}22; color:{meta["color"]}">{meta["label"]}</span>'
                date_str = this_date.strftime("%a, %d %b")
                today_str = ' <span class="today-badge">· TODAY</span>' if is_today else ""
                st.markdown(f'{badge}<span class="day-date">{date_str}{today_str}</span>', unsafe_allow_html=True)
                st.markdown(f"**{d['title']}**")
            with top_r:
                st.markdown(f"<div style='text-align:right; color:#8b90a3; padding-top:8px;'>{done_count}/{len(d['tasks'])}</div>", unsafe_allow_html=True)

            for ti, t in enumerate(d["tasks"]):
                tc1, tc2, tc3 = st.columns([9, 1, 1])
                with tc1:
                    st.checkbox(
                        t["text"],
                        value=t["done"],
                        key=f"chk_{t['id']}",
                        on_change=toggle_task,
                        args=(i, ti),
                    )
                with tc2:
                    st.button("▲", key=f"up_{t['id']}", disabled=(i == 0),
                               on_click=move_task, args=(i, ti, -1))
                with tc3:
                    st.button("▼", key=f"down_{t['id']}", disabled=(i == len(days) - 1),
                               on_click=move_task, args=(i, ti, 1))

            bottom_l, bottom_r = st.columns([3, 2])
            with bottom_r:
                if i < len(days) - 1:
                    st.button("⇤ Pull tomorrow into today", key=f"pull_{d['id']}",
                               on_click=pull_next_into_today, args=(i,))

            notes_key = f"notes_{d['id']}"
            with st.expander("Notes"):
                st.text_area(
                    "Notes",
                    value=d.get("notes", ""),
                    key=notes_key,
                    label_visibility="collapsed",
                    on_change=update_notes,
                    args=(d["id"], notes_key),
                )
