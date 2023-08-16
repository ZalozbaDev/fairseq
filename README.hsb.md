# Hornjoserbski priklad

## Prihotowanje

- instalacija, hlej [README.md](README.md)

- model wobstarać:

```bash
cd examples/mms/
wget https://dl.fbaipublicfiles.com/mms/asr/mms1b_all.pt
```

## Wuber datajow za spoznawanje a merjenje

- korpus wot "Mozilla common voice" wobstarać:

https://commonvoice.mozilla.org/hsb/datasets 

cyly korpus wuzwolić (nic delta korpus) a scahnyc

tar xvfz cv-corpus-14.0-2023-06-23-hsb.tar.gz

cd cv-corpus-14.0-2023-06-23/hsb/

### zmenic mp3 na wav dataje

```bash
for i in $(ls -1 *.mp3); do ffmpeg -i $i -ar 16000 -vn -ac 1 $(echo $i | sed -e s/\.mp3/\.wav/) ; done
```

# transkripty wutworic

```bash
for i in $(ls -1 *.mp3); do cat ../validated.tsv | grep $i > ./test.txt; IFS=$'\t' read -a myArray < ./test.txt; echo "${myArray[2]}" > $(echo $i | sed -e s/\.mp3/\.trl/ ) ; done
```

## Dataju wuzwolic a spoznawanje / merjenje wuwjesc

Priklad kiz wulici WER (word error rate):

```bash
python examples/mms/asr/infer/mms_infer.py --model examples/mms/mms1b_all.pt --lang hsb --audio ../Downloads/cv-corpus-14.0-2023-06-23/hsb/clips/_voice_hsb_20367572.wav  --format letter
```

Priklad kiz wulici CER (character error rate):

```bash
python examples/mms/asr/infer/mms_infer.py --model examples/mms/mms1b_all.pt --lang hsb --audio ../Downloads/cv-corpus-14.0-2023-06-23/hsb/clips/_voice_hsb_20367572.wav  --format non
```

### Wuwjedzenje prikladow bjez grafikowej karty


