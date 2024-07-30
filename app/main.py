from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.controllers import auth_controller, flight_controller, subscription_controller, notification_controller, token_controller
from app.kafka.producer import producer
from app.kafka.consumer import consumer
import asyncio
from schemas.kafka import Message
from contextlib import asynccontextmanager
from app.services.notifier_service import check_flights_update

async def periodic_flight_check():
    while True:
        await check_flights_update()
        await asyncio.sleep(7200)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await producer.start()
    await consumer.start()
    asyncio.create_task(consumer.consume_messages())
    asyncio.create_task(periodic_flight_check())
    yield
    await producer.stop()
    await consumer.stop()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500","*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.include_router(auth_controller.router, prefix="/auth")
app.include_router(token_controller.router, prefix="/token")
# app.include_router(airport_controller.router, prefix="/airports")
app.include_router(flight_controller.router, prefix="/flights")
app.include_router(subscription_controller.router, prefix="/subscriptions")
app.include_router(notification_controller.router, prefix="/notifications")

@app.post("/kafka/produce/")
async def send_message_to_kafka(message: Message):
    try:
        await producer.send_message(message.topic, '['+ message.flight_id+ ']- ' + message.message)
        return {"status": "Message sent to Kafka"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Server is up"}

if __name__ == "__main__":
    print('FastAPI uvicorn launched')
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)