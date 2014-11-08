try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='haproxy_test',
    version='0.1',
    description='Toy project to determine correct functionality for Neo4j HA',
    author='Arturo Sevilla',
    author_email='arturosevilla@gmail.com',
    url='',
    install_requires=['Flask'],
    packages=find_packages(exclude=['ez_setup'])
)
