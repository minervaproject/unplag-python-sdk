from setuptools import setup

setup(name='unicheck',
      version='1.0.6',
      description='Unicheck API python client',
      url='https://unicheck.com',
      author='Oleg Mykolaichenko',
      author_email='mukolaichenko@gmail.com',
      license='Apache 2.0 License',
      packages=['unicheck'],
      install_requires=[
            'requests>=2.12.3',
            'requests_oauthlib>=0.6.2',
            'msgpack>=0.5.6',
            'responses>=0.5.1',
      ],
      test_suite='tests',
      zip_safe=False)
