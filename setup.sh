#! /bin/bash
path=`pwd -P`
for i in data/components/*
do
  if [[ "$i" == *"Constants"* ]]; then
    continue
  elif [[ "$i" == *"Schneider"* ]]; then
    continue
  else
    sed -i '1d' $i
    sed -i '1i\includeFile = '$path'/data/components/ConstantsForNozzles.tps\' $i 
  fi
done
