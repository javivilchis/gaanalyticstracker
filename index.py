import os
from dotenv import load_dotenv
import pandas as pd
import matplotlib.pyplot as plt
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange, Dimension, Metric, RunReportRequest, FilterExpression, Filter
)


load_dotenv()
PROPERTY_ID = os.getenv("GA4_PROPERTY_ID")
def get_final_report(property_id):
    client = BetaAnalyticsDataClient()
    
    tasks = [
        {"name": "Winter Savings Guide", "path": "/spark/ambit-energy-winter-savings-guide", "start": "2025-12-02", "end": "2026-03-03"},
        {"name": "Extreme Weather Guide", "path": "/spark/ambit-energys-extreme-weather-guide", "start": "2026-01-20", "end": "2026-01-28"}
    ]

    for task in tasks:
        # --- PART 1: DEVICE VISITS ---
        request = RunReportRequest(
            property=f"properties/{property_id}",
            dimensions=[Dimension(name="deviceCategory")],
            metrics=[Metric(name="sessions")],
            date_ranges=[DateRange(start_date=task['start'], end_date=task['end'])],
            dimension_filter=FilterExpression(filter=Filter(field_name="pagePath", string_filter=Filter.StringFilter(value=task['path'])))
        )
        response = client.run_report(request)
        df_device = pd.DataFrame([[r.dimension_values[0].value, int(r.metric_values[0].value)] for r in response.rows], columns=["Device", "Visits"])

        # --- PART 2: FLOW (EXITS) ---
        flow_req = RunReportRequest(
            property=f"properties/{property_id}",
            dimensions=[Dimension(name="pagePath")],
            metrics=[Metric(name="sessions")],
            date_ranges=[DateRange(start_date=task['start'], end_date=task['end'])],
            dimension_filter=FilterExpression(filter=Filter(field_name="pageReferrer", string_filter=Filter.StringFilter(match_type=Filter.StringFilter.MatchType.CONTAINS, value=task['path'])))
        )
        flow_res = client.run_report(flow_req)
        df_flow = pd.DataFrame([[r.dimension_values[0].value, r.metric_values[0].value] for r in flow_res.rows], columns=["Next Page", "Exits"])

        # --- SAVE CSV ---
        # Relative path (./) saves it in the same folder as this script
        base_filename = task['name'].replace(" ", "_").lower()
        csv_path = f"./reports/{base_filename}_report-new.csv"
        
        with open(csv_path, 'w') as f:
            f.write(f"Report for: {task['name']}\n")
            f.write(f"Date Range: {task['start']} to {task['end']}\n\n")
            f.write("DEVICE BREAKDOWN\n")
            df_device.to_csv(f, index=False)
            f.write("\nTOP EXIT DESTINATIONS\n")
            df_flow.to_csv(f, index=False)
        print(f"✅ Saved CSV: {csv_path}")

                # --- SAVE GRAPH ---
        if not df_device.empty:
            plt.figure(figsize=(10, 6))
            
            # Map specific colors to device types
            color_map = {
                'mobile': '#3498db',   # Blue
                'desktop': '#2ecc71',  # Green
                'tablet': '#e67e22'    # Orange
            }
            
            # Apply colors based on the 'Device' column (default to gray if not found)
            colors = [color_map.get(dev.lower(), '#95a5a6') for dev in df_device['Device']]
            
            bars = plt.bar(df_device['Device'], df_device['Visits'], color=colors)
            
            # Labels on top of bars
            plt.gca().bar_label(bars, padding=3, fontweight='bold') 
            
            # Dynamic Title with Name and Date Range
            plt.title(f"Traffic by Device: {task['name']}\nRange: {task['start']} to {task['end']}", 
                      fontsize=12, fontweight='bold', pad=20)
            
            plt.ylabel("Total Sessions")
            plt.xlabel("Device Type")
            
            # Adjust y-axis limit to ensure labels aren't cut off
            plt.gca().set_ylim(top=df_device['Visits'].max() * 1.15)
            
            plt.tight_layout()
            plt.savefig(f"./reports/{base_filename}_graph-new.png")
            plt.close()
            print(f"✅ Saved Colorized Graph: {base_filename}_graph-new.png")



if __name__ == '__main__':
    get_final_report(PROPERTY_ID)
  