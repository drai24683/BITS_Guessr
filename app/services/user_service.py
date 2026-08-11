from app.models.user import User
from app.services.database import supabase


async def create_user(
    user_id,
    username: str,
    display_name: str,
    email: str
):
    try:
        response = (
            supabase
            .table("users")
            .insert({
                "id": user_id,
                "username": username,
                "display_name": display_name,
                "email": email
            })
            .execute()
        )

        data = response.data[0]

        user = User(
            data["id"],
            data["username"],
            data["display_name"],
            data["email"]
        )

        print(
            f"User created with user_id: {user.id}"
        )

        return user

    except Exception as e:
        raise RuntimeError(
            f"Failed to create user: {e}"
        ) from e


async def load_user(user_id):

    try:
        response = (
            supabase
            .table("users")
            .select("*")
            .eq("id", user_id)
            .execute()
        )

        if not response.data:
            print(
                f"No user found with user_id: {user_id}"
            )
            return None

        data = response.data[0]

        user = User(
            data["id"],
            data["username"],
            data["display_name"],
            data["email"]
        )

        print(
            f"User with user_id: {user_id} "
            f"fetched from database"
        )

        return user

    except Exception as e:
        raise RuntimeError(
            f"Failed to load user: {e}"
        ) from e


async def update_user(user: User):

    try:
        (
            supabase
            .table("users")
            .update({
                "username": user.username,
                "display_name": user.display_name
            })
            .eq("id", user.id)
            .execute()
        )

        print(f"User with user_id: {user.id} updated in database")

        return user

    except Exception as e:
        raise RuntimeError(
            f"Failed to update user: {e}"
        ) from e