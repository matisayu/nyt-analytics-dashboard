from sqlmodel import Session
from app.db import session_context
from app.models import SectionStat
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

from sqlmodel import select

def get_section_stats(session: Session, api_window: int):
    """Fetch section stats for a given window and only for records within that rolling window."""
    today = datetime.now()
    start_date = (today - timedelta(days=api_window)).strftime("%Y-%m-%d")

    stmt = select(SectionStat).where(
        SectionStat.api_window == api_window,
        SectionStat.date_collected >= start_date
    )
    return session.exec(stmt).all()

def plot_top_sections(api_window: int, top_n=10):
    with session_context() as session:
        records = get_section_stats(session, api_window)
        if not records:
            print(f"No data found for {api_window}-day window.")
            return

        # Aggregate counts by section
        section_counts = {}
        for r in records:
            section_counts[r.section] = r.story_count

        # Sort and take top n
        top_sections = dict(sorted(section_counts.items(), key=lambda x: x[1], reverse=True)[:top_n])

        plt.figure(figsize=(10,6))
        plt.bar(top_sections.keys(), top_sections.values(), color='skyblue')
        plt.title(f"Top Sections - {api_window}-day window")
        plt.xticks(rotation=45, ha="right")
        plt.ylabel("Story Count")
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    options = {"1": 1, "3": 3, "7": 7}
    print("Select window to visualize:")
    for k, v in options.items():
        print(f"{k}: {v}-day")

    choice = input("Enter choice: ").strip()
    if choice in options:
        plot_top_sections(options[choice])
    else:
        print("Invalid choice.")
