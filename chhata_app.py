import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import json

# --- 1. COMPREHENSIVE MASTER DATA ---
MASTER_DATA = {
    "Angul": {"Rainfall": {"2022": 1160.6, "2023": 1424.1, "2024": 1324.3, "2025": 1324.3}, "Urban": {"Anugul": {"2022-23": {"Govt": 2.0, "Pvt": 99.0}, "2023-24": {"Govt": 3.0, "Pvt": 59.0}, "2024-25": {"Govt": 15.0, "Pvt": 266.0}, "2025-26": {"Govt": 10.0, "Pvt": 136.0}}, "Talcher": {"2022-23": {"Govt": 2.0, "Pvt": 80.0}, "2023-24": {"Govt": 5.0, "Pvt": 214.0}, "2024-25": {"Govt": 15.0, "Pvt": 86.0}, "2025-26": {"Govt": 0.0, "Pvt": 6.0}}}, "Rural": {"Talcher": {"2022-23": {"Govt": 0.0}, "2023-24": {"Govt": 12.0}, "2024-25": {"Govt": 3.0}, "2025-26": {"Govt": 5.0}}, "Kaniha": {"2022-23": {"Govt": 4.0}, "2023-24": {"Govt": 9.0}, "2024-25": {"Govt": 0.0}, "2025-26": {"Govt": 6.0}}}, "ARUA": {"Talcher": {"2022-23": {"Ponds": 8.0}, "2023-24": {"Ponds": 10.0}, "2024-25": {"Ponds": 12.0}, "2025-26": {"Ponds": 2.0}}}},
    "Balasore": {"Rainfall": {"2022": 1482.7, "2023": 1471.9, "2024": 1366.9, "2025": 1366.9}, "Urban": {}, "Rural": {"Remuna": {"2022-23": {"Govt": 0.0}, "2023-24": {"Govt": 10.0}, "2024-25": {"Govt": 5.0}, "2025-26": {"Govt": 0.0}}, "Nilagiri": {"2022-23": {"Govt": 0.0}, "2023-24": {"Govt": 13.0}, "2024-25": {"Govt": 5.0}, "2025-26": {"Govt": 5.0}}, "Jaleswar": {"2022-23": {"Govt": 0.0}, "2023-24": {"Govt": 14.0}, "2024-25": {"Govt": 4.0}, "2025-26": {"Govt": 5.0}}, "Baliapal": {"2022-23": {"Govt": 0.0}, "2023-24": {"Govt": 8.0}, "2024-25": {"Govt": 7.0}, "2025-26": {"Govt": 3.0}}, "Bahananga": {"2022-23": {"Govt": 0.0}, "2023-24": {"Govt": 8.0}, "2024-25": {"Govt": 7.0}, "2025-26": {"Govt": 0.0}}}, "ARUA": {"Bahanaga": {"2022-23": {"Ponds": 8.0}, "2023-24": {"Ponds": 8.0}, "2024-25": {"Ponds": 8.0}, "2025-26": {"Ponds": 0.0}}, "Remuna": {"2022-23": {"Ponds": 8.0}, "2023-24": {"Ponds": 8.0}, "2024-25": {"Ponds": 8.0}, "2025-26": {"Ponds": 0.0}}, "Baliapal": {"2022-23": {"Ponds": 52.0}, "2023-24": {"Ponds": 52.0}, "2024-25": {"Ponds": 52.0}, "2025-26": {"Ponds": 38.0}}}},
    "Bargarh": {"Rainfall": {"2022": 1268.1, "2023": 1455.1, "2024": 1237.1, "2025": 1237.1}, "Urban": {"Bargarh": {"2022-23": {"Govt": 2.0, "Pvt": 18.0}, "2023-24": {"Govt": 4.0, "Pvt": 298.0}, "2024-25": {"Govt": 3.0, "Pvt": 100.0}, "2025-26": {"Govt": 3.0, "Pvt": 143.0}}, "Padmapur": {"2022-23": {"Govt": 1.0, "Pvt": 27.0}, "2023-24": {"Govt": 0.0, "Pvt": 106.0}, "2024-25": {"Govt": 2.0, "Pvt": 181.0}, "2025-26": {"Govt": 5.0, "Pvt": 210.0}}}, "Rural": {"Bhatali": {"2022-23": {"Govt": 3.0}, "2023-24": {"Govt": 0.0}, "2024-25": {"Govt": 9.0}, "2025-26": {"Govt": 4.0}}, "Baragarh": {"2022-23": {"Govt": 5.0}, "2023-24": {"Govt": 5.0}, "2024-25": {"Govt": 0.0}, "2025-26": {"Govt": 5.0}}}, "ARUA": {"Bargarh": {"2022-23": {"Ponds": 8.0}, "2023-24": {"Ponds": 0.0}, "2024-25": {"Ponds": 17.0}, "2025-26": {"Ponds": 7.0}}}},
    "Cuttack": {"Rainfall": {"2022": 1496.9, "2023": 1335.0, "2024": 1598.4, "2025": 1598.4}, "Urban": {"Cuttack": {"2022-23": {"Govt": 3.0, "Pvt": 374.0}, "2023-24": {"Govt": 5.0, "Pvt": 325.0}, "2024-25": {"Govt": 12.0, "Pvt": 435.0}, "2025-26": {"Govt": 8.0, "Pvt": 148.0}}}, "Rural": {"Cuttack Sadar": {"2022-23": {"Govt": 20.0}, "2023-24": {"Govt": 0.0}, "2024-25": {"Govt": 0.0}, "2025-26": {"Govt": 7.0}}}, "ARUA": {"Cuttack sadar": {"2022-23": {"Ponds": 0.0}, "2023-24": {"Ponds": 18.0}, "2024-25": {"Ponds": 0.0}, "2025-26": {"Ponds": 14.0}}}},
    "Khordha": {"Rainfall": {"2022": 1407.2, "2023": 1218.0, "2024": 1403.4, "2025": 1403.4}, "Urban": {"Bhubaneswar": {"2022-23": {"Govt": 5.0, "Pvt": 896.0}, "2023-24": {"Govt": 5.0, "Pvt": 1213.0}, "2024-25": {"Govt": 51.0, "Pvt": 828.0}, "2025-26": {"Govt": 0.0, "Pvt": 1023.0}}, "Khurda": {"2022-23": {"Govt": 3.0, "Pvt": 98.0}, "2023-24": {"Govt": 10.0, "Pvt": 351.0}, "2024-25": {"Govt": 10.0, "Pvt": 221.0}, "2025-26": {"Govt": 7.0, "Pvt": 93.0}}}, "Rural": {"Bolagarh": {"2022-23": {"Govt": 4.0}, "2023-24": {"Govt": 10.0}, "2024-25": {"Govt": 5.0}, "2025-26": {"Govt": 2.0}}, "Balipatna": {"2022-23": {"Govt": 7.0}, "2023-24": {"Govt": 2.0}, "2024-25": {"Govt": 10.0}, "2025-26": {"Govt": 0.0}}}, "ARUA": {"Bhubaneswar": {"2022-23": {"Ponds": 48.0}, "2023-24": {"Ponds": 30.0}, "2024-25": {"Ponds": 66.0}, "2025-26": {"Ponds": 48.0}}, "Bolagarh": {"2022-23": {"Ponds": 42.0}, "2023-24": {"Ponds": 51.0}, "2024-25": {"Ponds": 51.0}, "2025-26": {"Ponds": 48.0}}}},
    "Puri": {"Rainfall": {"2022": 1199.2, "2023": 993.7, "2024": 1155.3, "2025": 1155.3}, "Urban": {"Puri": {"2022-23": {"Govt": 3.0, "Pvt": 180.0}, "2023-24": {"Govt": 10.0, "Pvt": 347.0}, "2024-25": {"Govt": 5.0, "Pvt": 178.0}, "2025-26": {"Govt": 8.0, "Pvt": 284.0}}}, "Rural": {"Kakatapur": {"2022-23": {"Govt": 5.0}, "2023-24": {"Govt": 6.0}, "2024-25": {"Govt": 4.0}, "2025-26": {"Govt": 2.0}}}, "ARUA": {"Kakatpur": {"2022-23": {"Ponds": 7.0}, "2023-24": {"Ponds": 7.0}, "2024-25": {"Ponds": 7.0}, "2025-26": {"Ponds": 7.0}}}},
    "Bhadrak": {"Rainfall": {"2022": 1222.3, "2023": 1370.2, "2024": 1254.2, "2025": 1254.2}, "Urban": {}, "Rural": {"Dhamanagar": {"2022-23": {"Govt": 0.0}, "2023-24": {"Govt": 8.0}, "2024-25": {"Govt": 5.0}, "2025-26": {"Govt": 4.0}}, "Bhadrak": {"2022-23": {"Govt": 0.0}, "2023-24": {"Govt": 13.0}, "2024-25": {"Govt": 4.0}, "2025-26": {"Govt": 6.0}}, "Bhandaripokhari": {"2022-23": {"Govt": 0.0}, "2023-24": {"Govt": 10.0}, "2024-25": {"Govt": 6.0}, "2025-26": {"Govt": 1.0}}}, "ARUA": {"Bhandaripokhari": {"2022-23": {"Ponds": 8.0}, "2023-24": {"Ponds": 8.0}, "2024-25": {"Ponds": 8.0}, "2025-26": {"Ponds": 8.0}}, "Dhamnagar": {"2022-23": {"Ponds": 7.0}, "2023-24": {"Ponds": 7.0}, "2024-25": {"Ponds": 7.0}, "2025-26": {"Ponds": 7.0}}}},
    "Bolangir": {"Rainfall": {"2022": 1110.0, "2023": 1193.4, "2024": 1092.3, "2025": 1092.3}, "Urban": {"Bolangir": {"2022-23": {"Govt": 2.0, "Pvt": 154.0}, "2023-24": {"Govt": 4.0, "Pvt": 964.0}, "2024-25": {"Govt": 4.0, "Pvt": 14.0}, "2025-26": {"Govt": 0.0, "Pvt": 143.0}}, "Titilagarh": {"2022-23": {"Govt": 2.0, "Pvt": 13.0}, "2023-24": {"Govt": 4.0, "Pvt": 165.0}, "2024-25": {"Govt": 2.0, "Pvt": 311.0}, "2025-26": {"Govt": 2.0, "Pvt": 243.0}}}, "Rural": {"Loisingha": {"2022-23": {"Govt": 3.0}, "2023-24": {"Govt": 4.0}, "2024-25": {"Govt": 3.0}, "2025-26": {"Govt": 7.0}}, "Bolangir": {"2022-23": {"Govt": 3.0}, "2023-24": {"Govt": 3.0}, "2024-25": {"Govt": 5.0}, "2025-26": {"Govt": 5.0}}}, "ARUA": {"Loisinga": {"2022-23": {"Ponds": 7.0}, "2023-24": {"Ponds": 5.0}, "2024-25": {"Ponds": 11.0}, "2025-26": {"Ponds": 0.0}}}},
    "Dhenkanal": {"Rainfall": {"2022": 1421.7, "2023": 1629.7, "2024": 1496.2, "2025": 1496.2}, "Urban": {"Dhenkanal": {"2022-23": {"Govt": 2.0, "Pvt": 120.0}, "2023-24": {"Govt": 7.0, "Pvt": 280.0}, "2024-25": {"Govt": 10.0, "Pvt": 432.0}, "2025-26": {"Govt": 5.0, "Pvt": 445.0}}}, "Rural": {"Dhenkanal": {"2022-23": {"Govt": 9.0}, "2023-24": {"Govt": 12.0}, "2024-25": {"Govt": 0.0}, "2025-26": {"Govt": 5.0}}, "Odapada": {"2022-23": {"Govt": 5.0}, "2023-24": {"Govt": 5.0}, "2024-25": {"Govt": 1.0}, "2025-26": {"Govt": 5.0}}}},
    "Ganjam": {"Rainfall": {"2022": 1338.6, "2023": 930.4, "2024": 1151.9, "2025": 1151.9}, "Urban": {"Aska": {"2022-23": {"Govt": 4.0, "Pvt": 15.0}, "2023-24": {"Govt": 4.0, "Pvt": 158.0}, "2024-25": {"Govt": 4.0, "Pvt": 514.0}, "2025-26": {"Govt": 3.0, "Pvt": 85.0}}, "Berhampur": {"2022-23": {"Govt": 13.0, "Pvt": 233.0}, "2023-24": {"Govt": 11.0, "Pvt": 1083.0}, "2024-25": {"Govt": 0.0, "Pvt": 443.0}, "2025-26": {"Govt": 9.0, "Pvt": 0.0}}}, "Rural": {"Ganjam": {"2022-23": {"Govt": 14.0}, "2023-24": {"Govt": 6.0}, "2024-25": {"Govt": 0.0}, "2025-26": {"Govt": 3.0}}, "Aska": {"2022-23": {"Govt": 10.0}, "2023-24": {"Govt": 4.0}, "2024-25": {"Govt": 1.0}, "2025-26": {"Govt": 2.0}}}},
    "Jharsuguda": {"Rainfall": {"2022": 1323.8, "2023": 1715.4, "2024": 1059.3, "2025": 1059.3}, "Urban": {"Jharsuguda": {"2022-23": {"Govt": 3.0, "Pvt": 86.0}, "2023-24": {"Govt": 3.0, "Pvt": 325.0}, "2024-25": {"Govt": 10.0, "Pvt": 339.0}, "2025-26": {"Govt": 6.0, "Pvt": 286.0}}}, "Rural": {"Jharsuguda": {"2022-23": {"Govt": 6.0}, "2023-24": {"Govt": 4.0}, "2024-25": {"Govt": 7.0}, "2025-26": {"Govt": 2.0}}}, "ARUA": {"Jharsuguda": {"2022-23": {"Ponds": 8.0}, "2023-24": {"Ponds": 8.0}, "2024-25": {"Ponds": 8.0}, "2025-26": {"Ponds": 8.0}}}},
    "Kendrapara": {"Rainfall": {"2022": 1405.2, "2023": 1130.8, "2024": 1435.4, "2025": 1435.4}, "Urban": {"Kendrapada": {"2022-23": {"Govt": 2.0, "Pvt": 142.0}, "2023-24": {"Govt": 5.0, "Pvt": 206.0}, "2024-25": {"Govt": 11.0, "Pvt": 294.0}, "2025-26": {"Govt": 5.0, "Pvt": 71.0}}}, "Rural": {"Garadpur": {"2022-23": {"Govt": 7.0}, "2023-24": {"Govt": 0.0}, "2024-25": {"Govt": 6.0}, "2025-26": {"Govt": 4.0}}}, "ARUA": {"Garadpur": {"2022-23": {"Ponds": 45.0}, "2023-24": {"Ponds": 40.0}, "2024-25": {"Ponds": 41.0}, "2025-26": {"Ponds": 52.0}}}},
    "Mayurbhanj": {"Rainfall": {"2022": 1413.5, "2023": 1375.8, "2024": 1495.9, "2025": 1495.9}, "Urban": {"Baripada": {"2022-23": {"Govt": 0.0, "Pvt": 293.0}, "2023-24": {"Govt": 12.0, "Pvt": 579.0}, "2024-25": {"Govt": 5.0, "Pvt": 154.0}, "2025-26": {"Govt": 0.0, "Pvt": 391.0}}}, "Rural": {"Badsahi": {"2022-23": {"Govt": 0.0}, "2023-24": {"Govt": 15.0}, "2024-25": {"Govt": 0.0}, "2025-26": {"Govt": 10.0}}}, "ARUA": {"Badasahi": {"2022-23": {"Ponds": 8.0}, "2023-24": {"Ponds": 8.0}, "2024-25": {"Ponds": 8.0}, "2025-26": {"Ponds": 8.0}}}},
    "Sambalpur": {"Rainfall": {"2022": 1389.9, "2023": 1772.4, "2024": 1319.1, "2025": 1319.1}, "Urban": {"Sambalpur": {"2022-23": {"Govt": 3.0, "Pvt": 202.0}, "2023-24": {"Govt": 3.0, "Pvt": 643.0}, "2024-25": {"Govt": 15.0, "Pvt": 344.0}, "2025-26": {"Govt": 8.0, "Pvt": 423.0}}}, "Rural": {}, "ARUA": {}},
    "Sundargarh": {"Rainfall": {"2022": 1250.8, "2023": 1391.7, "2024": 1147.1, "2025": 1147.1}, "Urban": {"Rourkela": {"2022-23": {"Govt": 3.0, "Pvt": 58.0}, "2023-24": {"Govt": 4.0, "Pvt": 416.0}, "2024-25": {"Govt": 16.0, "Pvt": 544.0}, "2025-26": {"Govt": 5.0, "Pvt": 334.0}}}, "Rural": {"Bisra": {"2022-23": {"Govt": 3.0}, "2023-24": {"Govt": 7.0}, "2024-25": {"Govt": 0.0}, "2025-26": {"Govt": 6.0}}}, "ARUA": {"Bisra": {"2022-23": {"Ponds": 8.0}, "2023-24": {"Ponds": 8.0}, "2024-25": {"Ponds": 8.0}, "2025-26": {"Ponds": 8.0}}}},
    "Boudh": {"Rainfall": {"2022": 1675.1, "2023": 1559.2, "2024": 1409.3, "2025": 1409.3}, "Urban": {}, "Rural": {}, "ARUA": {}},
    "Deogarh": {"Rainfall": {"2022": 1545.2, "2023": 1527.4, "2024": 1214.1, "2025": 1214.1}, "Urban": {}, "Rural": {}, "ARUA": {}},
    "Gajapati": {"Rainfall": {"2022": 1537.9, "2023": 1220.3, "2024": 1232.4, "2025": 1232.4}, "Urban": {}, "Rural": {}, "ARUA": {}},
    "Kalahandi": {"Rainfall": {"2022": 1555.1, "2023": 1335.9, "2024": 1370.6, "2025": 1370.6}, "Urban": {}, "Rural": {}, "ARUA": {}},
    "Kandhamal": {"Rainfall": {"2022": 2022.9, "2023": 1610.7, "2024": 1208.8, "2025": 1208.8}, "Urban": {}, "Rural": {}, "ARUA": {}},
    "Koraput": {"Rainfall": {"2022": 1919.6, "2023": 1749.7, "2024": 1733.1, "2025": 1733.1}, "Urban": {}, "Rural": {}, "ARUA": {}},
    "Malkanagiri": {"Rainfall": {"2022": 1559.3, "2023": 1762.5, "2024": 2287.0, "2025": 2287.0}, "Urban": {}, "Rural": {}, "ARUA": {}},
    "Nabarangpur": {"Rainfall": {"2022": 1714.3, "2023": 1331.4, "2024": 1439.8, "2025": 1439.8}, "Urban": {"Nabarangapur": {"2022-23": {"Govt": 2.0, "Pvt": 115.0}, "2023-24": {"Govt": 4.0, "Pvt": 228.0}, "2024-25": {"Govt": 7.0, "Pvt": 132.0}, "2025-26": {"Govt": 6.0, "Pvt": 224.0}}}, "Rural": {}, "ARUA": {}},
    "Nayagarh": {"Rainfall": {"2022": 1496.2, "2023": 1275.1, "2024": 1508.9, "2025": 1508.9}, "Urban": {"Nayagarh": {"2022-23": {"Govt": 2.0, "Pvt": 95.0}, "2023-24": {"Govt": 5.0, "Pvt": 400.0}, "2024-25": {"Govt": 9.0, "Pvt": 179.0}, "2025-26": {"Govt": 8.0, "Pvt": 264.0}}}, "Rural": {"Nayagarh": {"2022-23": {"Govt": 6.0}, "2023-24": {"Govt": 9.0}, "2024-25": {"Govt": 5.0}, "2025-26": {"Govt": 5.0}}}, "ARUA": {"Nayagarh": {"2022-23": {"Ponds": 8.0}, "2023-24": {"Ponds": 8.0}, "2024-25": {"Ponds": 8.0}, "2025-26": {"Ponds": 8.0}}}},
    "Nuapada": {"Rainfall": {"2022": 1245.6, "2023": 1235.4, "2024": 1394.0, "2025": 1394.0}, "Urban": {}, "Rural": {"Nuapada": {"2022-23": {"Govt": 2.0}, "2023-24": {"Govt": 4.0}, "2024-25": {"Govt": 1.0}, "2025-26": {"Govt": 4.0}}}, "ARUA": {"Nuapada": {"2022-23": {"Ponds": 45.0}, "2023-24": {"Ponds": 45.0}, "2024-25": {"Ponds": 45.0}, "2025-26": {"Ponds": 45.0}}}},
    "Rayagada": {"Rainfall": {"2022": 1393.3, "2023": 1155.1, "2024": 1018.1, "2025": 1018.1}, "Urban": {}, "Rural": {}, "ARUA": {}},
}

