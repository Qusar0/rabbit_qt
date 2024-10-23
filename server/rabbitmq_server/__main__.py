import asyncio
import aio_pika
import configparser
import logging
from protobuf.message_pb2 import Request, Response
from datetime import datetime

class Server:
    def __init__(self, server_settings):
        self.server_settings = server_settings
        self.connection = None
        self.channel = None

    async def on_request(self, message: aio_pika.IncomingMessage):
        async with message.process():
            request = Request()
            request.ParseFromString(message.body)

            logging.info(f"Received request: {request.request_id}, value: {request.request} with timeout: {request.proccess_time_in_seconds} at time {datetime.now()}")

            if request.proccess_time_in_seconds > 0:
                await asyncio.sleep(request.proccess_time_in_seconds)

            response = Response(
                request_id=request.request_id,
                response=request.request * 2
            )

            await message.channel.basic_publish(
                body=response.SerializeToString(),
                exchange='',
                routing_key=message.reply_to,
            )
            logging.info(f"Sent response: {response.request_id}, value: {response.response} at time {datetime.now()}")

    async def connect_to_rabbitmq(self):
        while True:
            try:
                self.connection = await aio_pika.connect_robust(self.server_settings['broker_url'])
                self.channel = await self.connection.channel()

                exchange = await self.channel.declare_exchange(self.server_settings['exchange_name'], aio_pika.ExchangeType.DIRECT)
                queue = await self.channel.declare_queue('server_queue')

                await queue.bind(exchange)

                logging.info('Server is running and waiting for messages.')

                await queue.consume(self.on_request)
                await asyncio.Future()
            except (aio_pika.exceptions.AMQPConnectionError, ConnectionError) as e:
                logging.error(f"Connection to broker failed: {e}. Retrying in 5 seconds...")
                await asyncio.sleep(5)

    async def start(self):
        await self.connect_to_rabbitmq()

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config.ini')
    server_settings = config['Server']
    logging.basicConfig(level=server_settings['log_level'], filename=server_settings['log_file'])

    server = Server(server_settings)
    asyncio.run(server.start())
