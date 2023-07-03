import setuptools

with open('README.md') as rm:
    long_description = rm.read()

setuptools.setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='portfolio-manager-nb',
    url='https://github.com/AeroStarCreations/PortfolioManager',
    author='Nathan Balli',
    author_email='AeroStarCreations1@gmail.com',
    # Needed to actually package something
    packages=setuptools.find_packages(where='src'),
    package_dir={'': 'src'},
    # Needed for dependencies
    install_requires=[],
    # *strongly* suggested for sharing
    version=0.1.1,
    # The license can be anything you like
    license='MIT',
    description='Package for balanced investing',
    # You will also need a readme eventually (there will be a warning)
    long_description=long_description,
    long_description_content_type='text/markdown',
    # Other
    zip_safe=False,
    python_requires='>=3.5'
)
