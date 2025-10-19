import streamlit as st
import pandas as pd
from io import StringIO
from datetime import datetime
from core.utils import require_authentication
from core.wearable_store import (
    load_user_wearables,
    save_user_wearables,
    set_consent,
    append_records,
    set_provider_connection,
    clear_user_wearables,
    set_goals,
)

# --- Page Configuration ---
st.set_page_config(
    page_title="Wearables & Physiology",
    page_icon="⌚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Authentication ---
if not st.session_state.get("authenticated"):
    st.warning("Please log in to access this page.")
    st.stop()

require_authentication()

# --- Load User Data ---
email = st.session_state.user_profile.get("email")
if not email:
    st.error("User email not found. Please re-login.")
    st.stop()

user_data = load_user_wearables(email)

# --- Page Title ---
st.title("⌚ Wearables & Physiology")
st.markdown("Connect your wearables to track physiological data like heart rate, sleep, and activity. Gain insights into how your body responds to your mental state.")

# --- Consent & Privacy ---
with st.expander("🔒 Consent & Privacy", expanded=not user_data.get("consent", False)):
    st.markdown("""
    **Your data privacy is our priority.**
    - **Passive Data Collection:** We only collect data from your wearable provider after you grant explicit consent.
    - **Full Control:** You can revoke consent at any time. This will stop data syncing, and you can permanently delete all stored data.
    - **Data We Store:** We store timestamps, Heart Rate Variability (HRV), resting heart rate, sleep duration and efficiency, steps, and active minutes.
    - **Not Medical Advice:** This tool is for informational purposes only. Please consult a healthcare professional for any clinical concerns.
    """)
    consent_given = user_data.get("consent", False)
    consented = st.checkbox("I consent to the passive collection of my wearable data.", value=consent_given)
    if consented != consent_given:
        user_data = set_consent(email, consented)
        if consented:
            st.success("Thank you for your consent! You can now connect your providers.")
        else:
            st.warning("Consent revoked. Data syncing will be disabled.")
        st.rerun()

# --- Main Content Area ---
if user_data.get("consent"):
    col1, col2 = st.columns((1, 1))

    # --- Provider Connection ---
    with col1:
        st.subheader("🔗 Connect Providers")
        st.caption("Connect your wearable devices to automatically sync your data.")

        providers = {
            "Fitbit": "fitbit",
            "Google Fit": "google_fit",
            "Oura": "oura"
        }

        for provider_name, provider_key in providers.items():
            is_connected = user_data.get("providers", {}).get(provider_key, {}).get("connected", False)
            button_text = f"Disconnect {provider_name}" if is_connected else f"Connect {provider_name}"
            button_type = "secondary" if is_connected else "primary"
            if st.button(button_text, key=provider_key, use_container_width=True, type=button_type):
                user_data = set_provider_connection(email, provider_key, not is_connected)
                st.rerun()

    # --- Manual Data Import ---
    with col2:
        st.subheader("📄 Import CSV")
        st.caption("Manually upload a CSV file with your wearable data.")
        
        uploaded = st.file_uploader(
            "Upload a CSV file",
            type=["csv"],
            help="The CSV should have columns: timestamp, hrv_ms, resting_hr, sleep_minutes, sleep_efficiency, steps, active_minutes"
        )
        
        if uploaded:
            try:
                df = pd.read_csv(uploaded)
                colmap = {c.lower().strip().replace("_", ""): c for c in df.columns}
                
                if "timestamp" not in colmap:
                    st.error("CSV must include a 'timestamp' column.")
                else:
                    records = []
                    for _, row in df.iterrows():
                        rec = {
                            "timestamp": row[colmap["timestamp"]],
                            "hrv_ms": row.get(colmap.get("hrvms")),
                            "resting_hr": row.get(colmap.get("restinghr")),
                            "sleep_minutes": row.get(colmap.get("sleepminutes")),
                            "sleep_efficiency": row.get(colmap.get("sleepefficiency")),
                            "steps": row.get(colmap.get("steps")),
                            "active_minutes": row.get(colmap.get("activeminutes")),
                        }
                        records.append(rec)
                    
                    provider_guess = st.selectbox("Select the provider for this import:", ["fitbit", "google_fit", "oura", "unknown"])
                    if st.button("Import Data", use_container_width=True):
                        user_data = append_records(email, records, provider_guess)
                        st.success(f"Successfully imported {len(records)} records!")
            except Exception as e:
                st.error(f"Failed to parse CSV: {e}")

    st.divider()

    # --- Data Display and Summaries ---
    st.subheader("📊 Recent Records & Summaries")
    records = user_data.get("records", [])

    if not records:
        st.info("No wearable records found. Connect a provider or upload a CSV to get started.")
    else:
        df_view = pd.DataFrame(sorted(records, key=lambda r: r.get("timestamp", ""), reverse=True))
        df_view["ts"] = pd.to_datetime(df_view["timestamp"], errors="coerce")
        df_view = df_view.dropna(subset=["ts"]) # Ensure no NaT timestamps

        # --- Today's Goal Progress ---
        st.markdown("##### 🏆 Today's Goal Progress")
        goals = user_data.get("goals", {})
        if not goals:
            st.caption("You haven't set any goals yet. Set them in the 'Set Your Daily Goals' section below.")
        else:
            today_df = df_view[df_view["ts"].dt.date == datetime.utcnow().date()]
            if today_df.empty:
                st.info("No data recorded for today yet to track goal progress.")
            else:
                today_latest = today_df.iloc[0]
                goal_metrics_defined = [m for m in goals.keys() if m in today_latest]
                
                if not goal_metrics_defined:
                    st.caption("Set goals for available metrics (e.g., steps, sleep) to see progress.")
                else:
                    goal_cols = st.columns(len(goal_metrics_defined))
                    i = 0
                    for metric in goal_metrics_defined:
                        with goal_cols[i]:
                            goal_data = goals[metric]
                            target = goal_data.get("target", 0)
                            current_value = today_latest.get(metric, 0)
                            
                            st.markdown(f"**{metric.replace('_', ' ').title()}**")
                            progress = min(current_value / target, 1.0) if target > 0 else 0
                            
                            st.progress(progress, text=f"{int(current_value)} / {int(target)}")
                            if progress >= 1.0:
                                st.write("🎉 Goal Met!")
                        i += 1
        
        st.divider()

        # --- Summaries (Last 7 Days) ---
        st.markdown("##### Last 7 Days at a Glance")
        cutoff = pd.Timestamp.utcnow().tz_localize(None) - pd.Timedelta(days=7)
        last7 = df_view[df_view["ts"] >= cutoff]

        if last7.empty:
            st.info("No data recorded in the last 7 days.")
        else:
            summary_cols = st.columns(4)
            metrics = {
                "Avg HRV (ms)": ("hrv_ms", "mean"),
                "Avg Resting HR": ("resting_hr", "mean"),
                "Total Sleep (hrs)": ("sleep_minutes", "sum"),
                "Total Steps": ("steps", "sum")
            }
            
            for i, (label, (col, agg)) in enumerate(metrics.items()):
                with summary_cols[i]:
                    if col in last7.columns:
                        series = last7[col].dropna().astype(float)
                        if not series.empty:
                            value = series.agg(agg)
                            if "sleep" in label:
                                value /= 60
                            st.metric(label, f"{value:.1f}")
                        else:
                            st.metric(label, "N/A")
                    else:
                        st.metric(label, "N/A")

        # --- Weekly Insights ---
        st.markdown("##### 💡 Weekly Insights")
        
        cutoff_14_days = pd.Timestamp.utcnow().tz_localize(None) - pd.Timedelta(days=14)
        last_14_days_df = df_view[df_view["ts"] >= cutoff_14_days]

        insights = []

        def generate_weekly_insight(df, metric, name, higher_is_better=True):
            w1_start = pd.Timestamp.utcnow().tz_localize(None) - pd.Timedelta(days=7)
            w2_start = pd.Timestamp.utcnow().tz_localize(None) - pd.Timedelta(days=14)
            
            week1_df = df[df["ts"] >= w1_start]
            week2_df = df[(df["ts"] >= w2_start) & (df["ts"] < w1_start)]

            if week1_df.empty or week2_df.empty or metric not in df.columns:
                return None

            avg_w1 = week1_df[metric].mean()
            avg_w2 = week2_df[metric].mean()

            if pd.isna(avg_w1) or pd.isna(avg_w2) or avg_w2 == 0:
                return None

            percent_change = ((avg_w1 - avg_w2) / avg_w2) * 100

            if abs(percent_change) < 5:
                return None

            if percent_change > 0:
                direction = "higher"
                emoji = "📈" if higher_is_better else "📉"
                remark = "Keep it up!" if higher_is_better else "You might want to look into this."
            else:
                direction = "lower"
                emoji = "📉" if higher_is_better else "📈"
                remark = "You might want to look into this." if higher_is_better else "Great improvement!"

            return f"Your average **{name}** this week was **{abs(percent_change):.0f}% {direction}** than last week. {remark} {emoji}"

        insight_metrics = {
            "steps": {"name": "Daily Steps", "higher_is_better": True},
            "sleep_minutes": {"name": "Sleep Duration", "higher_is_better": True},
            "resting_hr": {"name": "Resting Heart Rate", "higher_is_better": False},
            "hrv_ms": {"name": "Heart Rate Variability (HRV)", "higher_is_better": True},
        }

        for key, props in insight_metrics.items():
            insight = generate_weekly_insight(last_14_days_df, key, props["name"], props["higher_is_better"])
            if insight:
                insights.append(insight)

        if not insights:
            st.caption("Not enough data to generate weekly insights. Keep tracking for at least two weeks!")
        else:
            for insight in insights:
                st.info(insight)
        
        st.divider()

        # --- Interactive Visualization ---
        st.subheader("📈 Visualize Your Data")

        min_date = df_view["ts"].min().date()
        max_date = df_view["ts"].max().date()
        default_start = max(min_date, max_date - pd.Timedelta(days=29))

        date_range = st.date_input(
            "Select a date range to visualize:",
            value=(default_start, max_date),
            min_value=min_date,
            max_value=max_date,
            key="wearable_date_range"
        )

        if len(date_range) == 2:
            start_date, end_date = date_range
            start_ts = pd.to_datetime(start_date)
            end_ts = pd.to_datetime(end_date) + pd.Timedelta(days=1)

            df_filtered = df_view[(df_view["ts"] >= start_ts) & (df_view["ts"] < end_ts)]

            if df_filtered.empty:
                st.info("No data available for the selected date range.")
            else:
                df_chart = df_filtered.set_index("ts")

                st.markdown("##### ❤️ Heart Rate & HRV")
                hr_cols = ["resting_hr", "hrv_ms"]
                if all(c in df_chart.columns for c in hr_cols):
                    hr_data = df_chart[hr_cols].dropna(how='all')
                    if not hr_data.empty:
                        st.line_chart(hr_data)
                    else:
                        st.caption("No Heart Rate or HRV data in this period.")
                else:
                    st.caption("Heart Rate or HRV data not available.")

                st.markdown("##### 😴 Sleep")
                sleep_cols = ["sleep_minutes", "sleep_efficiency"]
                if all(c in df_chart.columns for c in sleep_cols):
                    sleep_data = df_chart[sleep_cols].dropna(how='all')
                    if not sleep_data.empty:
                        st.line_chart(sleep_data)
                    else:
                        st.caption("No Sleep data in this period.")
                else:
                    st.caption("Sleep data not available.")

                st.markdown("##### 🏃 Activity")
                activity_cols = ["steps", "active_minutes"]
                if all(c in df_chart.columns for c in activity_cols):
                    activity_data = df_chart[activity_cols].dropna(how='all')
                    if not activity_data.empty:
                        st.line_chart(activity_data)
                    else:
                        st.caption("No Activity data in this period.")
                else:
                    st.caption("Activity data not available.")
        
        st.divider()

        # --- Detailed Records ---
        st.markdown("##### All Recorded Data")
        st.dataframe(df_view.drop(columns=["ts"]), use_container_width=True, hide_index=True)

    # --- Goal Setting ---
    with st.expander("🎯 Set Your Daily Goals"):
        current_goals = user_data.get("goals", {})
        goal_metrics = {
            "steps": "Daily Steps",
            "sleep_minutes": "Daily Sleep (minutes)",
            "active_minutes": "Daily Active Minutes"
        }
        new_goals = {}
        for key, label in goal_metrics.items():
            target = st.number_input(
                label, 
                min_value=0, 
                value=int(current_goals.get(key, {}).get("target", 0)),
                step=100 if key == "steps" else 15,
                key=f"goal_{key}"
            )
            if target > 0:
                new_goals[key] = {"target": target, "frequency": "daily"}

        if st.button("Save Goals"):
            user_data = set_goals(email, new_goals)
            st.success("Your goals have been saved!")
            st.rerun()

    # --- Data Controls ---
    st.divider()
    st.subheader("⚙️ Data Controls")
    st.warning("This action is irreversible and will permanently delete all your stored wearable data.")
    if st.button("Delete All Wearable Data", type="primary", use_container_width=True):
        clear_user_wearables(email)
        st.success("All your wearable data has been successfully deleted.")
        st.rerun()

else:
    st.info("Please provide consent above to begin connecting your wearable devices and tracking your physiological data.")