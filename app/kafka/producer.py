from aiokafka import AIOKafkaProducer
import asyncio

class KafkaProducer:
    def __init__(self, servers):
        self.servers = servers
        self.producer = None

    async def start(self):
        self.producer = AIOKafkaProducer(bootstrap_servers=self.servers)
        await self.producer.start()

    async def send_message(self, topic, message):
        try:
            await self.producer.send_and_wait(topic, message.encode('utf-8'))
            print(f"Sent message to {topic}")
        except Exception as e:
            print(f"Failed to send message: {e}")

    async def stop(self):
        await self.producer.stop()

kafka_servers = 'localhost:9093'
producer = KafkaProducer(servers=kafka_servers)