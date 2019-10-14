from setuptools import find_packages
from distutils.core import setup

with open('README.md') as f:
    ld = f.read()

def _get_required():
    output = []
    with open('requirements/requirements.txt') as f:
        for line in f.readlines():
            line = line.strip()
            if line.startswith('#') or line.startswith('-'):
                continue
            if not line:
                continue
            output.append(line)
    return output


setup(
    name='hivemind_tasks',
    version='0.0.1',
    packages=['hivemind_tasks'],
    license='MIT',
    description='Tasks management using the hivemind system as the backend',
    author='',
    long_description=ld,
    long_description_content_type="text/markdown",
    url = 'https://github.com/mccartnm/hivemind_tasks',
    author_email='mccartneyworks@gmail.com',
    keywords=[
        'backend',
        'fault-tolerant',
        'micro-service',
        'nodes',
        'abstract',
        'management',
        'tasks'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
    ],
    install_requires=_get_required(),
)
