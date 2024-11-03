from setuptools import setup
from setuptools.command.build_py import build_py
import os
import subprocess

class CustomBuild(build_py):
    def run(self):
        proto_dir = '../protobufs/'
        for proto_file in os.listdir(proto_dir):
            if proto_file.endswith('.proto'):
                proto_path = os.path.join(proto_dir, proto_file)
                subprocess.check_call(['protoc', f'--proto_path={proto_dir}', '--python_out=./protobuf/', proto_path])

        super().run()
setup(
    name='rabbitmq_server',
    version='1.0.0',
    author='R&EC SPb ETU',
    author_email='info@nicetu.spb.ru',
    url='http://nicetu.spb.ru',
    description='Работа с брокером сообщений, серверная часть',
    long_description="",
    zip_safe=False,
    packages=['rabbitmq_server'],
    cmdclass={'build_py': CustomBuild}
)
