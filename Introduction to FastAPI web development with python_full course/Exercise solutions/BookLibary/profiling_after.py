import time
import asyncio
import httpx

async def profile_book_search():
    async with httpx.AsyncClient(base_url="http://127.0.0.1:8000") as client:

        # Step 1 — Register admin user (safe to run even if already exists)
        await client.post(
            "/api/v1/auth/register",
            json={
                "username": "admin_user",
                "email": "admin@example.com",
                "password": "adminpass123",
                "role": "admin"
            }
        )

        # Step 2 — Login to get token
        login = await client.post(
            "/api/v1/auth/token",
            data={"username": "admin_user", "password": "adminpass123"}
        )

        if "access_token" not in login.json():
            print(f"Login failed: {login.json()}")
            return

        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        print("=" * 40)
        print("WITH CACHING")
        print("=" * 40)

        times = []
        for i in range(10):
            start = time.time()
            response = await client.get(
                "/api/v1/books/",
                params={"limit": 10},
            )
            elapsed = time.time() - start
            times.append(elapsed)
            label = "CACHE MISS" if i == 0 else "CACHE HIT "
            print(f"Request {i+1} [{label}]: {response.status_code} - {elapsed:.4f}s")

        print(f"\nTotal:   {sum(times):.4f}s")
        print(f"Average: {sum(times)/len(times):.4f}s")
        print(f"Fastest: {min(times):.4f}s")
        print(f"Slowest: {max(times):.4f}s")

if __name__ == "__main__":
    asyncio.run(profile_book_search())