# Terminal Client Database Interface

A command-line interface for accessing and querying the client database using Python's Typer and Rich libraries.

## Features

- Get client information by ID with optional field filtering
- Search clients by city and gender
- Pretty-printed table output
- Color-coded responses

## Usage

---
# Get all information for a client
python -m terminal.main get-client 230126

# Get specific field for a client (e.g., Employer)
python -m terminal.main get-client 230126 --field Employer

# Search for clients
python -m terminal.main search-clients --city "Seattle" --gender "F"
---

## Example Output

---
┌─────────┬────────────────────┐
│ Field   │ Value             │
├─────────┼────────────────────┤
│ Name    │ John Smith        │
│ City    │ Seattle           │
│ State   │ WA               │
└─────────┴────────────────────┘
---

## Dependencies

- typer: Command-line interface creation
- rich: Terminal formatting and tables
- python-dotenv: Environment configuration
- mysql-connector-python: Database connectivity

## Future Enhancements

- [ ] Add support for complex search criteria
- [ ] Export results to CSV/JSON
- [ ] Interactive mode with command history
- [ ] Batch operations support
- [ ] Natural language query support