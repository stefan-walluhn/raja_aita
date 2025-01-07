from fastapi import FastAPI

from .routers import beacons, summarize


api = FastAPI()

api.include_router(beacons.router, prefix="/beacons")
api.include_router(summarize.router, prefix="/summarize")
