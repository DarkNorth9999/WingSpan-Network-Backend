from aiokafka import AIOKafkaConsumer
import asyncio
from app.services.notification_processing import process_notification

class KafkaConsumer:
    def __init__(self, servers, topic):
        self.servers = servers
        self.topic = topic
        # self.group_id = group_id
        self.consumer = None

    async def start(self):
        self.consumer = AIOKafkaConsumer(
            self.topic,
            bootstrap_servers=self.servers,
            # group_id=self.group_id
        )
        await self.consumer.start()
        asyncio.create_task(self.consume_messages())

    async def consume_messages(self):
        try:
            async for message in self.consumer:
                print(f"Received: {message.topic}:{message.partition}:{message.offset}: key={message.key} value={message.value.decode('utf-8')}")
                notification_message = message.value.decode('utf-8')
                cleaned_message = notification_message.replace('[', '').replace(']', '')
                flight_id, message = cleaned_message.split('- ', 1)
                print(f"Received notification for flight: {flight_id}")
                await process_notification(flight_id.strip(), message.strip())
        finally:
            await self.consumer.stop()

    async def stop(self):
        await self.consumer.stop()

kafka_servers = 'localhost:9093'
consumer = KafkaConsumer(servers=kafka_servers, topic='notification')