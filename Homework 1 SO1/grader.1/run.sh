#! /bin/sh

tar -czf so1.2017.2018.1.1464722.tgz ../program02.py
rm all.tgz 2>/dev/null
cd ../p_all
tar -czf ../grader.1/all.tgz *
cd ../grader.1
bash grader.1.sh 2
