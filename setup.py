from setuptools import find_packages, setup

setup(
    name='pypackager-lib',

    packages=['lib', 'lib/Factory', 'lib/JsonParser', 'lib/packager', 'lib/YamlParser',
              'lib/packager/creator', 'lib/packager/objectinspector'],
    version='0.2.4',

    description='Serializer/Deserializer',
    author='Me',
    license='MIT',
    python_requires='>=3.8',
)

import os
from pathlib import Path

home = str(Path.home())

os.system('rm -rf ~/pypackager-lib')
os.system('mkdir ~/pypackager-lib')
os.system('cp -a . ~/pypackager-lib')

os.system('chmod +x ~/pypackager-lib/cli/redump.py')
with open(home + '/.bashrc', 'a') as file:
    file.write("alias redump='" + "~/pypackager-lib/cli/redump.py'" + '\n')

