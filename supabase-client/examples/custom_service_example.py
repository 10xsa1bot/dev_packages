"""
Custom Service Example

This example shows how to create and use custom services
for your specific tables.
"""

from dotenv import load_dotenv
load_dotenv()

from supabase_api import SupabaseAPI


def main():
    print("=" * 60)
    print("Supabase Client - Custom Service Example")
    print("=" * 60)

    # Initialize API
    api = SupabaseAPI.from_env()

    # Using the built-in Users Service
    print("\n1. Using built-in UsersService...")

    # Create a user
    result = api.users.create_user(
        email='testuser@example.com',
        username='testuser',
        first_name='Test',
        last_name='User'
    )

    if result['success']:
        print(f"✅ User created: {result['data']}")

    # Check if email exists
    result = api.users.email_exists('testuser@example.com')

    if result['exists']:
        print(f"✅ Email exists in database")

    # Get user by email
    result = api.users.get_by_email('testuser@example.com')

    if result['success'] and result['data']:
        user = result['data'][0] if isinstance(result['data'], list) else result['data']
        print(f"✅ Found user: {user.get('username')}")

        # Update user status
        if 'id' in user:
            result = api.users.update_user_status(user['id'], 'verified')

            if result['success']:
                print(f"✅ User status updated to verified")

    # Get active users
    result = api.users.get_active_users(limit=5)

    if result['success']:
        print(f"✅ Found {len(result['data'])} active users")

    # Search users
    result = api.users.search_users('test', limit=10)

    if result['success']:
        print(f"✅ Search found {len(result['data'])} users")

    print("\n" + "=" * 60)
    print("Example completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
