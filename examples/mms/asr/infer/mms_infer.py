#!/usr/bin/env python -u
# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import argparse
import soundfile as sf
import tempfile
from pathlib import Path
import os
import subprocess
import sys
import re

def parser():
    parser = argparse.ArgumentParser(description="ASR inference script for MMS model")
    parser.add_argument("--model", type=str, help="path to ASR model", required=True)
    parser.add_argument("--audio", type=str, help="path to audio file", required=True, nargs='+')
    parser.add_argument("--lang", type=str, help="audio language", required=True)
    parser.add_argument("--format", type=str, choices=["none", "letter"], default="letter")
    return parser.parse_args()

def process(args):
    with tempfile.TemporaryDirectory() as tmpdir:
        print(">>> preparing tmp manifest dir ...", file=sys.stderr)
        tmpdir = Path(tmpdir)
        with open(tmpdir / "dev.tsv", "w") as fw ,open(tmpdir / "dev.ltr", "w") as fl, open(tmpdir / "dev.wrd", "w") as ft:
            fw.write("/\n")
            for audio in args.audio:
                trl=audio.replace('.wav','.trl')#.replace('/sig/','/trl/')
                if os.path.isfile(trl):
                    nsample = sf.SoundFile(audio).frames
                    fw.write(f"{audio}\t{nsample}\n")
                    with open(trl, 'r') as t:
                        data= t.read().replace('\n',' ').replace(' ', '|').lower()
                        fl.write(' '.join(list(data.replace(' ', '|')))+'\n')
                        ft.write(data.replace('|', ' ')+'\n')
                else:
                	print(">>> transcript file not found: " + trl, file=sys.stderr)
        with open(tmpdir / "dev.uid", "w") as fw:
            fw.write(f"{audio}\n"*len(args.audio))
        print('>>> check file in ' + str(tmpdir.absolute())  + " for prepared data", file=sys.stderr)
        cmd = f"""
        PYTHONPATH=. PREFIX=INFER HYDRA_FULL_ERROR=1 python examples/speech_recognition/new/infer.py -m --config-dir examples/mms/asr/config/ --config-name infer_common decoding.type=viterbi dataset.max_tokens=4000000 distributed_training.distributed_world_size=1 "common_eval.path='{args.model}'" task.data={tmpdir} dataset.gen_subset="{args.lang}:dev" common_eval.post_process={args.format} decoding.results_path={tmpdir} decoding.unique_wer_file=true
        """
        print(">>> loading model & running inference ...", file=sys.stderr)
        subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL,)
        with open(tmpdir/"hypo.word") as fr:
            for ii, hypo in enumerate(fr):
                hypo = re.sub("\(\S+\)$", "", hypo).strip()
                print(f'===============\nInput: {args.audio[ii]}\nOutput: {hypo}')


if __name__ == "__main__":
    args = parser()
    process(args)
