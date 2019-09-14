from setuptools import setup

# List of dependencies installed via `pip install -e .`
# by virtue of the Setuptools `install_requires` value below.
requires = [
    'pyramid',
    'pyramid-chameleon',
    'python-twitch-client',
    'twitchircpy',
    'deform',
    'waitress',
]

setup(
    name='openssakdook',
    install_requires=requires,
    entry_points={
        'paste.app_factory': [
            'main = openssakdook:main'
        ],
    },
)