from common.database import DatabaseConnection, CRUDOperations
from common.models import User

def test_connection():
    try:
        with DatabaseConnection() as cursor:
            print("Database connection successful!")
            return True
    except Exception as e:
        print(f"Connection failed: {e}")
        return False

def test_crud():
    # Test user data
    test_user = User(name="Test User", email="test@example.com", age=30)
    user_dict = {
        "name": test_user.name,
        "email": test_user.email,
        "age": test_user.age
    }
    
    try:
        # Create
        user_id = CRUDOperations.create("users", user_dict)
        print(f"Created user with ID: {user_id}")
        
        # Read
        users = CRUDOperations.read("users", {"id": user_id})
        print(f"Read user: {users[0]}")
        
        # Update
        update_data = {"name": "Updated User"}
        rows_updated = CRUDOperations.update("users", update_data, {"id": user_id})
        print(f"Updated {rows_updated} rows")
        
        # Delete
        rows_deleted = CRUDOperations.delete("users", {"id": user_id})
        print(f"Deleted {rows_deleted} rows")
        
        return True
    except Exception as e:
        print(f"CRUD test failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing database connection...")
    test_connection()
    print("\nTesting CRUD operations...")
    test_crud() 