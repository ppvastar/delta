#!/bin/sh
GOOS=linux GOARCH=amd64 go build -o delta-service  main.go
if [ -d output ]
then
    rm -r output
fi
mkdir -p output/delta-service/log
cp -R  ../dpl output
cp delta-service output/delta-service
cp control.sh output/delta-service
cp run.sh output/delta-service


