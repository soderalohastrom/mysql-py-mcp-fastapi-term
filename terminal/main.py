import typer
from rich.console import Console
from rich.table import Table
from common.database import CRUDOperations
from common.models import User

app = typer.Typer()
console = Console()

@app.command()
def add_user(name: str, email: str, age: int = None):
    """Add a new user to the database"""
    user_data = {"name": name, "email": email}
    if age:
        user_data["age"] = age
    user_id = CRUDOperations.create("users", user_data)
    console.print(f"[green]User created with ID: {user_id}[/green]")

@app.command()
def list_users():
    """List all users"""
    users = CRUDOperations.read("users")
    table = Table("ID", "Name", "Email", "Age")
    for user in users:
        table.add_row(
            str(user["id"]),
            user["name"],
            user["email"],
            str(user.get("age", "N/A"))
        )
    console.print(table)

@app.command()
def update_user(id: int, name: str = None, email: str = None, age: int = None):
    """Update a user's information"""
    update_data = {}
    if name:
        update_data["name"] = name
    if email:
        update_data["email"] = email
    if age:
        update_data["age"] = age
    
    if update_data:
        rows = CRUDOperations.update("users", update_data, {"id": id})
        console.print(f"[green]Updated {rows} user(s)[/green]")
    else:
        console.print("[yellow]No updates provided[/yellow]")

@app.command()
def delete_user(id: int):
    """Delete a user"""
    rows = CRUDOperations.delete("users", {"id": id})
    console.print(f"[green]Deleted {rows} user(s)[/green]")

if __name__ == "__main__":
    app()
