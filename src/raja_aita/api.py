from fastapi import FastAPI

from .routers import beacons


api = FastAPI()

api.include_router(beacons.router, prefix="/beacons")
