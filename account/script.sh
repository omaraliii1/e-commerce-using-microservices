#!/bin/bash

FILES=$(find . -maxdepth 1 -type f -name "*.yaml" -o -name "*.yml")

for file in $FILES; do
    echo "Applying $file ..."
    kubectl apply -f $file
done

echo "Done!"