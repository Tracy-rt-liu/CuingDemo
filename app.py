import streamlit as st
import time
import random
import pandas as pd
import altair as alt

st.set_page_config(layout="wide", page_title="Cuing Agent")

# --- Custom CSS ---
st.markdown("""
<style>
[data-testid="stHorizontalBlock"] { align-items: center; }
</style>
""", unsafe_allow_html=True)

st.title("🏭 Cuing Agent")

# --- Session State ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "streaming_done" not in st.session_state:
    st.session_state.streaming_done = True
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "step" not in st.session_state:
    st.session_state.step = 0

# --- Response Definitions ---
STEP_0_BLOCKS = [
    {
        "type": "text",
        "content": (
            "To diagnose the yield decline, I'd like to validate four potential drivers:\n\n"
            "| Metric | Last Week | 4-Week Avg | Delta |\n"
            "| --- | --- | --- | --- |\n"
            "| First Pass Yield | 88.2% | 92.5% | -4.3pp |\n"
            "| Throughput / Worker | 13 units/day | 15 units/day | -13% |\n"
            "| OEE | 71% | 78% | -7pp |\n"
            "| Scrap Rate | 6.5% | 3.8% | +2.7pp |\n"
            "| Rework Hours | +22% | Baseline | ↑ |\n\n"
            "**Labor ramp & productivity**  \n"
            "**Equipment performance (OEE)**  \n"
            "**Material quality**  \n"
            "**Process bottlenecks / cycle time shifts**\n\n"
            "Based on your SAP + MES integration, here's what I see for "
            "last week vs trailing 4-week average:"
        ),
    },
    {
        "type": "text",
        "content": (
            "\n---\n\n"
            "**🔧 Labor Changes Identified**\n"
            "- 3 new workers onboarded 4 weeks ago\n"
            "- Standard training ramp: 4 weeks\n"
            "- Current effective productivity of new workers estimated "
            "at 70–80% of experienced operator\n\n"
            "**Please confirm:**"
        ),
    },
    {
        "type": "questions",
        "items": [
            {"id": "ramp_assumption", "text": "Is the 4-week ramp assumption accurate?"},
            {"id": "new_hires_line", "text": "Are the new hires assigned to the affected line?"},
            {"id": "scrap_shifts", "text": "Has scrap increased on specific shifts?"},
        ],
    },
    {
        "type": "text",
        "content": (
            "\n---\n\n"
            "**⚙️ Equipment Observations**\n"
            "- Line 3 stamping press last major overhaul: March 2021\n"
            "- Recommended refurbishment cycle: 18–24 months\n"
            "- Unplanned downtime last week: +18%\n"
            "- Minor stoppages: +27%\n\n"
            "**Can you confirm:**"
        ),
    },
    {
        "type": "questions",
        "items": [
            {"id": "micro_stoppages", "text": "Have you experienced increased micro-stoppages?"},
            {"id": "maintenance_deferrals", "text": "Any recent maintenance deferrals?"},
        ],
    },
]

