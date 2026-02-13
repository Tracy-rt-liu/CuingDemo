import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time
import random

# --- Page Config ---
st.set_page_config(
    page_title="Manufacturing Yield Diagnostic",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Premium Custom CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=Outfit:wght@400;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #f8fafc;
    }

    h1, h2, h3 {
        font-family: 'Outfit', sans-serif;
        color: #f8fafc;
        font-weight: 700;
    }

    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border: 1px solid rgba(255, 255, 255, 0.1);
        background: rgba(255, 255, 255, 0.05);
        color: white;
    }

    .stButton>button:hover {
        background: rgba(255, 255, 255, 0.15);
        border-color: #38bdf8;
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.4);
        transform: translateY(-1px);
    }

    /* Selected Button Style */
    .stButton>button.active {
        background: #0ea5e9 !important;
        border-color: #38bdf8 !important;
        color: white !important;
    }

    .chat-bubble {
        background: rgba(255, 255, 255, 0.05);
        padding: 20px;
        border-radius: 12px;
        border-left: 4px solid #38bdf8;
        margin-bottom: 20px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
    }

    .thinking-log {
        font-family: 'Courier New', Courier, monospace;
        color: #94a3b8;
        font-size: 0.9rem;
        padding-left: 20px;
        border-left: 2px dashed rgba(255, 255, 255, 0.2);
        margin: 15px 0;
    }

    /* Scrollbar styling */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.1); border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(255, 255, 255, 0.2); }
