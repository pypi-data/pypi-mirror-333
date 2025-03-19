from setuptools import setup
import os

def custom_install():
    print("Running custom installation logic...")
    os.system("echo Custom install script executed")

custom_install()

setup()