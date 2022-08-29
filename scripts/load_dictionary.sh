#! /usr/bin/env bash

set -e


SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Download dictionaries

dictionaryFilesDir="dictionary_files"

cd $SCRIPT_DIR/..

# Setup venv
python3.9 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Fetch dictionaries

rm -rf dictionary_files

## Kanji
wget --directory-prefix=$dictionaryFilesDir http://www.edrdg.org/kanjidic/kanjidic2.xml.gz
gzip -d $dictionaryFilesDir/kanjidic2.xml.gz

## JMDict
wget --directory-prefix=$dictionaryFilesDir http://ftp.edrdg.org/pub/Nihongo/JMdict.gz
gzip -d $dictionaryFilesDir/JMDict.gz
mv $dictionaryFilesDir/JMdict $dictionaryFilesDir/JMdict.xml

# Load dictonaries

## Kanji
python -m tools.load_kanji $dictionaryFilesDir/kanjidic2.xml

## JMdict
python -m tools.load_jmdict $dictionaryFilesDir/JMdict.xml
