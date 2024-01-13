from setuptools import setup

setup(name='featuredeploy',
      version='1.0.6',
      description='Test single features',
      url='http://github.com/resmio/resmio/featuredeploy',
      author='Resmio Team',
      author_email='info@resmio.com',
      packages=['featuredeploy'],
      scripts=['featuredeploy/featuredeploy'],
      package_data={
          'featuredeploy': ['deploy.sh'],
      },
      install_requires=[
          'pytz>=2016.7',
          'python-digitalocean==1.9.0',
          'pycryptodome==3.19.1'
      ],
      zip_safe=False)
