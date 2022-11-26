from datetime import datetime
from pathlib import Path

import pandas as pd


def sanitize_month(year_month: str) -> int:
    if year_month.startswith("AF"):
        return datetime.strptime(year_month.split("_")[1], "%b").month
    else:
        return datetime.strptime(year_month.split("_")[0], "%b").month


def transform_raw_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, names=["date", "polarity", "score"])
    df["month"] = df["date"].apply(sanitize_month)
    df["year"] = path.stem.split("_")[0]
    df["branch"] = path.stem.split("_")[1]
    df["date"] = df[["year", "month"]].apply(
        lambda row: f"{row.year}-{row.month:02d}", axis=1
    )
    return df


def main():
    data = Path.cwd() / "data"
    raw_data = Path.cwd() / "raw"

    if not raw_data.exists():
        raise RuntimeError(
            "Missing raw data directory, please add raw data into a folder called raw."
        )

    if not data.exists():
        data.mkdir()

    dataframes = []
    for path in raw_data.glob("*.csv"):
        dataframes.append(transform_raw_data(path))

    df = pd.concat(dataframes).reset_index(drop=True)
    df.to_csv(data / "sentiment_data.csv", index=False)


if __name__ == "__main__":
    main()
