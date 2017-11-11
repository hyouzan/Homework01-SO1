#! /bin/bash

if [ ! \( -f all.tgz \) ]
then
    echo Manca il file all.tgz, impossibile proseguire
    exit
fi
res=`ls -1 so1.????.????.?.*.tgz 2> /dev/null | awk -F. '$2 == "2017" && $3 == "2018" && $4 == "1" && $5 ~ /[0-9]{5,}/ {print}' | wc -l | awk '{print $1}'`
if [ $res -eq 0 ]
then
    echo Manca il file con le soluzioni, impossibile proseguire
    exit
fi
if [ $res -gt 1 ]
then
    echo Troppi file con le soluzioni, impossibile proseguire
    exit
fi

max_hw=6
max_minutes=10
sampling=5

rm -fr program* check grade*py *out* __pycache__ log
programs_all=`tar tzf all.tgz | awk -F. 'NF > 2{print $1}' | sort | uniq`
max_punteggio=`echo $max_hw $programs_all | awk '{printf("%lf", $1/(NF - 1));}'`
if [ $# -eq 1 ]
then
    tar --wildcards -xz --file=all.tgz grade`printf "%02d" $1`.py check/grade`printf "%02d" $1`*
    programs=program`printf "%02d" $1`.py
    tar --wildcards -xz --file=`ls so1*.tgz` $programs
    test -f $programs || { echo "La soluzione all'esercizio "$1" non e' presente nel file "so1*.tgz; exit; }
else
    tar xfz all.tgz 
    tar xfz `ls so1*.tgz`
fi

tot=0
for grade_check in $programs_all
do
    grade=`echo $grade_check | sed -e 's/check\///g'`
    num_grade=`echo $grade | sed -e 's/grade0//g'`
    if [ ! \( -f $grade.py \) ]
    then
	echo -e "\t"$num_grade" non presente!"
	echo Risultato per esercizio $num_grade: 0"/"$max_punteggio
	continue
    fi
    ok=0
    #onde evitare furbate
    how_many=`ls -1 $grade_check* | wc -l`
#     permutation=`python3 <<EOF | sed -e 's/[^0-9 ]//g'
# from random import *
# ok = False
# while not(ok):
#     seq = list(range(1, $how_many + 1))
#     shuffle(seq)
#     ok = True
#     for i in range(len(seq)):
#         if seq[i] == i + 1:
#             ok = False
#             break
# print(seq)
# EOF`
#     mkdir tmp
#     mv check/${grade}* tmp
#     i_old=1
#     for i in $permutation
#     do
# 	mv tmp/$grade.out.$i_old check/$grade.out.$i
# 	((i_old++))
#     done
#     rm -r tmp
    for ((i = 1; i <= how_many; i++))
    do
	timeout $((max_minutes*60)) python3 $grade.py $((i - 1)) > $grade.py.out.$((i - 1)) 2>&1
	exit_status=$?
	if [ $exit_status -eq 124 ]
	then
	    echo -e "\ttest $i fallito per timeout!"
	    continue
	fi
	# i_old=`echo $permutation | awk -v i=$i '{print $i}'`
	test -f $grade.out.$i || { echo -e "Manca $grade.out.$i\n\ttest $i fallito (probabile crash)!"; continue; }
	diff -q $grade.out.$i check/$grade.out.$i && { ((ok++)); echo -e "\ttest $i ok!"; } || echo -e "\ttest $i fallito!"
	# diff -q $grade.out.$i check/$grade.out.$i_old && { ((ok++)); echo -e "\ttest $i ok!"; } || echo -e "\ttest $i fallito!"
    done
    res=`echo $ok $how_many $max_punteggio | awk '{printf("%lf", ($1/$2)*$3)}'`
    echo Risultato per esercizio $num_grade: $res"/"$max_punteggio
    tot=`echo $res $tot | awk '{printf("%lf", $1 + $2)}'`
done
if [ $# -ne 1 ]
then
    echo -e "\n\nRISULTATO INTERO HOMEWORK: $tot/$max_hw\n\n"
fi
