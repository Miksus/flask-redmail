from setuptools import setup, find_packages
import versioneer

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="Flask-Redmail",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author="Mikael Koli",
    author_email="koli.mikael@gmail.com",
    url="https://github.com/Miksus/flask-redmail.git",
    packages=find_packages(),
    description="Email sending for Flask",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Communications :: Email',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
     ],
     include_package_data=True, # for MANIFEST.in
     python_requires='>=3.6.0',

    install_requires = [
        'Flask',
        'redmail'
    ],
)
