from guess_loi_prep.download import download


def download_annotation(species, ensembl_version=None):
    release = "release-%s/gtf" % ensembl_version if ensembl_version else "current_gtf"
    url = "ftp://ftp.ensembl.org/pub/%s/%s/*.chr.gtf.gz" % (release, species)
    download(url, species + '.chr.gtf.gz')
