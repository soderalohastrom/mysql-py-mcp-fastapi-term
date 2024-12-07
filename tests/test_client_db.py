from common.database import DatabaseConnection
from common.models import Client

def test_client_query():
    try:
        with DatabaseConnection() as cursor:
            query = """
            SELECT 
                p.Person_id,
                p.FirstName,
                p.LastName,
                p.DateOfBirth,
                p.DateCreated,
                p.Employer,
                p.MaritalStatus,
                p.Education
            FROM Persons p
            WHERE p.Person_id = 230126
            LIMIT 1
            """
            cursor.execute(query)
            result = cursor.fetchone()
            
            if result:
                client = Client(
                    id=result['Person_id'],
                    first_name=result['FirstName'],
                    last_name=result['LastName'],
                    date_of_birth=result['DateOfBirth'],
                    date_created=result['DateCreated'],
                    employer=result['Employer'],
                    marital_status=result['MaritalStatus'],
                    education=result['Education']
                )
                print("\nClient Data Retrieved:")
                print(f"ID: {client.id}")
                print(f"Name: {client.first_name} {client.last_name}")
                print(f"DOB: {client.date_of_birth}")
                print(f"Created: {client.date_created}")
                print(f"Employer: {client.employer}")
                print(f"Marital Status: {client.marital_status}")
                print(f"Education: {client.education}")
                return True
            else:
                print("No client found with ID 230126")
                return False
                
    except Exception as e:
        print(f"Query failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing client database query...")
    test_client_query() 