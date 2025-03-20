from easunpy.async_isolar import AsyncISolar
import asyncio

async def main():
   isolar = AsyncISolar("none", "none")
   response = await isolar.get_all_data()
   
if __name__ == "__main__":
   asyncio.run(main())