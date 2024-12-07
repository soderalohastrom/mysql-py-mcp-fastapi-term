import typer
from rich.console import Console
from rich.table import Table
from common.database import DatabaseConnection

app = typer.Typer()
console = Console()

@app.command()
def get_client(client_id: int, field: str = None):
    """Get client information by ID"""
    fields = [field] if field else None
    db = DatabaseConnection()
    result = db.get_client(client_id, fields)
    
    if result:
        table = Table(title=f"Client {client_id}")
        table.add_column("Field")
        table.add_column("Value")
        
        for key, value in result.items():
            table.add_row(str(key), str(value))
        
        console.print(table)
    else:
        console.print(f"No client found with ID {client_id}")

@app.command()
def search_clients(city: str = None, gender: str = None):
    """Search clients by criteria"""
    criteria = {}
    if city:
        criteria['city'] = city
    if gender:
        criteria['gender'] = gender
    
    db = DatabaseConnection()
    results = db.search_clients(criteria)
    
    if results:
        table = Table(title="Search Results")
        table.add_column("ID")
        table.add_column("Name")
        table.add_column("Gender")
        table.add_column("Location")
        
        for r in results:
            table.add_row(
                str(r['Person_id']),
                f"{r['FirstName']} {r['LastName']}",
                r['Gender'],
                f"{r['City']}, {r['State']}"
            )
        
        console.print(table)
    else:
        console.print("No clients found matching criteria")

if __name__ == "__main__":
    app()
