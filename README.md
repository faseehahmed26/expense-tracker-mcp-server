
# Expense Tracker MCP Server

A Model Context Protocol (MCP) server built with FastMCP that provides expense tracking capabilities. This server allows AI assistants and other MCP clients to add, list, and summarize expenses through a simple SQLite-based database.

## Acknowledgments

This project was inspired by and learned from the [CampusX YouTube channel](https://www.youtube.com/@campusx-official). Special thanks to CampusX for their excellent tutorials and educational content.

## Features

- **Add Expenses**: Record expenses with date, amount, category, subcategory, and optional notes
- **List Expenses**: Query expenses within a date range
- **Summarize Expenses**: Get category-wise expense summaries with optional filtering
- **Category Management**: Access expense categories via MCP resources
- **SQLite Storage**: Lightweight, file-based database for easy data management

## Requirements

- Python >= 3.11
- [uv](https://github.com/astral-sh/uv) (recommended) or pip
- FastMCP >= 2.12.3

## Installation

### Using uv (Recommended)

1. Clone or navigate to this directory:
   ```bash
   cd expense-tracker-mcp-server
   ```

2. Install dependencies:
   ```bash
   uv sync
   ```

3. Pin Python version (if needed):
   ```bash
   uv python pin 3.11
   ```

### Using pip

1. Create a virtual environment:
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install fastmcp>=2.12.3
   ```

## Usage

### Running the Server

#### Development Mode (with Inspector)

```bash
uv run fastmcp dev main.py
```

This will start the MCP server with the inspector UI, allowing you to test tools and resources interactively.

#### Production Mode

```bash
uv run fastmcp run main.py
```

### Installing in Claude Desktop

To use this server with Claude Desktop:

```bash
uv run fastmcp install claude-desktop main.py
```

This will automatically configure Claude Desktop to use this MCP server.

## MCP Tools

### `add_expense`

Add a new expense entry to the database.

**Parameters:**
- `date` (string, required): Date of the expense (e.g., "2024-01-15")
- `amount` (float, required): Expense amount
- `category` (string, required): Main category name
- `subcategory` (string, optional): Subcategory (defaults to empty string)
- `note` (string, optional): Additional notes (defaults to empty string)

**Returns:**
```json
{
  "status": "ok",
  "id": 1
}
```

**Example:**
```python
add_expense(
    date="2024-01-15",
    amount=25.50,
    category="Food",
    subcategory="Groceries",
    note="Weekly shopping"
)
```

### `list_expenses`

List expense entries within an inclusive date range.

**Parameters:**
- `start_date` (string, required): Start date of the range (inclusive)
- `end_date` (string, required): End date of the range (inclusive)

**Returns:**
List of expense dictionaries with fields: `id`, `date`, `amount`, `category`, `subcategory`, `note`

**Example:**
```python
list_expenses(
    start_date="2024-01-01",
    end_date="2024-01-31"
)
```

### `summarize`

Summarize expenses by category within a date range.

**Parameters:**
- `start_date` (string, required): Start date of the range (inclusive)
- `end_date` (string, required): End date of the range (inclusive)
- `category` (string, optional): Filter by specific category (defaults to None)

**Returns:**
List of dictionaries with `category` and `total_amount` fields

**Example:**
```python
# Summarize all categories
summarize(
    start_date="2024-01-01",
    end_date="2024-01-31"
)

# Summarize specific category
summarize(
    start_date="2024-01-01",
    end_date="2024-01-31",
    category="Food"
)
```

## MCP Resources

### `expense://categories`

Provides access to the expense categories JSON file. This resource is read fresh on each access, so you can edit `categories.json` without restarting the server.

**MIME Type:** `application/json`

## Configuration

### Database

The SQLite database (`expenses.db`) is automatically created in the project directory when the server starts. The database schema includes:

- `id`: Auto-incrementing primary key
- `date`: Expense date (TEXT)
- `amount`: Expense amount (REAL)
- `category`: Main category (TEXT, required)
- `subcategory`: Subcategory (TEXT, optional)
- `note`: Additional notes (TEXT, optional)

### Categories File

Create a `categories.json` file in the project root to define available expense categories. The file should contain valid JSON. Example:

```json
{
  "Food": ["Groceries", "Restaurants", "Takeout"],
  "Transport": ["Gas", "Public Transit", "Parking"],
  "Entertainment": ["Movies", "Concerts", "Games"],
  "Bills": ["Utilities", "Internet", "Phone"]
}
```

## Development

### Project Structure

```
expense-tracker-mcp-server/
├── main.py              # Main server implementation
├── expenses.db          # SQLite database (auto-generated)
├── categories.json      # Expense categories configuration
├── pyproject.toml       # Project configuration
├── .python-version      # Python version pin
└── README.md           # This file
```

### Running Tests

You can test the server using the FastMCP inspector:

```bash
uv run fastmcp dev main.py
```

This opens a web interface where you can:
- View available tools and resources
- Test tool calls with sample parameters
- Inspect responses and errors

## Troubleshooting

### Python Version Issues

If you encounter Python version errors, ensure you're using Python 3.11 or higher:

```bash
python3 --version
```

Use `uv python pin` to set the correct version:

```bash
uv python pin 3.11
```

### Database Errors

If the database becomes corrupted, you can safely delete `expenses.db` and it will be recreated on the next server start.

### Missing Categories File

If `categories.json` doesn't exist, create an empty JSON object `{}` or a properly formatted categories structure.

