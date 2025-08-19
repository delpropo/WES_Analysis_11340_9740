#!/bin/bash

# Extract rows from gene_annotation.bed where the third column matches any string in GOI.txt

awk 'NR==FNR{goi[$1]; next} ($4 in goi)' GOI.txt gene_annotation.bed > extracted_GOI.bed