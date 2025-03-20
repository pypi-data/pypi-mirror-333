

rsync  -av mains/*.py ${PYTHONPATHDYNAM}/bin/
rsync  -Rav modules/*.{py,pyc} modules/*/*.{py,pyc} ${PYTHONPATHDYNAM}
