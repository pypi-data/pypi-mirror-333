from setuptools import setup, find_packages

setup(
    name="node-db",
    packages=find_packages(
        include=["node_db_package", "node_db_package.*"]
    ),  # This will include all subpackages
    version="0.1.2",
    author="Node",
    description="The shared database for Node",
    install_requires=[
        "sqlalchemy>=2.0.0",
        "python-dotenv>=1.0.0",
        "psycopg2-binary>=2.9.0",
        # other dependencies
    ],
)
