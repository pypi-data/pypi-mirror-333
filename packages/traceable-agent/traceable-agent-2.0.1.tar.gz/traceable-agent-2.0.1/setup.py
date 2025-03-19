# pylint: skip-file
import os
from setuptools import setup, find_packages, Extension

exec(open('src/traceableai/version.py').read())

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="traceable-agent",
    version=__version__,
    author="Traceable.ai",
    description="Traceable.ai Python Agent",
    url="https://traceable.ai",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    include_package_data=True,
    python_requires=">=3.8",
    ext_modules=[
        # this option will let wheel builder know to package c extensions when ran from CI. No effect for source tar installs
        Extension(
            name='traceableai.filter._libtraceable',
            sources=[],
            optional=os.environ.get('CIBUILDWHEEL', '0') != '1'
        )
    ],
    install_requires=[
        "opentelemetry-api==1.30.0",
        "opentelemetry-exporter-otlp==1.30.0",
        "opentelemetry-instrumentation==0.51b0",
        "opentelemetry-instrumentation-aiohttp-client==0.51b0",
        "opentelemetry-instrumentation-boto==0.51b0",
        "opentelemetry-instrumentation-botocore==0.51b0",
        "opentelemetry-instrumentation-wsgi==0.51b0",
        "opentelemetry-instrumentation-fastapi==0.51b0",
        "opentelemetry-instrumentation-flask==0.51b0",
        "opentelemetry-instrumentation-mysql==0.51b0",
        "opentelemetry-instrumentation-psycopg2==0.51b0",
        "opentelemetry-instrumentation-requests==0.51b0",
        "opentelemetry-instrumentation-grpc==0.51b0",
        "opentelemetry-instrumentation-django==0.51b0",
        "opentelemetry-instrumentation-aws-lambda==0.51b0",
        "opentelemetry-propagator-b3==1.30.0",
        "opentelemetry-proto==1.30.0",
        "opentelemetry-sdk==1.30.0",
        "opentelemetry-util-http==0.51b0",
        "google>=3.0.0",
        "pyyaml",
        "protobuf",
        "psutil",
        "distro",
        "cffi",
        "setuptools",
        "jaraco.text",
        "platformdirs"
    ],
    entry_points={
        'console_scripts': [
            'traceableai-instrument = traceableai.autoinstrumentation.wrapper:run',
        ],
    }
)
