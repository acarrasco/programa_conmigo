PROGRAM_TO_TEST=$1

for I in $(seq 7)
do
    if python $PROGRAM_TO_TEST < cases/input_0$I.txt | diff cases/output_0$I.txt -
    then
        echo case $I ok
    else
        echo error in case $I
    fi
done