STEP_1_BLOCKS = [
    {
        "type": "text",
        "content": (
            "Thank you for confirming the inputs. Below is a structured "
            "assessment of impact by driver, ranked by materiality."
        ),
    },
    {
        "type": "text",
        "content": (
            "\n---\n\n"
            "**A. Labor Ramp Impact – Low to Moderate**\n\n"
            "**System Data:**\n"
            "- 20 operators total\n"
            "- 3 new operators\n"
            "- Experienced productivity: 15 units/day\n"
            "- New operator productivity during ramp: 75%\n\n"
            "**Effective Output Calculation**\n\n"
            "Experienced output:\n"
            "17 workers × 15 units = **255 units/day**\n\n"
            "New workers:\n"
            "3 × (15 × 75%) = **33.75 units/day**\n\n"
            "Total expected output:\n"
            "255 + 33.75 = **288.75 units/day**\n\n"
            "If fully ramped:\n"
            "20 × 15 = **300 units/day**\n\n"
            "Ramp drag = **11.25 units/day** (3.75% total output loss)\n\n"
            "This explains some throughput loss but **not** a 4.3pp yield drop.\n\n"
            "**Conclusion:** Labor ramp is contributory, not primary driver."
        ),
    },
    {
        "type": "text",
        "content": (
            "\n---\n\n"
            "**B. OEE Decomposition – Primary Driver**\n\n"
            "OEE = Availability × Performance × Quality\n\n"
            "**From system data:**\n"
            "- Availability dropped from 90% → 84%\n"
            "- Performance dropped from 95% → 92%\n"
            "- Quality dropped from 98% → 95%\n\n"
            "New OEE: 0.84 × 0.92 × 0.95 = **73.4%**\n"
            "Previous OEE: 0.90 × 0.95 × 0.98 = **83.8%**\n\n"
            "That's a **10.4pp OEE deterioration**. The decline is primarily driven "
            "by reduced Availability and Quality. The magnitude of OEE loss "
            "significantly exceeds the labor ramp effect and aligns with observed "
            "yield and scrap increases."
        ),
    },
    {
        "type": "text",
        "content": (
            "\n---\n\n"
            "**C. Scrap Financial Impact – Economic Impact**\n\n"
            "**System Data:**\n"
            "- 300 units/day baseline\n"
            "- Contribution margin per unit: \\$120\n\n"
            "**Analysis:**\n"
            "- Scrap increase: (6.5% – 3.8%) × 300 = **8.1 additional scrap units/day**\n"
            "- Financial impact: 8.1 × \\$120 = **\\$972/day**\n"
            "- Annualized (250 days): **\\$243,000 impact**\n\n"
            "Scrap increase is economically material and consistent with the observed "
            "quality degradation within OEE."
        ),
    },
    {
        "type": "text",
        "content": (
            "\n---\n\n"
            "Please confirm whether you would like me to incorporate more variables "
            "into the next diagnostic view, or proceed with visualization focused on "
            "equipment-driven yield deterioration."
        ),
    },
]

STEP_2_BLOCKS = [
    {
        "type": "chart",
        "title": "1️⃣ OEE Waterfall (Week-over-Week)",
        "chart_type": "oee_waterfall",
        "commentary": (
            "**58%** of deterioration driven by availability loss\n\n"
            "**29%** driven by performance slowdown\n\n"
            "**13%** driven by quality decline\n\n"
            "**Confirms equipment instability as dominant driver**"
        ),
    },
    {
        "type": "chart",
        "title": "2️⃣ Constrained Asset Performance",
        "chart_type": "asset_performance",
        "commentary": (
            "Asset running near theoretical capacity\n\n"
            "Reliability has deteriorated materially\n\n"
            "Breakdown frequency increased ~4×\n\n"
            "**Clear constraint machine impacting system flow**"
        ),
    },
    {
        "type": "chart",
        "title": "3️⃣ Scrap & Margin Impact Trend",
        "chart_type": "scrap_trend",
        "commentary": (
            "**Approximate cumulative impact to date:** ≈ $32–38K realized in last 6 weeks"
        ),
    },
]

FALLBACK_BLOCKS = [
    {
        "type": "text",
        "content": "Thank you for the additional context. Let me analyze this further "
        "and get back to you with updated recommendations.",
    }
]


def get_response_blocks(step):
    if step == 0:
        return STEP_0_BLOCKS
    if step == 1:
        return STEP_1_BLOCKS
    if step == 2:
        return STEP_2_BLOCKS
    return FALLBACK_BLOCKS


# --- Thinking animation ---
THINKING_PHASES = {
    0: [
        ("Querying SAP + MES data...", 1.2),
        ("Analyzing yield trends...", 1.0),
        ("Cross-referencing equipment logs...", 0.8),
        ("Preparing diagnostic summary...", 0.6),
    ],
    1: [
        ("Retrieving operator headcount and new hire records...", 0.4),
        ("Calculating effective productivity for new vs experienced workers...", 0.35),
        ("Aggregating total expected output and ramp drag impact...", 0.3),
        ("Comparing projected labor output vs actual yield...", 0.3),
        ("Flagging labor contribution to yield deviation...", 0.25),
        ("Pulling line-level OEE metrics from MES logs...", 0.35),
        ("Decomposing Availability, Performance, and Quality components...", 0.3),
        ("Computing week-over-week OEE change...", 0.25),
        ("Evaluating relative impact of each OEE component on total output...", 0.3),
        ("Extracting daily scrap counts and defect categories...", 0.3),
        ("Calculating incremental units lost to scrap...", 0.25),
        ("Converting scrap units into financial impact based on contribution margin...", 0.3),
        ("Annualizing margin exposure from weekly scrap data...", 0.25),
        ("Prioritizing drivers by combined operational and economic impact...", 0.3),
        ("Preparing structured assessment summary for user confirmation...", 0.35),
    ],
}
THINKING_PHASES[2] = THINKING_PHASES[1]  # Reuse detailed phases for step 2


