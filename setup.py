import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='syslog_analytics',
                 version='0.0.2',
                 entry_points={
                     'console_scripts': ['syslog_analytics=syslog_analytics.main:main'],
                 },
                 description='Script to extract data from DNS logs.',
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 url='https://github.com/lraulin/syslog_analytics',
                 author='Lee Raulin',
                 author_email='lee.raulin.ctr@dot.gov',
                 license='MIT',
                 packages=setuptools.find_packages(),
                 classifiers=[
                     "Programming Language :: Python :: 3",
                     "License :: OSI Approved :: MIT License",
                     "Operating System :: OS Independent",
                 ],
                 )
