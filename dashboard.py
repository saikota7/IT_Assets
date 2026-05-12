import streamlit as st
import pandas as pd
import plotly.express as px
from data_handler import load_data, add_asset, update_status

st.set_page_config(layout="wide")

df = load_data()

# -------------------------
# TITLE
# -------------------------
st.markdown("## 🏢 Eruvaka Asset Management")

# -------------------------
# NAVIGATION
# -------------------------
page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Add Asset", "Stock Update"]
)

# =====================================================
# 🟢 DASHBOARD
# =====================================================
if page == "Dashboard":

    # -------------------------
    # ASSET SELECT
    # -------------------------
    asset = st.radio(
        "Select Asset",
        ["Laptop", "Keyboard", "Headset", "Monitor"],
        horizontal=True
    )

    config = {
        "Laptop": ("Laptop Status", "Laptop Location"),
        "Keyboard": ("Keyboard Status", "Keyboard Location"),
        "Headset": ("Headset Status", "Headset Location"),
        "Monitor": ("Monitor Status", "Monitor Location")
    }

    status_col, location_col = config[asset]

    # -------------------------
    # SIDEBAR FILTERS
    # -------------------------
    st.sidebar.header(f"{asset} Filters")

    df_filtered = df.copy()
    df_filtered = df_filtered[df_filtered[status_col].notna()]

    loc_filter = st.sidebar.multiselect(
        "Location",
        sorted(df_filtered[location_col].dropna().unique()),
        key=f"{asset}_loc"
    )

    dept_filter = st.sidebar.multiselect(
        "Department",
        sorted(df_filtered["Department"].dropna().unique()),
        key=f"{asset}_dept"
    )

    make_filter = st.sidebar.multiselect(
        "Make",
        sorted(df_filtered["Make"].dropna().unique()),
        key=f"{asset}_make"
    )

    model_filter = st.sidebar.multiselect(
        "Model",
        sorted(df_filtered["Model"].dropna().unique()),
        key=f"{asset}_model"
    )

    # -------------------------
    # APPLY FILTERS
    # -------------------------
    if loc_filter:
        df_filtered = df_filtered[df_filtered[location_col].isin(loc_filter)]

    if dept_filter:
        df_filtered = df_filtered[df_filtered["Department"].isin(dept_filter)]

    if make_filter:
        df_filtered = df_filtered[df_filtered["Make"].isin(make_filter)]

    if model_filter:
        df_filtered = df_filtered[df_filtered["Model"].isin(model_filter)]

    # -------------------------
    # KPI FUNCTION (UNCHANGED)
    # -------------------------
    def calculate_kpi(df, status_col):

        df = df[df[status_col].notna()]
        df[status_col] = df[status_col].astype(str).str.strip()

        valid_status = ["Assigned", "In Stock", "Scrap", "Not Working", "No-only mouse Dell"]
        df = df[df[status_col].isin(valid_status)]

        total = len(df)
        assigned = (df[status_col] == "Assigned").sum()
        stock = (df[status_col] == "In Stock").sum()
        scrap = (df[status_col] == "Scrap").sum()
        not_working = (df[status_col] == "Not Working").sum()

        return total, assigned, stock, scrap, not_working

    # -------------------------
    # KPI DISPLAY
    # -------------------------
    total, assigned, stock, scrap, not_working = calculate_kpi(df_filtered, status_col)

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total", total)
    c2.metric("Assigned", assigned)
    c3.metric("In Stock", stock)
    c4.metric("Scrap", scrap)
    c5.metric("Not Working", not_working)

    st.markdown("---")

    # -------------------------
    # CHARTS (UNCHANGED)
    # -------------------------
    st.markdown("### Dashboard")

    g1, g2 = st.columns(2)
    g3, g4 = st.columns(2)

    with g1:
        loc = df_filtered[location_col].value_counts().reset_index()
        loc.columns = ["Location", "Count"]

        fig1 = px.bar(loc, x="Location", y="Count", text="Count")
        fig1.update_traces(textposition="outside")
        fig1.update_layout(height=300)
        st.plotly_chart(fig1, use_container_width=True)

    with g2:
        status = df_filtered[status_col].value_counts().reset_index()
        status.columns = ["Status", "Count"]

        fig2 = px.pie(status, names="Status", values="Count")
        fig2.update_layout(height=300)
        st.plotly_chart(fig2, use_container_width=True)

    with g3:
        dept = df_filtered["Department"].value_counts().reset_index()
        dept.columns = ["Department", "Count"]

        fig3 = px.bar(dept, x="Department", y="Count", text="Count")
        fig3.update_traces(textposition="outside")
        fig3.update_layout(height=300)
        st.plotly_chart(fig3, use_container_width=True)

    with g4:
        model = df_filtered["Model"].value_counts().reset_index()
        model.columns = ["Model", "Count"]

        fig4 = px.bar(model.head(10), x="Model", y="Count", text="Count")
        fig4.update_traces(textposition="outside")
        fig4.update_layout(height=300)
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown("### Excel Data")
    st.markdown("---")
    st.dataframe(df_filtered)


