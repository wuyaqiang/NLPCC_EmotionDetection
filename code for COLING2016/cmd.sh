#!/usr/bin/env bash
./svm_learn train.txt train.model > dump
./svm_classify test.txt train.model result.output > dump 
