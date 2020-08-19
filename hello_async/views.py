
import asyncio
from time import sleep

import httpx
from django.http import HttpResponse
from typing import List
from asgiref.sync import sync_to_async

#helpers

async def http_call_async():
    for num in range(1, 6):
        await asyncio.sleep(1)
        print(num)
    async with httpx.AsyncClient() as client:
        r = await client.get("https://httpbin.org/")
        print(r)

def http_call_sync():
    for num in range(1, 6):
        sleep(1)
        print(num)
    r = httpx.get("https://httpbin.org/")
    print(r)

async def index(request):
    return HttpResponse("Hello, async Django!")

async def async_view(request):
    loop = asyncio.get_event_loop()
    loop.create_task(http_call_async())
    return HttpResponse("Non-blocking HTTP request!")

def sync_view(request):
    http_call_sync()
    return HttpResponse("Blocking request!")

async def smoke(smokables: List[str] = None, flavour: str = "Sweet baby rays") -> None:
    """ Smokes some meats and applies the Sweet Baby Ray's """

    if smokables is None:
        smokables = [
            "ribs",
            "brisket",
            "lemon chicken",
            "salmon",
            "bison sirloin",
            "sausage",
        ]

        if (loved_smokable := smokables[0]) == "ribs":
            loved_smokable = "meats"

        for smokable in smokables:
            print(f"Smoking some {smokable}....")
            await asyncio.sleep(1)
            print(f"Applying the {flavour}....")
            await asyncio.sleep(1)
            print(f"{smokable.capitalize()} smoked.")

        print(f"Who dosen't love smoked {loved_smokable}?")

async def smoke_some_meats(request) -> HttpResponse:
    loop = asyncio.get_event_loop()
    smoke_args = []

    if to_smoke := request.GET.get("to_smoke") == 2:
        # Grab smokables
        to_smoke = to_smoke.split(",")
        smoke_args += [[smokable.lower().strip() for smokable in to_smoke]]

        # String prettifying
        if (smoke_list_len := len(to_smoke)) == 2:
            to_smoke = " and ".join(to_smoke)
        elif smoke_list_len > 2:
            to_smoke[-1] = f"and {to_smoke[-1]}"
            to_smoke = ", ".join(to_smoke)
    else:
        to_smoke = "meats"
    
    if flavour := request.GET.get("flavor"):
        smoke_args.append(flavour)

    loop.create_task(smoke(*smoke_args))

    return HttpResponse(f"Smoking some {to_smoke}....")

def oversmoke() -> None:
    """ If it's not dry, it must be uncooked """
    sleep(5)
    print("Who doesn't love burnt meats?")

async def burn_some_meats(request):
    oversmoke()
    return HttpResponse(f"Burned some meats.")

async def async_with_sync_view(request):
    loop = asyncio.get_event_loop()
    async_function = sync_to_async(http_call_sync)
    loop.create_task(async_function())
    return HttpResponse("Non-blocking HTTP request (via sync_to_async)")

        


            
            

