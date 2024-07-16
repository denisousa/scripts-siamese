# Hyperparameter Optimization - Siamese

## DADOS ORIGINAIS
- Os dados originais que o Chaiyong me mandou em relação ao
Qualitas Corpus e dump do Stack Overflow estão abaixo:

link:
email: denismzsousa@gmail.com
folder: Chaiyong Datasource


## Introduction
Welcome to the *Hyperparameter Optimization - Siamese* project! This project consists of an infrastructure designed to search for the best hyperparameters that exist in the [Siamese](https://github.com/UCL-CREST/Siamese) tool. Below is the list of hyperparameters that we seek to find the best values for:

- Minimum Clone Size (lines)
    - minCloneSize
- Size of ngram
    - ngramSize
    - t2NgramSize
    - t1NgramSize
- Query Reduction
    - QRPercentileNorm
    - QRPercentileT2
    - QRPercentileT1
- Boosting
    - normBoost
    - t2Boost
    - t1Boost
    - origBoost
- Similarity
    - simThreshold

## About Siamese
[Siamese](https://github.com/UCL-CREST/Siamese) is a powerful tool utilized in the field of clone detection. It provides sophisticated functionalities for identifying code clones within a codebase. The project aims to enhance the efficiency of code maintenance in large software systems by detecting and managing code duplications.

## Siamese Optimization

Algoritmos de Busca falar

## How to execute?
### Downloading Databases

The developer must download the following databases:

- **cut_stackoverflow_filtered.zip**: Codebase with stack overflow snippets.
- **qualitas_corpus_clean.zip**: Codebase with snippets of projects that exist in Qualitas Corpus
- **elasticsearch**: Elastic Search instance at version 2.2.0.
- COLOCAR O ORÁCULO AQUI TAMBÉM

---
**_Note:_**: The cut_stackoverflow_filtered.zip code snippets contain only the files and code snippets that exist in the ground truth, in addition, the name of the files has also been adapted to signal the cut points.

To download these databases you must execute:

```
python download_datasource.py
```

### Configure values

### Configure Infrastructure Execution Parameters

### Project Indexing

### Execution of the Optimization Algorithm

Happy optimizing! 🚀

## Using Java 8

Utilizar o Java 8:
#sudo update-alternatives --config java
#sudo update-alternatives --config javac

sudo visudo
username ALL=(ALL) NOPASSWD: ALL

chmod +x java-install.sh

sudo apt-get install maven
sudo apt-get install openjdk-8-jdk
sudo apt purge openjdk-11-*
java -version
javac -version

need install
sudo apt-get install trash-cli

## Env Example
PROJECTS_PATH=./my_projects
ELASTICSEARCH_CLUSTERS=my_clusters
INDEX_NAME=qualitas_corpus
PROJECT_TO_INDEX=${PROJECTS_PATH}/mini_qualitas_corpus_clean
PROJECT_TO_SEARCH=${PROJECTS_PATH}/cut_stackoverflow_filtered
INITIAL_CLUSTER_QUANTITY=4
FINAL_CLUSTER_QUANTITY=8