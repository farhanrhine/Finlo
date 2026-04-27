import sqlite3
from datetime import datetime


def get_db():
    """Reuse the existing get_db function from db.py"""
    conn = sqlite3.connect('Finlo.db')
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON;')
    return conn


def _close_db(conn):
    """Helper to close database connection"""
    conn.close()


def get_user_by_id(user_id):
    """Fetch user details by user_id"""
    conn = get_db()
    try:
        result = conn.execute(
            'SELECT id, name, email, created_at FROM users WHERE id = ?',
            (user_id,)
        ).fetchone()
        if result:
            user = dict(result)
            # Format date as "Month YYYY" (e.g., "April 2026")
            # Handle both full datetime (with time) and date-only formats
            created_str = user['created_at']
            if ' ' in created_str:
                # Has timestamp, take only the date part
                created_str = created_str.split(' ')[0]
            created_date = datetime.strptime(created_str, '%Y-%m-%d')
            user['member_since'] = created_date.strftime('%B %Y')
            return user
        return None
    finally:
        _close_db(conn)


def get_summary_stats(user_id):
    """Fetch summary statistics for a user"""
    conn = get_db()
    try:
        # Get total spent and transaction count
        stats = conn.execute(
            '''SELECT
                SUM(amount) as total_spent,
                COUNT(*) as transaction_count
            FROM expenses
            WHERE user_id = ?''',
            (user_id,)
        ).fetchone()

        result = {
            'total_spent': stats['total_spent'] if stats['total_spent'] else 0.0,
            'transaction_count': stats['transaction_count'] if stats['transaction_count'] else 0,
            'top_category': '—'
        }

        # Get top category if there are transactions
        if result['transaction_count'] > 0:
            top_cat = conn.execute(
                '''SELECT category, SUM(amount) as cat_total
                FROM expenses
                WHERE user_id = ?
                GROUP BY category
                ORDER BY cat_total DESC
                LIMIT 1''',
                (user_id,)
            ).fetchone()
            if top_cat:
                result['top_category'] = top_cat['category']

        return result
    finally:
        _close_db(conn)


def get_recent_transactions(user_id, limit=10):
    """Fetch recent transactions for a user"""
    conn = get_db()
    try:
        rows = conn.execute(
            '''SELECT date, description, category, amount
            FROM expenses
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT ?''',
            (user_id, limit)
        ).fetchall()

        return [dict(row) for row in rows]
    finally:
        _close_db(conn)


def get_category_breakdown(user_id):
    """Fetch category breakdown with percentages"""
    conn = get_db()
    try:
        # Get totals per category
        rows = conn.execute(
            '''SELECT category, SUM(amount) as total
            FROM expenses
            WHERE user_id = ?
            GROUP BY category
            ORDER BY total DESC''',
            (user_id,)
        ).fetchall()

        if not rows:
            return []

        # Convert to list of dicts and calculate percentages
        breakdown = []
        total_sum = sum(row['total'] for row in rows)

        for row in rows:
            pct = round((row['total'] / total_sum) * 100) if total_sum > 0 else 0
            breakdown.append({
                'name': row['category'],
                'total': f"₹{row['total']:.2f}",
                'percentage': pct
            })

        # Adjust for rounding to ensure percentages sum to 100
        if breakdown:
            total_pct = sum(item['percentage'] for item in breakdown)
            if total_pct != 100:
                # Adjust the largest category to absorb the rounding difference
                max_idx = 0
                max_pct = breakdown[0]['percentage']
                for i, item in enumerate(breakdown):
                    if item['percentage'] > max_pct:
                        max_pct = item['percentage']
                        max_idx = i
                breakdown[max_idx]['percentage'] += (100 - total_pct)

        return breakdown
    finally:
        _close_db(conn)