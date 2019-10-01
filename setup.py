from setuptools import find_packages, setup

setup(
    name="guess-loi-prepare",
    version="0.1.0",
    author="Romualdi's Lab",
    author_email=[
        "paolo.cavei@gmail.com",
        "enrica.calura@gmail.com",
        "gbrsales@gmail.com",
    ],
    description="Tools to prepare data for Guess-LOI",
    packages=find_packages(),
    install_requires=[
    ],
    entry_points={
        'console_scripts': [
            'download_annotation=guess_loi_prep.commands.annotation:main',
        ],
    }
)
