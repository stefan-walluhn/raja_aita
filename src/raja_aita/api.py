from fastapi import FastAPI

from .routers import beacons, summarize, cleanup


api = FastAPI()

api.include_router(beacons.router, prefix="/beacons")
api.include_router(summarize.router, prefix="/summarize")
api.include_router(cleanup.router, prefix="/cleanup")