# =====================================================
# ➕ ADD ASSET
# =====================================================
elif page == "Add Asset":

    st.header("➕ Add / Update Employee")

    df = load_data()

    # -------------------------
    # EMPLOYEE SELECT (SEARCHABLE)
    # -------------------------
    emp_list = sorted(df["Employee Name"].dropna().unique())

    emp_option = st.selectbox(
        "Select Employee",
        ["New"] + emp_list
    )

    # -------------------------
    # HANDLE NEW vs EXISTING
    # -------------------------
    if emp_option == "New":
        emp_name = st.text_input("Enter New Employee Name")
        emp_data = {}
    else:
        emp_name = emp_option

        filtered = df[df["Employee Name"] == emp_name]

        if not filtered.empty:
            emp_data = filtered.iloc[0]
        else:
            emp_data = {}

    # -------------------------
    # FORM FIELDS (SAFE GET)
    # -------------------------
    department = st.text_input("Department", value=emp_data.get("Department", ""))
    location = st.text_input("Location", value=emp_data.get("Location", ""))

    # LAPTOP
    st.subheader("💻 Laptop")
    laptop_tag = st.text_input("Laptop Asset Tag", value=emp_data.get("Laptop Asset Tag", ""))

    laptop_status_list = ["Assigned","In Stock","Scrap","Not Working"]
    laptop_status_val = emp_data.get("Laptop Status", "Assigned")

    laptop_status = st.selectbox(
        "Laptop Status",
        laptop_status_list,
        index=laptop_status_list.index(laptop_status_val) if laptop_status_val in laptop_status_list else 0
    )

    # KEYBOARD
    st.subheader("⌨️ Keyboard")
    keyboard_status_val = emp_data.get("Keyboard Status", "Assigned")

    keyboard_status = st.selectbox(
        "Keyboard Status",
        laptop_status_list,
        index=laptop_status_list.index(keyboard_status_val) if keyboard_status_val in laptop_status_list else 0
    )

    # HEADSET
    st.subheader("🎧 Headset")
    headset_status_val = emp_data.get("Headset Status", "Assigned")

    headset_status = st.selectbox(
        "Headset Status",
        laptop_status_list,
        index=laptop_status_list.index(headset_status_val) if headset_status_val in laptop_status_list else 0
    )

    # MONITOR
    st.subheader("🖥️ Monitor")
    monitor_status_val = emp_data.get("Monitor Status", "Assigned")

    monitor_status = st.selectbox(
        "Monitor Status",
        laptop_status_list,
        index=laptop_status_list.index(monitor_status_val) if monitor_status_val in laptop_status_list else 0
    )

    # -------------------------
    # SAVE LOGIC (UPDATE OR INSERT)
    # -------------------------
    if st.button("Save"):

        if not emp_name:
            st.error("⚠️ Please enter Employee Name")
        else:
            df = load_data()

            if emp_name in df["Employee Name"].values:
                # UPDATE EXISTING
                df.loc[df["Employee Name"] == emp_name, "Department"] = department
                df.loc[df["Employee Name"] == emp_name, "Location"] = location
                df.loc[df["Employee Name"] == emp_name, "Laptop Asset Tag"] = laptop_tag
                df.loc[df["Employee Name"] == emp_name, "Laptop Status"] = laptop_status
                df.loc[df["Employee Name"] == emp_name, "Keyboard Status"] = keyboard_status
                df.loc[df["Employee Name"] == emp_name, "Headset Status"] = headset_status
                df.loc[df["Employee Name"] == emp_name, "Monitor Status"] = monitor_status

                st.success("✅ Employee Updated Successfully")

            else:
                # ADD NEW
                new_row = {
                    "Employee Name": emp_name,
                    "Department": department,
                    "Location": location,
                    "Laptop Asset Tag": laptop_tag,
                    "Laptop Status": laptop_status,
                    "Keyboard Status": keyboard_status,
                    "Headset Status": headset_status,
                    "Monitor Status": monitor_status
                }

                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

                st.success("✅ New Employee Added Successfully")

            from data_handler import save_data
            save_data(df)
# =====================================================
# 📦 STOCK UPDATE
# =====================================================
elif page == "Stock Update":

    st.header("📦 Asset Stock Update")

    df = load_data()

    # -------------------------
    # SELECT ASSET TYPE
    # -------------------------
    asset = st.selectbox(
        "Select Asset",
        ["Laptop", "Keyboard", "Headset", "Monitor"]
    )

    # -------------------------
    # COLUMN MAPPING (WITH TAG)
    # -------------------------
    config = {
        "Laptop": ("Laptop Status", "Laptop Location", "Laptop Asset Tag"),
        "Keyboard": ("Keyboard Status", "Keyboard Location", "KB Asset Tag"),
        "Headset": ("Headset Status", "Headset Location", "Heaset Asset Tag"),
        "Monitor": ("Monitor Status", "Monitor Location", "Monitor Asset tag")
    }

    status_col, location_col, tag_col = config[asset]

    # -------------------------
    # SELECT ASSET TAG
    # -------------------------
    asset_tags = df[tag_col].dropna().unique()

    if len(asset_tags) == 0:
        st.warning("No asset tags found")
    else:
        selected_tag = st.selectbox(f"{asset} Asset Tag", asset_tags)

        # -------------------------
        # FILTER ROW
        # -------------------------
        filtered = df[df[tag_col] == selected_tag]

        if not filtered.empty:
            row = filtered.iloc[0]

            # -------------------------
            # UPDATE FIELDS
            # -------------------------
            new_location = st.text_input(
                "Update Location",
                value=row.get(location_col, "")
            )

            status_list = ["Assigned","In Stock","Scrap","Not Working"]
            current_status = row.get(status_col, "Assigned")

            new_status = st.selectbox(
                "Update Status",
                status_list,
                index=status_list.index(current_status) if current_status in status_list else 0
            )

            # -------------------------
            # UPDATE BUTTON
            # -------------------------
            if st.button("Update"):

                df.loc[df[tag_col] == selected_tag, location_col] = new_location
                df.loc[df[tag_col] == selected_tag, status_col] = new_status

                from data_handler import save_data
                save_data(df)

                st.success("✅ Updated Successfully")