# --- 2. CONFIGURATION ---
CONSTANTS = {"Govt": 162.57, "Pvt": 123.09, "Ponds": 8750.0, "RIF": 0.6, "Efficiency": 0.7}
THRESHOLD = 762.0

st.set_page_config(page_title="CHHATA Master Application", layout="wide", page_icon="💧")
st.title("💧 CHHATA Scheme: Official Master Application")
st.markdown("---")

# Setup Navigation Tabs
tab1, tab2 = st.tabs(["📊 Historical Analysis", "🧮 Custom Estimator"])

# --- TAB 1: DATA ANALYSIS ---
with tab1:
    st.header("Implementation Dashboard (2022-2025)")
    st.write("Analyze year-wise construction and recharge based on actual field figures.")

    # Select Filters in Sidebar
    st.sidebar.header("Data Dashboard Filters")
    district = st.sidebar.selectbox("1. Select District", sorted(MASTER_DATA.keys()))
    cat_map = {"Urban (ULB)": "Urban", "Rural (Block)": "Rural", "ARUA (Artificial Recharge)": "ARUA"}
    category_label = st.sidebar.radio("2. Select Category", list(cat_map.keys()))
    cat_key = cat_map[category_label]

    # Sub-area selection
    available_areas = list(MASTER_DATA[district].get(cat_key, {}).keys())

    if not available_areas:
        st.warning(f"No {category_label} records found for {district} in the dataset.")
    else:
        selected_area = st.sidebar.selectbox(f"3. Select {cat_key}", available_areas)
        
        # Calculation Engine
        fy_labels = ["2022-23", "2023-24", "2024-25", "2025-26"]
        rain_map = MASTER_DATA[district]["Rainfall"]
        construction_stats = MASTER_DATA[district][cat_key][selected_area]
        
        results_data = []
        for fy in fy_labels:
            rain_yr = fy.split("-")[0]
            raw_rain = float(rain_map.get(rain_yr, 0))
            
            # Application of 762mm deduction for ARUA
            effective_rain = max(0, raw_rain - THRESHOLD) if cat_key == "ARUA" else raw_rain
            
            counts = construction_stats.get(fy, {})
            fy_recharge = 0
            details = []
            
            for s_type, count in counts.items():
                area_m2 = CONSTANTS.get(s_type, 162.57)
                recharge = count * area_m2 * (effective_rain / 1000) * CONSTANTS["RIF"] * CONSTANTS["Efficiency"]
                fy_recharge += recharge
                details.append(f"{s_type}: {int(count)}")
            
            results_data.append({
                "Financial Year": fy,
                "Rainfall (mm)": round(raw_rain, 1),
                "Structures Built": ", ".join(details),
                "Recharge (m³)": round(fy_recharge, 2)
            })
        
        df = pd.DataFrame(results_data)

        # Layout for Tab 1
        col1, col2 = st.columns([1, 1.8])
        
        with col1:
            st.subheader(f"Results for {selected_area}")
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            total_m3 = df["Recharge (m³)"].sum()
            st.metric("Total Groundwater Recharge", f"{total_m3:,.2f} m³")
            st.metric("Total Volume in BCM", f"{total_m3 / 1e9:.8f} BCM")

        with col2:
            st.subheader("Trends: Rainfall Impact vs Recharge")
            fig = go.Figure()
            
            # Raw Rainfall Bars
            fig.add_trace(go.Bar(
                x=df["Financial Year"], y=df["Rainfall (mm)"],
                name="Rainfall (mm)", marker_color='rgba(135, 206, 250, 0.6)', yaxis='y'
            ))
            
            # Recharge Line
            fig.add_trace(go.Scatter(
                x=df["Financial Year"], y=df["Recharge (m³)"],
                name="Recharge (m³)", marker_color='navy',
                mode='lines+markers+text', text=df["Recharge (m³)"],
                textposition="top center", yaxis='y2'
            ))

            fig.update_layout(
                yaxis=dict(title="Rainfall (mm)", side="left"),
                yaxis2=dict(title="Recharge (m³)", side="right", overlaying="y", showgrid=False),
                template="plotly_white",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig, use_container_width=True)

