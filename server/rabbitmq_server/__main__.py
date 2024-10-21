import asyncio
import aio_pika
import configparser
import logging
from protobuf.message_pb2 import Request, Response
from datetime import datetime

async def on_request(message: aio_pika.IncomingMessage):
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
            routing_key=message.reply_to
        )
        logging.info(f"Sent response: {response.request_id}, value: {response.response} at time {datetime.now()}")

async def connect_to_rabbitmq(server_settings):
    while True:
        try:
            connection = await aio_pika.connect_robust(server_settings['broker_url'])
            channel = await connection.channel()

            exchange = await channel.declare_exchange(server_settings['exchange_name'], aio_pika.ExchangeType.DIRECT)
            queue = await channel.declare_queue('server_queue')

            await queue.bind(exchange)
            
            logging.info('Server is running and waiting for messages.')

            await queue.consume(on_request)
            await asyncio.Future()
        except (aio_pika.exceptions.AMQPConnectionError, ConnectionError) as e:
            logging.error(f"Connection to broker failed: {e}. Retrying in 5 seconds...")
            await asyncio.sleep(5)


async def main(server_settings):
    await connect_to_rabbitmq(server_settings)

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config.ini')
    server_settings = config['Server']
    logging.basicConfig(level=server_settings['log_level'], filename=server_settings['log_file'])
    asyncio.run(main(server_settings))