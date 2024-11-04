from setuptools import setup, find_packages
from setuptools.command.build_py import build_py
import os
import subprocess

class CustomBuild(build_py):
    def run(self):
        ui_dir = './src/ui/'
        for ui_file in os.listdir(ui_dir):
            if ui_file.endswith('.ui'):
                py_file = os.path.join(ui_dir, f"{os.path.splitext(ui_file)[0]}UI.py")
                ui_file_path = os.path.join(ui_dir, ui_file)
                subprocess.check_call(['pyuic5', ui_file_path, '-o', py_file])

        proto_dir = '../protobufs/'
        for proto_file in os.listdir(proto_dir):
            if proto_file.endswith('.proto'):
                proto_path = os.path.join(proto_dir, proto_file)
                subprocess.check_call(['protoc', f'--proto_path={proto_dir}', '--python_out=./src/protobuf/', proto_path])

        super().run()

setup(
    name='rabbitmq_client',
    version='1.0.0',
    author='R&EC SPb ETU',
    author_email='info@nicetu.spb.ru',
    url='http://nicetu.spb.ru',
    description='Работа с брокером сообщений, клиентская часть',
    long_description="",
    zip_safe=False,
    packages=find_packages(),
    cmdclass={'build_py': CustomBuild},
    install_requires=[
        'pika',
        'PyQt5',
        'protobuf==3.20',
    ],
    entry_points={
        'console_scripts': [
            'client_rabbitmq=src.__main__:main'
        ]
    }
)