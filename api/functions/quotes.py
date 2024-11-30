# Utility functions needed for bbc quotes

import sqlite3

def get_quote(quote_id: int = None):
    """
    Retrieves a quote from the database.

    If quote_id is provided, the quote with that ID is retrieved. Otherwise, a random quote is chosen.

    :param quote_id: The ID of the quote to retrieve, or None to get a random quote
    :return: A tuple containing the ID, content, author username, and the timestamp
    """
    conn = sqlite3.connect("assets/quotes.db")
    cursor = conn.cursor()
    if quote_id:
        cursor.execute("SELECT * FROM quotes WHERE id = ?", (quote_id,))
    else:
        cursor.execute("SELECT * FROM quotes ORDER BY RANDOM() LIMIT 1")
    quote = cursor.fetchone()
    conn.close()
    return quote