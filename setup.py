from setuptools import setup, find_packages

setup(
    name='open-singly',
    version='0.1',
    description='IDjango package for integration with Singly API (uses open-singly)',
    author='Venelin Stoykov',
    author_email='venelin@magicsolutions.bg',
    url='https://github.com/MagicSolutions/django-singly',
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
      'Django',
      'django-json-field',
      'open_singly',
    ],
    classifiers=[
      'Development Status :: 4 - Beta',
      'Environment :: Web Environment',
      'Intended Audience :: Developers',
      'Operating System :: OS Independent',
      'Programming Language :: Python',
    ]
)