def show_thinking(step=0):
    """Display an animated thinking state before the response."""
    phases = THINKING_PHASES.get(step, THINKING_PHASES[0])
    with st.status("🔍 Analyzing system data...", expanded=True) as status:
        for label, duration in phases:
            st.write(label)
            time.sleep(duration)
        status.update(label="✅ Analysis complete", state="complete", expanded=False)
    time.sleep(0.3)


# --- Streaming helpers ---
def text_generator(text, speed=0.03):
    """Yield text word-by-word, batching table rows as one chunk."""
    lines = text.split("\n")
    i = 0
    while i < len(lines):
        if lines[i].strip().startswith("|"):
            # Render the entire table at once
            table = ""
            while i < len(lines) and lines[i].strip().startswith("|"):
                table += lines[i] + "\n"
                i += 1
            yield table
            time.sleep(0.4)
        else:
            line = lines[i]
            i += 1
            if line.strip():
                # Stream word-by-word for natural feel
                words = line.split(" ")
                for j, word in enumerate(words):
                    yield word + (" " if j < len(words) - 1 else "")
                    time.sleep(speed + random.uniform(0, 0.02))
                yield "\n"
            else:
                yield "\n"


def render_questions(items):
    """Render interactive Yes / No pill-buttons for each question."""
    for item in items:
        qid = item["id"]
        answer = st.session_state.answers.get(qid)

        cols = st.columns([5, 0.8, 0.8, 3.4])
        with cols[0]:
            st.markdown(f"&ensp;{item['text']}")
        with cols[1]:
            yes_type = "primary" if answer == "yes" else "secondary"
            yes_label = "✓ Yes" if answer == "yes" else "Yes"
            if st.button(yes_label, key=f"{qid}_yes", type=yes_type, use_container_width=True):
                st.session_state.answers[qid] = "yes"
                st.rerun()
        with cols[2]:
            no_type = "primary" if answer == "no" else "secondary"
            no_label = "✗ No" if answer == "no" else "No"
            if st.button(no_label, key=f"{qid}_no", type=no_type, use_container_width=True):
                st.session_state.answers[qid] = "no"
                st.rerun()


def render_chart_oee_waterfall():
    data = pd.DataFrame([
        {"label": "Previous OEE", "amount": 83.8, "type": "total"},
        {"label": "Availability", "amount": -6, "type": "delta"},
        {"label": "Performance", "amount": -3, "type": "delta"},
        {"label": "Quality", "amount": -1.4, "type": "delta"},
        {"label": "New OEE", "amount": 73.4, "type": "total"},
    ])
    
    # Pre-calculate start and end values for waterfall bars
    data["end"] = data["amount"].cumsum()
    data["start"] = data["end"].shift(1).fillna(0)
    
    # Adjust start/end for 'total' bars (they start at 0)
    data.loc[data["type"] == "total", "start"] = 0
    data.loc[data["type"] == "total", "end"] = data["amount"]
    
    # Logic for 'delta' bars: if amount is negative, start is higher than end
    # We need to ensure 'start' is the previous cumulative sum and 'end' is new cumulative sum.
    # Actually, simpler: just track the running total.
    # Previous: 0 -> 83.8
    # Avail: 83.8 -> 77.8
    # Perf: 77.8 -> 74.8
    # Qual: 74.8 -> 73.4
    # New: 0 -> 73.4
    
    # Correct calculation:
    running_total = 0
    starts = []
    ends = []
    for _, row in data.iterrows():
        if row["type"] == "total":
            starts.append(0)
            ends.append(row["amount"])
            running_total = row["amount"]
        else:
            starts.append(running_total)
            running_total += row["amount"]
            ends.append(running_total)
    
    data["start"] = starts
    data["end"] = ends
    data["color"] = data["type"].apply(lambda x: "#1f77b4" if x == "total" else "#ff7f0e")

    c = (
        alt.Chart(data)
        .mark_bar()
        .encode(
            x=alt.X("label", sort=None, title=None),
            y=alt.Y("start", title="OEE %"),
            y2="end",
            color=alt.Color("color", scale=None),
            tooltip=["label", "amount", "end"],
        )
        .properties(height=300)
    )
    st.altair_chart(c, use_container_width=True)