</style>
""", unsafe_allow_html=True)

# --- Session State Initialization ---
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'answers' not in st.session_state:
    st.session_state.answers = {}

# --- Helper Functions ---
def stream_text(text, delay=0.03):
    placeholder = st.empty()
    full_text = ""
    for word in text.split(" "):
        full_text += word + " "
        placeholder.markdown(f'<div class="chat-bubble">{full_text}</div>', unsafe_allow_html=True)
        time.sleep(delay)

def run_thinking_log(logs, delay=0.5):
    log_container = st.empty()
    current_logs = ""
    for log in logs:
        current_logs += f"• {log}\n\n"
        log_container.markdown(f'<div class="thinking-log">{current_logs}</div>', unsafe_allow_html=True)
        time.sleep(delay)

# --- Main App Layout ---
st.title("🏭 Manufacturing Yield Diagnostic")
st.markdown("---")

# Container for the chat flow
chat_placeholder = st.container()

# --- Step 0: Initial User Input & Drivers Validation ---
if st.session_state.step >= 0:
    with chat_placeholder:
        st.markdown("**User:** I think yield dropped last week. Can you help me understand why?")
        
        st.markdown("""
        <div class="chat-bubble">
        To diagnose the yield decline, I’d like to validate four drivers:<br>
        • Labor ramp & productivity<br>
        • Equipment performance (OEE)<br>
        • Material quality<br>
        • Process bottlenecks / cycle time shifts
        </div>
        """, unsafe_allow_html=True)

        st.subheader("Driver Validation Questions")
        
        col1, col2 = st.columns(2)
        
        questions = [
            ("q1", "Is the 4-week ramp assumption accurate?"),
            ("q2", "Are the new hires assigned to the affected line?"),
            ("q3", "Has scrap increased on specific shifts?"),
            ("q4", "Have you experienced increased micro-stoppages?"),
            ("q5", "Any recent maintenance deferrals?")
        ]

        for i, (key, text) in enumerate(questions):
            with col1 if i % 2 == 0 else col2:
                st.write(f"**{text}**")
                btn_col1, btn_col2 = st.columns(2)
                
                # Use current answer to determine style (pseudo-highlighting for now)
                # Streamlit doesn't natively support easy "active" classes on buttons without re-run logic
                # So we store in state and show text confirmation
                
                if btn_col1.button("Yes", key=f"{key}_yes"):
                    st.session_state.answers[key] = "Yes"
                if btn_col2.button("No", key=f"{key}_no"):
                    st.session_state.answers[key] = "No"
                
                if key in st.session_state.answers:
                    st.markdown(f"Selected: **{st.session_state.answers[key]}**")

        if len(st.session_state.answers) >= 5:
            if st.button("Confirm Inputs and Run Initial Analysis"):
                st.session_state.step = 1
                st.rerun()

# --- Step 1: Thinking Log & Initial Assessment ---
if st.session_state.step >= 1:
    with chat_placeholder:
        st.markdown("---")
        # Only show animations once when transition happens
        # In a real app we might use a flag, for this demo we just render
        
        thinking_logs = [
            "Retrieving operator headcount and new hire records…",
            "Calculating effective productivity for new vs experienced workers…",
            "Aggregating total expected output and ramp drag impact…",
            "Comparing projected labor output vs actual yield…",
            "Flagging labor contribution to yield deviation…",
            "Pulling line-level OEE metrics from MES logs…",
            "Decomposing Availability, Performance, and Quality components…",
            "Computing week-over-week OEE change…",
            "Evaluating relative impact of each OEE component on total output…",
            "Extracting daily scrap counts and defect categories…",
            "Calculating incremental units lost to scrap…",
            "Converting scrap units into financial impact based on contribution margin…",
            "Annualizing margin exposure from weekly scrap data…",
            "Prioritizing drivers by combined operational and economic impact…",
            "Preparing structured assessment summary for user confirmation…"
        ]
        
        # We only run the logic if we just entered this step
        if 'step1_run' not in st.session_state:
            run_thinking_log(thinking_logs)
            st.session_state.step1_run = True
            
        assessment_text = (
            "Based on the inputs and data analysis, here is the initial assessment: \n\n"
            "**Labor Ramp Impact (Low to Moderate):** New hires are contributing to some variance, but not the primary cause.\n\n"
            "**OEE Decomposition (Primary Driver):** Equipment performance has dropped significantly (10.4pp), with availability being the main bottleneck.\n\n"
            "**Scrap Financial Impact:** Scrap rates have increased to 6.5%, leading to substantial margin loss."
        )
        
        # Word by word streaming
        if 'step1_assess_done' not in st.session_state:
            stream_text(assessment_text)
            st.session_state.step1_assess_done = True
        else:
            st.markdown(f'<div class="chat-bubble">{assessment_text}</div>', unsafe_allow_html=True)

        if st.button("Generate Interactive Diagnostic Charts"):
            st.session_state.step = 2
            st.rerun()

# --- Step 2: Diagnostic Charts ---
if st.session_state.step >= 2:
    with chat_placeholder:
        st.markdown("---")
        
        # Thinking log for chart preparation
        if 'step2_run' not in st.session_state:
            run_thinking_log([
                "Preparing OEE Waterfall…",
                "Loading constrained asset performance data…",
                "Compiling scrap & margin trend…"
            ])
            st.session_state.step2_run = True

        st.header("Interactive Diagnostic Assessment")

        # Layout for charts
        col1, col2 = st.columns(2)

        # a) OEE Waterfall
        with col1:
            st.subheader("OEE Waterfall")
            fig_waterfall = go.Figure(go.Waterfall(
                name = "OEE", orientation = "v",
                measure = ["absolute", "relative", "relative", "relative", "total"],
                x = ["Previous OEE", "Availability", "Performance", "Quality", "New OEE"],
                textposition = "outside",
                text = ["83.8%", "-6%", "-3%", "-1.4%", "73.4%"],
                y = [83.8, -6, -3, -1.4, 0],
                connector = {"line":{"color":"rgba(255, 255, 255, 0.3)"}},
                increasing = {"marker":{"color":"#10b981"}},
                decreasing = {"marker":{"color":"#ef4444"}},
                totals = {"marker":{"color":"#0ea5e9"}}
            ))
            fig_waterfall.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color="white",
                margin=dict(l=20, r=20, t=20, b=20),
                height=400
            )
            st.plotly_chart(fig_waterfall, use_container_width=True)
            
            st.info("""
            **Key Insights:**
            - 58% driven by availability loss
            - 29% driven by performance slowdown
            - 13% driven by quality decline
            - Dominant driver: **Equipment Instability**
            """)

        # b) Constrained Asset Performance
        with col2:
            st.subheader("Constrained Asset Performance")
            asset_data = {
                "Metric": ["Capacity Utilization", "Downtime", "MTBF (hrs)"],
                "Value": [94, 18, 22]
            }
            fig_bar = go.Figure(go.Bar(
                x=asset_data["Metric"],
                y=asset_data["Value"],
                marker_color=['#6366f1', '#f43f5e', '#fde047'],
                text=[f"{v}%" if i < 2 else f"{v}h" for i, v in enumerate(asset_data["Value"])],
                textposition='auto',
            ))
            fig_bar.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color="white",
                margin=dict(l=20, r=20, t=20, b=20),
                height=400,
                yaxis_title="Percentage / Hours"
            )
            st.plotly_chart(fig_bar, use_container_width=True)
            
            st.warning("""
            **Asset Analysis (Line 3):**
            - Running near theoretical capacity (94%)
            - Reliability has deteriorated materially
            - Breakdown frequency increased ~4×
            - **Critical bottleneck detected**
            """)

        st.markdown("---")

        # c) Scrap & Margin Impact Trend
        st.subheader("Scrap & Margin Impact Trend")
        
        # User input for weeks
        num_weeks = st.number_input("Adjust Analysis Horizon (Weeks)", min_value=1, max_value=8, value=6, step=1)
        
        # Data
        weeks_data = list(range(1, 9))
        scrap_data = [3.8, 4.1, 4.4, 4.8, 5.7, 6.5, 6.2, 6.0]
        margin_loss = [0, 3600, 7200, 14400, 21600, 29700, 26400, 24000]
        
        # Slice based on user input
        df_trend = pd.DataFrame({
            "Week": weeks_data[:num_weeks],
            "Scrap %": scrap_data[:num_weeks],
            "Margin Loss ($)": margin_loss[:num_weeks]
        })

        fig_trend = go.Figure()

        # Left Axis: Scrap %
        fig_trend.add_trace(go.Scatter(
            x=df_trend["Week"], y=df_trend["Scrap %"],
            name="Scrap %",
            line=dict(color='#fbbf24', width=4),
            mode='lines+markers'
        ))

        # Right Axis: Margin Loss
        fig_trend.add_trace(go.Scatter(
            x=df_trend["Week"], y=df_trend["Margin Loss ($)"],
            name="Weekly Margin Loss ($)",
            line=dict(color='#ef4444', width=4, dash='dot'),
            mode='lines+markers',
            yaxis="y2"
        ))

        fig_trend.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color="white",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            yaxis=dict(title="Scrap %", side="left", gridcolor="rgba(255,255,255,0.1)"),
            yaxis2=dict(title="Margin Loss ($)", side="right", overlaying="y", gridcolor="rgba(255,255,255,0.05)"),
            xaxis=dict(title="Weeks", gridcolor="rgba(255,255,255,0.1)"),
            margin=dict(l=20, r=20, t=50, b=20),
            height=500
        )
        
        # Annotation for the latest point
        current_scrap = df_trend["Scrap %"].iloc[-1]
        baseline_scrap = 3.8
        scrap_increase = round(current_scrap - baseline_scrap, 1)
        
        fig_trend.add_annotation(
            x=df_trend["Week"].iloc[-1], y=current_scrap,
            text=f"+{scrap_increase}pp increase",
            showarrow=True, arrowhead=2, bgcolor="#ef4444", font=dict(color="white")
        )

        st.plotly_chart(fig_trend, use_container_width=True)
        
        st.markdown(f"""
        <div class="chat-bubble" style="border-left-color: #fbbf24;">
        Current scrap at {current_scrap}% vs 3.8% baseline.<br>
        <b>Callout:</b> +{scrap_increase}pp scrap increase = <b>$243K annualized margin impact</b>.<br>
        Approximate cumulative loss over {num_weeks} weeks: <b>${sum(df_trend["Margin Loss ($)"]):,.0f}</b>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        
        # Final Download Step
        st.subheader("Final Synthesis")
        
        summary_text = f"""EXECUTIVE SUMMARY

1. OEE deterioration of 10.4pp driven primarily by availability loss.
2. Line 3 identified as primary constraint asset.
3. Scrap increase of {scrap_increase}pp = ~$243K annualized exposure.

Recommended Actions:
Immediate: Maintenance audit on Line 3.
Near-term: Daily OEE dashboard.
Structural: CapEx refurbishment case.
"""

        if st.download_button(
            label="Download Executive Summary",
            data=summary_text,
            file_name="Yield_Diagnostic_Summary.txt",
            mime="text/plain"
        ):
            st.success("Download started! Demo concluded.")
            st.balloons()
