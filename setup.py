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
        "pysam"
    ],
    entry_points={
        'console_scripts': [
            'download_annotation=guess_loi_prep.commands.annotation:main',
            'download_genome=guess_loi_prep.download_genome:main',
            'download_chromosome_variants=guess_loi_prep.download_variants:main',
            'filter_gtf=guess_loi_prep.filter_gtf:filter_gtf',
            'filter_vcfs=guess_loi_prep.filter_vcf:filter_vcfs',
            'split_variants=guess_loi_prep.variant_selection:create_vcf_for_brew_loi'
        ],
    }
)
