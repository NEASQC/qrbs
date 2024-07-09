#!/bin/sh


#Funciones
####################################################
CREATEFOLDER()	{
	Folder=$1
	if [ ! -d $Folder ]
	then
		mkdir $Folder
	fi
}
####################################################

# JSON="./"
# JSON_QPU=$JSON"qpu_noisy_deterministic.json"
# SHOTS=0
# 
# FOLDER="./deterministic/"
# CREATEFOLDER $FOLDER
# 
# for MODEL in "bayes" "fuzzy" "cf"
# do
#     NAME="deterministic_"$MODEL
#     for ID in 0 1 2 3 4 5 6
#     do
#         execute="python launch_basket.py
#             -model $MODEL
#             -shots $SHOTS
#             -json_qpu $JSON_QPU
#             -folder $FOLDER
#             -name $NAME
#             -id $ID
#             --print
#             --save
#             --exe 
#         "
# 
#         echo $execute
#         $execute
#     done
# done

JSON="./"
JSON_QPU=$JSON"qpu_noisy_stochastic.json"
SHOTS=0

#FOLDER="./stochastic/"

for MODEL in "bayes" "fuzzy" "cf"
do
    FOLDER="./stochastic_"$MODEL"/"
    CREATEFOLDER $FOLDER
    NAME="stochastic_"$MODEL
    for ID in {0..18}
    do
        execute="python launch_basket.py
            -model $MODEL
            -shots $SHOTS
            -json_qpu $JSON_QPU
            -folder $FOLDER
            -name $NAME
            -id $ID
            --print
            --save
            --exe 
        "

        echo $execute
        $execute
    done
done

