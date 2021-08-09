import setuptools

setuptools.setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='portfolio-manager',
    url='https://github.com/AeroStarCreations/PortfolioManager',
    author='Nathan Balli',
    author_email='AeroStarCreations1@gmail.com',
    # Needed to actually package something
    packages=setuptools.find_packages(),
    # Needed for dependencies
    install_requires=[],
    # *strongly* suggested for sharing
    version=0.1,
    # The license can be anything you like
    license='MIT',
    description='Package for balanced investing',
    # You will also need a readme eventually (there will be a warning)
    # long_description=open('README.txt').read()
    # Other
    zip_safe=False
)