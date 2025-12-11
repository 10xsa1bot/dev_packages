"""
Basic Usage Example - Unipile Client

This example demonstrates how to use the Unipile client to fetch LinkedIn profiles.
"""

from dotenv import load_dotenv
load_dotenv()

import sys
sys.path.append('..')

from unipile_api import UnipileAPI


def main():
    print("=" * 60)
    print("Unipile Client - Basic Usage Example")
    print("=" * 60)

    # Initialize API
    print("\n1. Initializing Unipile API...")
    api = UnipileAPI.from_env()

    # Test connection
    print("\n2. Testing connection...")
    if api.test_connection():
        print("✅ Connected to Unipile!")
    else:
        print("❌ Connection failed!")
        print("Make sure UNIPILE_DSN is set in your .env file")
        return

    # You need to provide your account ID
    # Get this from Unipile dashboard
    account_id = input("\n3. Enter your Unipile Account ID: ").strip()

    if not account_id:
        print("❌ Account ID is required")
        return

    # Get own profile
    print(f"\n4. Getting your own profile...")
    result = api.profiles.get_own_profile(account_id=account_id)

    if result['success']:
        profile = result['data']
        print(f"✅ Profile retrieved successfully!")
        print(f"\n   Name: {profile.get('name', 'N/A')}")
        print(f"   Headline: {profile.get('headline', 'N/A')}")
        print(f"   Location: {profile.get('location', 'N/A')}")
        print(f"   Connections: {profile.get('connections', 'N/A')}")
        print(f"   Profile URL: {profile.get('profile_url', 'N/A')}")
    else:
        print(f"❌ Error: {result.get('error')}")
        if result.get('error_detail'):
            print(f"   Details: {result['error_detail']}")

    # Get another user's profile
    print(f"\n5. Getting another user's profile...")
    identifier = input("   Enter LinkedIn username or URL: ").strip()

    if identifier:
        result = api.profiles.get_user_profile(
            account_id=account_id,
            identifier=identifier
        )

        if result['success']:
            profile = result['data']
            print(f"✅ Profile retrieved successfully!")
            print(f"\n   Name: {profile.get('name', 'N/A')}")
            print(f"   Headline: {profile.get('headline', 'N/A')}")
            print(f"   Location: {profile.get('location', 'N/A')}")
            print(f"   Connections: {profile.get('connections', 'N/A')}")

            # Show experience if available
            if profile.get('experience'):
                print(f"\n   Experience:")
                for exp in profile['experience'][:3]:  # Show first 3
                    print(f"     - {exp.get('title', 'N/A')} at {exp.get('company', 'N/A')}")
        else:
            print(f"❌ Error: {result.get('error')}")
            if result.get('error_detail'):
                print(f"   Details: {result['error_detail']}")
    else:
        print("   Skipped")

    print("\n" + "=" * 60)
    print("Example completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
