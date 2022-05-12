import time
import asyncio


dates = ["1", "2", "3", "4", "5", "6"]
tic = time.perf_counter()

async def fetchData(url):
    print("the url", url)
    url = "Woula"
    time.sleep(2)
    return url

def principal(dates):

    for date in dates:
        url = f"hello: {date}"

        print(f"Start {date}")
        
        task = asyncio.create_task(fetchData(url))

        print(f"End {date}")

    print(f"{time.perf_counter() - tic:0.1f} seconds")

if __name__ == "__main__":
    principal(dates)