# --- TAB 2: CUSTOM ESTIMATOR (CALCULATOR) ---
with tab2:
    st.header("⚡ Custom Recharge Estimator")
    st.write("Use this calculator to estimate potential recharge for planned structures or custom scenarios.")

    calc_col1, calc_col2 = st.columns(2)

    with calc_col1:
        st.subheader("Input Parameters")
        c_count = st.number_input("Number of New Structures", min_value=1, value=10, key="c_count")
        c_rainfall = st.number_input("Annual Rainfall for the Area (mm)", min_value=0.0, value=1200.0, key="c_rain")
        c_type = st.selectbox("Structure Category", ["Government Building", "Private Building", "ARUA Pond Shaft"], key="c_type")
        
        # Setup logic constants
        area_map = {"Government Building": 162.57, "Private Building": 123.09, "ARUA Pond Shaft": 8750.0}
        c_area = area_map[c_type]
        
        # Toggle ARUA Deduction automatically based on selection, or let user decide
        c_arua_logic = st.toggle("Apply ARUA 762mm Threshold Deduction", value=(c_type == "ARUA Pond Shaft"), key="c_logic")
    
    with calc_col2:
        st.subheader("Estimation Result")
        # Handle the Rainfall - 762 logic
        final_rain = max(0, c_rainfall - THRESHOLD) if c_arua_logic else c_rainfall
        
        # Calculate result: Count * Area * Rain_m * RIF * Efficiency
        c_result = c_count * c_area * (final_rain / 1000) * 0.6 * 0.7
        
        st.metric("Estimated Annual Recharge", f"{c_result:,.2f} m³")
        st.metric("Volume in BCM", f"{c_result / 1e9:.10f} BCM")

        with st.expander("🔍 Show Calculation Formula & Logic"):
            st.write(f"**Structure Type:** {c_type}")
            st.write(f"**Selected Roof/Catchment Area:** {c_area} sq.m")
            if c_arua_logic:
                st.write(f"**Effective Rainfall Calculation:** {c_rainfall} - 762 = **{final_rain} mm**")
            else:
                st.write(f"**Applied Rainfall:** {c_rainfall} mm")
            
            st.latex(rf"{c_count} \times {c_area} \times \frac{{{final_rain}}}{{1000}} \times 0.6 \times 0.7 = {c_result:,.2f} m^3")

st.caption("Developed for CHHATA Scheme Technical Assessment | Data Verified 2026")
