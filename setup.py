from setuptools import setup
from pip.req import parse_requirements
from pip.download import PipSession
import glob
import sys
import os


def setup_requirements(pattern='requirements/*.txt', install_combined=False):
    """
    Parse a glob of requirements and return a dictionary of setup() options.
    Any files that are not a standard option name (ie install, tests, setup) are added to extras_require with their
    basename minus ext. An extra key is added to extras_require: 'all', that contains all distinct reqs combined.

    If you're running this for a Docker build, set install_combined=True.
    This will set install_requires to all distinct reqs combined.

    Create a dictionary that holds your options to setup() and update it using this.
    Pass that as kwargs into setup(), viola

    :param str pattern: Glob pattern to find requirements files
    :param bool install_combined: Set True to set install_requires to extras_require['all']
    :return dict: Dictionary of parsed setup() options
    """
    key_map = {
        'install.txt': 'install_requires',
        'tests.txt': 'tests_require',
        'setup.txt': 'setup_requires',
    }
    ret = {v: [] for v in key_map.values()}
    extras = ret['extras_require'] = {}
    all = set()
    session = PipSession()

    for full_fn in glob.glob(pattern):
        # Parse file
        reqs = [str(r.req) for r in parse_requirements(full_fn, session=session)]
        all.update(reqs)

        fn = os.path.basename(full_fn)
        key = key_map.get(fn)
        if key:
            ret[key].extend(reqs)
        else:
            # Remove extension
            key, _ = os.path.splitext(fn)
            extras[key] = reqs

    if 'all' not in extras:
        extras['all'] = list(all)

    return ret


__version__ = 'unknown'  # This is ovewritten by the execfile below
exec(open('meinconf/_version.py').read())


conf = dict(
    name='meinconf',
    description='Configuration for all',
    url='http://github.com/akatrevorjay/meinconf',
    author='Trevor Joynson',
    author_email='pypi@trevor.joynson.io',
    license='GPL',
    # keywords=[],
    # classifiers=[],

    version=__version__,
    packages=['meinconf', 'meinconf._flask'],
)
conf.update(setup_requirements(install_combined=True))

conf['download_url'] = '{url}/tarball/{version}'.format(**conf)

needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
if needs_pytest:
    conf['setup_requires'].append('pytest-runner')

setup(**conf)
