#!/bin/bash

source /usr/local/nemo_cvs/NEMORC.sh


rsync  -av mains/*.py ${NEMO}/py/bin/
rsync  -Rav modules/*.{py,pyc} modules/*/*.{py,pyc} ${NEMO}/py
