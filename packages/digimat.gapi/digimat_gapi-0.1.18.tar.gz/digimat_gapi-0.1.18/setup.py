from setuptools import setup, find_packages

setup(
    name='digimat.gapi',
    version='0.1.18',
    description='Digimat Google API tools',
    # namespace_packages=['digimat'],
    author='Frederic Hess',
    author_email='fhess@st-sa.ch',
    url='http://www.digimat.ch',
    license='PSF',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'gspread',
        'strict_rfc3339',
        'google-auth',
        'google-auth-oauthlib',
        'requests',
        # 'httplib2',
        # 'oauth2client',
        # 'google-api-python-client',
        'setuptools'
    ],
    dependency_links=[
        ''
    ],
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
    ],
    zip_safe=False)