def render_chart_asset_performance():
    data = pd.DataFrame([
        {"metric": "Capacity Utilization", "value": 94, "unit": "%"},
        {"metric": "Downtime", "value": 18, "unit": "%"},
        {"metric": "MTBF", "value": 22, "unit": "hours"},
    ])
    
    c = (
        alt.Chart(data)
        .mark_bar()
        .encode(
            x=alt.X("metric", sort=None, title=None),
            y=alt.Y("value", title="Value"),
            color=alt.value("#1f77b4"),
            tooltip=["metric", "value", "unit"],
        )
        .properties(height=300)
    )
    st.altair_chart(c, use_container_width=True)


def render_chart_scrap_trend(key_prefix=""):
    # Toggle for duration
    view_option = st.radio(
        "Select duration:",
        ["6 Weeks", "8 Weeks"],
        horizontal=True,
        key=f"scrap_view_toggle_{key_prefix}",
    )
    
    weeks = 8 if view_option == "8 Weeks" else 6
    
    # Data
    data = pd.DataFrame({
        "Week": range(1, 9),
        "Scrap %": [3.8, 4.1, 4.4, 4.8, 5.7, 6.5, 6.2, 6.0],
        "Margin Loss": [0, 3600, 7200, 14400, 21600, 29700, 26400, 24000],
    })
    data = data[data["Week"] <= weeks]
    
    base = alt.Chart(data).encode(x="Week:O")

    line_scrap = base.mark_line(color="#ff7f0e").encode(
        y=alt.Y("Scrap %", title="Scrap %", axis=alt.Axis(titleColor="#ff7f0e")),
        tooltip=["Week", "Scrap %"]
    )
    
    line_margin = base.mark_line(color="#1f77b4", strokeDash=[5, 5]).encode(
        y=alt.Y("Margin Loss", title="Weekly Margin Loss ($)", axis=alt.Axis(titleColor="#1f77b4")),
        tooltip=["Week", "Margin Loss"]
    )
    
    # Baseline annotation (3.8%)
    rule = alt.Chart(pd.DataFrame({"y": [3.8]})).mark_rule(strokeDash=[2, 2], color="gray").encode(y="y")

    c = alt.layer(line_scrap, line_margin, rule).resolve_scale(y="independent").properties(height=350)
    
    st.altair_chart(c, use_container_width=True)


def render_blocks(blocks, streaming=False, step=0, key_prefix=""):
    """Render response blocks; stream text progressively when streaming=True."""
    if streaming:
        show_thinking(step)
    for block in blocks:
        if block["type"] == "text":
            if streaming:
                st.write_stream(text_generator(block["content"]))
            else:
                st.markdown(block["content"])
        elif block["type"] == "questions":
            if streaming:
                time.sleep(0.3)
            render_questions(block["items"])
        elif block["type"] == "chart":
            st.subheader(block["title"])
            if block["chart_type"] == "oee_waterfall":
                render_chart_oee_waterfall()
            elif block["chart_type"] == "asset_performance":
                render_chart_asset_performance()
            elif block["chart_type"] == "scrap_trend":
                render_chart_scrap_trend(key_prefix)

            if streaming:
                st.write_stream(text_generator(block["commentary"]))
            else:
                st.markdown(block["commentary"])
            st.divider()


# --- Display Messages ---
for i, msg in enumerate(st.session_state.messages):
    is_last = i == len(st.session_state.messages) - 1

    with st.chat_message(msg["role"]):
        if msg["role"] == "user":
            st.markdown(msg["content"])
        else:
            blocks = get_response_blocks(msg.get("step", 0))
            should_stream = is_last and not st.session_state.streaming_done
            if should_stream:
                st.session_state.streaming_done = True  # prevent re-stream on rerun
            render_blocks(blocks, streaming=should_stream, step=msg.get("step", 0), key_prefix=str(i))

# --- Chat Input ---
user_input = st.chat_input("Ask about yield performance...")

if user_input:
    current_step = st.session_state.step
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.messages.append({"role": "assistant", "step": current_step})
    st.session_state.step += 1
    st.session_state.streaming_done = False
    st.rerun()
