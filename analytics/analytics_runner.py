from app.db import init_db, session_context
from analytics.trends import aggregate_popular_stats

def run_analytics():

    init_db()
    with session_context() as session:
        aggregate_popular_stats(session)

if __name__ == "__main__":
    run_analytics()
