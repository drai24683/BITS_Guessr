import httpx

from app.services.database import supabase


BUCKET_NAME = "challenges"


async def migrate_images():
    response = (
        supabase
        .table("challenges")
        .select("id, image_path")
        .order("id")
        .execute()
    )

    challenges = response.data

    print(f"Found {len(challenges)} challenges.")

    uploaded = 0
    skipped = 0
    failed = 0

    async with httpx.AsyncClient(
        timeout=30,
        follow_redirects=True
    ) as client:

        for challenge in challenges:

            challenge_id = challenge["id"]
            image_path = challenge["image_path"]

            # Already migrated
            if image_path.startswith("challenges/"):
                print(f"Challenge {challenge_id}: already migrated, skipping.")
                skipped += 1
                continue

            if not image_path:
                print(f"Challenge {challenge_id}: no image URL, skipping.")
                failed += 1
                continue

            storage_path = f"challenges/{challenge_id}.jpg"

            try:
                # Download image from Google
                image_response = await client.get(image_path)
                image_response.raise_for_status()

                image_bytes = image_response.content

                # Upload to Supabase Storage
                supabase.storage \
                    .from_(BUCKET_NAME) \
                    .upload(
                        storage_path,
                        image_bytes,
                        {
                            "content-type": "image/jpeg",
                            "upsert": False
                        }
                    )

                # Only update DB after successful upload
                supabase \
                    .table("challenges") \
                    .update({
                        "image_path": storage_path
                    }) \
                    .eq("id", challenge_id) \
                    .execute()

                print(f"Challenge {challenge_id}: ✓ migrated")
                uploaded += 1

            except Exception as e:
                print(f"Challenge {challenge_id}: ✗ failed — {e}")
                failed += 1

    print()
    print("Migration complete.")
    print(f"Uploaded: {uploaded}")
    print(f"Skipped:  {skipped}")
    print(f"Failed:   {failed}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(migrate_images())