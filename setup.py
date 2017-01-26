from setuptools import setup, find_packages

from uaa_client import VERSION


setup(name='cg-django-uaa',
      zip_safe=False,
      version=VERSION,
      description='A cloud.gov UAA authentication backend for Django',
      author='Atul Varma',
      author_email='atul.varma@gsa.gov',
      license='Public Domain',
      url='https://github.com/18F/cg-django-uaa',
      package_dir={'uaa_client': 'uaa_client'},
      packages=find_packages(),
      install_requires=[
          'django>=1.8,<2',
          'PyJWT>=1.4.2',
          'requests>=2.11.0'
      ],
      test_suite='uaa_client.runtests.run_tests',
      tests_require=[
          'httmock>=1.2.5',
      ],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Web Environment',
          'Framework :: Django',
          'Framework :: Django :: 1.8',
          'Framework :: Django :: 1.9',
          'Framework :: Django :: 1.10',
          'Intended Audience :: Developers',
          'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Topic :: Utilities'],
      )
