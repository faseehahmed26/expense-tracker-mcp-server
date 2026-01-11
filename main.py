# Import required libraries
from fastmcp import FastMCP  # FastMCP framework for building MCP servers
import os  # For file path operations
import sqlite3  # SQLite database for storing expenses

# Define file paths relative to this script's location
DB_PATH = os.path.join(os.path.dirname(__file__), "expenses.db")  # SQLite database file path
CATEGORIES_PATH = os.path.join(os.path.dirname(__file__), "categories.json")  # JSON file containing expense categories

# Initialize the FastMCP server with a name
mcp = FastMCP("ExpenseTracker")

def init_db():
    """
    Initialize the SQLite database by creating the expenses table if it doesn't exist.
    This function is called at module import time to ensure the database is ready.
    """
    with sqlite3.connect(DB_PATH) as c:  # Context manager ensures connection is closed
        # Create expenses table with all required fields
        c.execute("""
            CREATE TABLE IF NOT EXISTS expenses(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                subcategory TEXT DEFAULT '',
                note TEXT DEFAULT ''
            )
        """)

# Initialize the database when the module is imported
init_db()

@mcp.tool()  # Decorator registers this function as an MCP tool (callable by clients)
def add_expense(date, amount, category, subcategory="", note=""):
    """
    Add a new expense entry to the database.
    
    Args:
        date: Date of the expense (string format)
        amount: Expense amount (float)
        category: Main category name (string)
        subcategory: Optional subcategory (string, defaults to empty)
        note: Optional note about the expense (string, defaults to empty)
    
    Returns:
        Dictionary with status and the ID of the newly created expense
    """
    with sqlite3.connect(DB_PATH) as c:
        # Use parameterized query to prevent SQL injection
        cur = c.execute(
            "INSERT INTO expenses(date, amount, category, subcategory, note) VALUES (?,?,?,?,?)",
            (date, amount, category, subcategory, note)
        )
        return {"status": "ok", "id": cur.lastrowid}  # Return success status and new expense ID
    
@mcp.tool()  # Register as an MCP tool
def list_expenses(start_date, end_date):
    """
    List expense entries within an inclusive date range.
    
    Args:
        start_date: Start date of the range (inclusive)
        end_date: End date of the range (inclusive)
    
    Returns:
        List of dictionaries, each representing an expense entry with all fields
    """
    with sqlite3.connect(DB_PATH) as c:
        # Query expenses within date range, ordered by ID
        cur = c.execute(
            """
            SELECT id, date, amount, category, subcategory, note
            FROM expenses
            WHERE date BETWEEN ? AND ?
            ORDER BY id ASC
            """,
            (start_date, end_date)
        )
        # Convert query results to list of dictionaries for easier JSON serialization
        cols = [d[0] for d in cur.description]  # Get column names from cursor description
        return [dict(zip(cols, r)) for r in cur.fetchall()]  # Convert each row to a dict

@mcp.tool()  # Register as an MCP tool
def summarize(start_date, end_date, category=None):
    """
    Summarize expenses by category within an inclusive date range.
    Optionally filter by a specific category.
    
    Args:
        start_date: Start date of the range (inclusive)
        end_date: End date of the range (inclusive)
        category: Optional category filter (if None, summarizes all categories)
    
    Returns:
        List of dictionaries with category names and their total amounts
    """
    with sqlite3.connect(DB_PATH) as c:
        # Build query dynamically based on whether category filter is provided
        query = (
            """
            SELECT category, SUM(amount) AS total_amount
            FROM expenses
            WHERE date BETWEEN ? AND ?
            """
        )
        params = [start_date, end_date]

        # Add category filter if specified
        if category:
            query += " AND category = ?"
            params.append(category)

        # Group by category and order alphabetically
        query += " GROUP BY category ORDER BY category ASC"

        cur = c.execute(query, params)
        # Convert results to list of dictionaries
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]

@mcp.resource("expense://categories", mime_type="application/json")  # Register as an MCP resource
def categories():
    """
    Provide access to the categories JSON file as an MCP resource.
    This allows clients to read the available expense categories.
    
    Returns:
        Contents of the categories.json file as a string
    """
    # Read fresh each time so you can edit the file without restarting
    with open(CATEGORIES_PATH, "r", encoding="utf-8") as f:
        return f.read()

# Entry point: Run the MCP server when script is executed directly
if __name__ == "__main__":
    mcp.run()  # Start the MCP server (defaults to stdio transport)