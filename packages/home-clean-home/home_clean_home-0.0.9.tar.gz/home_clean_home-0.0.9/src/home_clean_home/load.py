from collections import defaultdict
from importlib.resources import files

import pandas as pd


def load_hch_service_details_info(
    excel_path: str = str(files("home_clean_home") / "docs" / "hch_knowledge_base_ref.xlsx"),
    sheet: str = "Services Summary and Attachment",
) -> dict[str, list[str]]:
    hch_df = pd.read_excel(excel_path, sheet_name=sheet)
    hch_df["Category"] = hch_df["Category"].ffill()
    hch_df["Service within Category"] = hch_df["Service within Category"].ffill()
    hch_df["Latest Desired Message Response to the service (as of 4 Dec)"] = hch_df[
        "Latest Desired Message Response to the service (as of 4 Dec)"
    ].ffill()
    hch_df["Desired Response After User Provide Image/Video (Deprecated)"] = hch_df[
        "Desired Response After User Provide Image/Video (Deprecated)"
    ].ffill()
    hch_df["Mandatory Details Required from User Before Escalating to Human"] = hch_df[
        "Mandatory Details Required from User Before Escalating to Human"
    ].ffill()
    hch_df.set_index(["Category"], inplace=True)

    hch_split = hch_df.to_dict(orient="split")

    columns = hch_split["columns"]
    service2details_info = defaultdict(list)
    for cur_index, cur_data in zip(hch_split["index"], hch_split["data"]):
        raw_info = ""
        for cur_column, cur_value in zip(columns, cur_data):
            raw_info += f"{cur_column}: {cur_value}\n"
            raw_info += f"{'-'*50}\n"
        service2details_info[cur_index].append(
            f"## Relevant Information {len(service2details_info[cur_index])+1}\n\n" + raw_info
        )
    return service2details_info


def load_hch_service_price_info(
    excel_path: str = str(files("home_clean_home") / "docs" / "hch_knowledge_base_ref.xlsx"),
    sheets: list[str] = [
        "Surcharge",
        "House",
        "Floor Scrubbing",
        "Sofa",
        "Mattress",
        "Carpet",
        "Curtain",
        "Disinfecting",
        "Formaldehyde",
    ],
) -> dict[str, list[str]]:
    sheet2df = pd.read_excel(excel_path, sheet_name=sheets)
    sheet2services = {
        "Surcharge": ["all"],
        "House": [
            "Detail Cleaning",
            "Move In Cleaning",
            "Move Out Cleaning",
            "Post-Renovation Cleaning",
            "Spring Cleaning (Occupied Unit)",
        ],
        "Floor Scrubbing": ["Floor Cleaning or Floor Care"],
        "Sofa": ["Household Accessory Cleaning (e.g. Sofa, Mattress, Carpet, Curtains)"],
        "Mattress": ["Household Accessory Cleaning (e.g. Sofa, Mattress, Carpet, Curtains)"],
        "Carpet": ["Household Accessory Cleaning (e.g. Sofa, Mattress, Carpet, Curtains)"],
        "Curtain": ["Household Accessory Cleaning (e.g. Sofa, Mattress, Carpet, Curtains)"],
        "Disinfecting": ["Disinfecting"],
        "Formaldehyde": ["Formaldehyde (VOC)"],
    }
    service2tables = defaultdict(list)
    for sheet in sheets:
        df = sheet2df[sheet]
        # Identify empty rows (all NaN)
        empty_rows = df.isnull().all(axis=1)
        # Get the index of empty rows
        empty_indices = df.index[empty_rows].tolist()
        # Add the start and end indices
        table_start_indices = [0] + [idx + 1 for idx in empty_indices if idx + 1 < len(df)]
        table_end_indices = empty_indices + [len(df)]
        # Extract each table
        tables = []
        for idx, (start, end) in enumerate(zip(table_start_indices, table_end_indices)):
            table = df.iloc[start:end].dropna(how="all", axis=1)  # Drop empty columns
            if not table.empty:  # Ignore empty tables
                if idx > 0:
                    table = table.set_axis(table.iloc[0].tolist(), axis=1).reset_index(drop=True).drop(labels=0, axis=0)
                tables.append(table.to_dict(orient="index"))

        services = sheet2services[sheet]
        for service in services:
            service2tables[service].extend(tables)

    if "all" in service2tables:
        extra_tables = service2tables.pop("all")
        for service in service2tables:
            service2tables[service].extend(extra_tables)

    service2price_info = defaultdict(list)
    for service, tables in service2tables.items():
        for rel_idx, table in enumerate(tables):
            raw_info = ""
            for item_idx, col2val in enumerate(table.values()):
                raw_info += f"{item_idx+1}: {col2val}\n"
            service2price_info[service].append(f"## Relevant Information {rel_idx+1}\n\n" + raw_info)

    return service2price_info
