# Interactive Manufacturing Yield Diagnostic Demo – Cursor Instructions

## Overview
This project builds a **real-time, interactive demo** for a manufacturing yield diagnostic agent.  
Features include:

- Chat interface with user inputs
- Animated “thinking log”
- Interactive charts:
  - OEE Waterfall
  - Constrained Asset Performance
  - Scrap & Margin Trend with 6→8 week toggle
- Clickable Yes/No buttons for user confirmation
- Downloadable executive summary

---

## Step 1 – Project Setup
1. Create projeect and select **Python / Streamlit** as the environment.

---

## Step 2 – Define Chat Flow

1. **Step 0 – Initial User Input**
    - Prompt: `"I think yield dropped last week. Can you help me understand why?"`
    - Agent responds:
      ```
      To diagnose the yield decline, I’d like to validate four drivers:
      • Labor ramp & productivity
      • Equipment performance (OEE)
      • Material quality
      • Process bottlenecks / cycle time shifts
      ```
    - Show **Yes/No buttons** for the following:
      - Is the 4-week ramp assumption accurate?
      - Are the new hires assigned to the affected line?
      - Has scrap increased on specific shifts?
      - Have you experienced increased micro-stoppages?
      - Any recent maintenance deferrals?
    - Clicking a button should **store the user input** and **highlight the selection**.

2. **Step 1 – Second User Input**
    - After Yes/No inputs, display **animated thinking log**:
      ```
      Retrieving operator headcount and new hire records…
      Calculating effective productivity for new vs experienced workers…
      Aggregating total expected output and ramp drag impact…
      Comparing projected labor output vs actual yield…
      Flagging labor contribution to yield deviation…
      Pulling line-level OEE metrics from MES logs…
      Decomposing Availability, Performance, and Quality components…
      Computing week-over-week OEE change…
      Evaluating relative impact of each OEE component on total output…
      Extracting daily scrap counts and defect categories…
      Calculating incremental units lost to scrap…
      Converting scrap units into financial impact based on contribution margin…
      Annualizing margin exposure from weekly scrap data…
      Prioritizing drivers by combined operational and economic impact…
      Preparing structured assessment summary for user confirmation…
      ```
    - After the thinking log, display **word-by-word output** with the full assessment:
      - Labor Ramp Impact (Low to Moderate)
      - OEE Decomposition (Primary Driver)
      - Scrap Financial Impact

---

## Step 3 – Third User Input (Interactive Charts)

1. Animate **thinking log** (optional) for chart preparation:
    ```
    Preparing OEE Waterfall…
    Loading constrained asset performance data…
    Compiling scrap & margin trend…
    ```
2. Display **three interactive charts**:

   ### a) OEE Waterfall
   - Chart Type: Waterfall
   - Data:
     | Component     | Change (%) |
     |---------------|------------|
     | Previous OEE  | 83.8       |
     | Availability  | -6         |
     | Performance   | -3         |
     | Quality       | -1.4       |
     | New OEE       | 73.4       |
   - Commentary:
     - 58% of deterioration driven by availability loss
     - 29% driven by performance slowdown
     - 13% driven by quality decline
     - Confirms equipment instability as dominant driver

   ### b) Constrained Asset Performance
   - Chart Type: Bar
   - Data:
     | Metric             | Value (%) |
     |-------------------|-----------|
     | Capacity Utilization | 94        |
     | Downtime            | 18        |
     | MTBF (hrs)          | 22        |
   - Commentary:
     - Asset running near theoretical capacity
     - Reliability has deteriorated materially
     - Breakdown frequency increased ~4×
     - Clear constraint machine impacting system flow

   ### c) Scrap & Margin Impact Trend
   - Chart Type: Line
   - X-axis: Weeks
   - Left Y-axis: Scrap %
   - Right Y-axis: Weekly Margin Loss ($)
   - Data (6 weeks):
     | Week | Scrap % | Weekly Margin Loss ($) |
     |------|---------|-----------------------|
     | 1    | 3.8     | 0                     |
     | 2    | 4.1     | 3,600                 |
     | 3    | 4.4     | 7,200                 |
     | 4    | 4.8     | 14,400                |
     | 5    | 5.7     | 21,600                |
     | 6    | 6.5     | 29,700                |
   - Optional 8-week view for toggle:
     | 7    | 6.2     | 26,400                |
     | 8    | 6.0     | 24,000                |
   - Overlay & Annotations:
     - Baseline scrap = 3.8%
     - Current scrap = 6.5%
     - Callout: +2.7pp scrap increase = $243K annualized margin impact
   - Commentary:
     - Approximate cumulative impact: ≈ $32–38K realized over 6 weeks
   - User can toggle **6→8 weeks** dynamically

---

## Step 4 – Downloadable Executive Summary

- After charts are displayed, provide **download button**:
  - File: `Yield_Diagnostic_Summary.txt`
  - Content:
    ```
    EXECUTIVE SUMMARY

    1. OEE deterioration of 10.4pp driven primarily by availability loss.
    2. Line 3 identified as primary constraint asset.
    3. Scrap increase of 2.7pp = ~$243K annualized exposure.

    Recommended Actions:
    Immediate: Maintenance audit on Line 3.
    Near-term: Daily OEE dashboard.
    Structural: CapEx refurbishment case.
    ```

---

## Step 5 – Styling & Interactivity

1. Ensure **all text appears progressively**:
   - Word-by-word for assessment
   - Line-by-line for thinking logs
2. Yes/No buttons should:
   - Highlight when clicked
   - Store the selection
3. Charts should be **interactive**:
   - Hover tooltips
   - Toggle 6→8 week view for scrap trend
   - Highlight selected bars or points

---

## Step 6 – Run Demo

1. Click **Run** in Cursor.
2. Test full interaction:
   - Input 1 → Yes/No buttons → Step 2 output
   - Input 2 → Thinking log → Word-by-word assessment
   - Input 3 → Interactive charts → Toggle weeks
   - Download executive summary
3. Confirm all elements render in **one window**, real-time.

---

## Notes

- No external files are needed; charts use **demo data provided above**.  
- All actions happen **online in the browser**.  
- Optional enhancements:
  - Monte Carlo simulation button  
  - Sensitivity analysis panel  
  - Additional KPI overlays on charts  

---

