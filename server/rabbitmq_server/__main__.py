import asyncio
import configparser
import logging
from rabbitmq_server.server import Server


def main():
    config = configparser.ConfigParser()
    config.read('../configs/server_config.ini')
    server_settings = config['Server']
    logging.basicConfig(level=server_settings['log_level'], filename=server_settings['log_file'])

    server = Server(server_settings)
    asyncio.run(server.start())
