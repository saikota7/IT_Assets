def get_kpi(df, column):

    df[column] = df[column].astype(str).str.strip()

    total = df[column].notna().sum()

    assigned = (df[column] == "Assigned").sum()
    stock = (df[column] == "In Stock").sum()
    scrap = (df[column] == "Scrap").sum()
    not_working = (df[column] == "Not Working").sum()

    return total, assigned, stock, scrap, not_working