"""
Basic Usage Example - Supabase Client

This example demonstrates basic CRUD operations using the Supabase client.
"""

from dotenv import load_dotenv
load_dotenv()

from supabase_api import SupabaseAPI


def main():
    print("=" * 60)
    print("Supabase Client - Basic Usage Example")
    print("=" * 60)

    # Initialize API
    print("\n1. Initializing Supabase API...")
    api = SupabaseAPI.from_env()

    # Test connection
    print("\n2. Testing connection...")
    if api.test_connection():
        print("✅ Connected to Supabase!")
    else:
        print("❌ Connection failed!")
        return

    # Get a table service
    print("\n3. Working with 'users' table...")
    users = api.table('users')

    # CREATE - Create a new user
    print("\n4. Creating a new user...")
    result = users.create({
        'name': 'John Doe',
        'email': 'john.doe@example.com',
        'age': 30,
        'status': 'active'
    })

    if result['success']:
        print(f"✅ User created: {result['data']}")
        user_id = result['data'][0]['id']
    else:
        print(f"❌ Error: {result['error']}")
        return

    # READ - Get all users
    print("\n5. Getting all users (limit 10)...")
    result = users.get_all(limit=10, order_by='created_at')

    if result['success']:
        print(f"✅ Found {len(result['data'])} users")
        for user in result['data'][:3]:  # Show first 3
            print(f"   - {user.get('name')} ({user.get('email')})")
    else:
        print(f"❌ Error: {result['error']}")

    # FIND - Find specific users
    print("\n6. Finding active users...")
    result = users.find({'status': 'active'}, limit=5)

    if result['success']:
        print(f"✅ Found {len(result['data'])} active users")
    else:
        print(f"❌ Error: {result['error']}")

    # SEARCH - Search by text
    print("\n7. Searching for 'John'...")
    result = users.search('name', 'John', limit=5)

    if result['success']:
        print(f"✅ Found {len(result['data'])} users matching 'John'")
    else:
        print(f"❌ Error: {result['error']}")

    # UPDATE - Update a user
    print(f"\n8. Updating user {user_id}...")
    result = users.update(user_id, {
        'name': 'John Updated',
        'age': 31
    })

    if result['success']:
        print(f"✅ User updated: {result['data']}")
    else:
        print(f"❌ Error: {result['error']}")

    # COUNT - Count users
    print("\n9. Counting total users...")
    result = users.count()

    if result['success']:
        print(f"✅ Total users: {result['count']}")
    else:
        print(f"❌ Error: {result['error']}")

    # EXISTS - Check if exists
    print("\n10. Checking if email exists...")
    result = users.exists({'email': 'john.doe@example.com'})

    if result['success']:
        if result['exists']:
            print(f"✅ Email exists in database")
        else:
            print(f"ℹ️  Email not found")
    else:
        print(f"❌ Error: {result['error']}")

    # DELETE - Delete a user
    print(f"\n11. Deleting user {user_id}...")
    result = users.delete(user_id)

    if result['success']:
        print(f"✅ User deleted")
    else:
        print(f"❌ Error: {result['error']}")

    print("\n" + "=" * 60)
    print("Example completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
