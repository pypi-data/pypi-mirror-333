from logging import getLogger

from fastapi import FastAPI

logger = getLogger()

app = FastAPI()


@app.get("/")
def root() -> dict:
    logger.info("The root endpoint was invoked.")
    return {"message": "Hello BMA"}


@app.get("/calculate")
def calculate() -> dict:
    logger.info("The calculate endpoint was invoked.")
    return {"message": "Calculate"}


@app.get("/results")
def results() -> dict:
    logger.info("The results endpoint was invoked.")
    return {"message": "Show results"}
