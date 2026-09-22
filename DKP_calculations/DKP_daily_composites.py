import re
import os

import pandas as pd

from pathlib import Path
from collections import defaultdict

# Dir paths
path_main  = Path(os.path.abspath('')).parents[2]
path_work  = Path(os.path.abspath(''))
path_files = path_work / 'files'

indir  = path_files / 'LS'
outdir = path_files
cols   = ['aspect','length','divs','vort','strain','lat','lon']

# Group files by day
pat = re.compile(r"_(\d{8})T\d{4}\.parquet$")
files_by_day = defaultdict(list)

cols = ['aspect','length','divs','vort','strain','lat','lon']
pat  = re.compile(r"_(\d{8})T\d{4}\.parquet$")

# Walk through leg1_n5 and leg2_n5 together
files_by_day = defaultdict(list)
for f in sorted(indir.glob('leg*_n5/dkp_fast-SWOT_*.parquet')):
    m = pat.search(f.name)
    if m:
        files_by_day[m.group(1)].append(f)

outdir = path_files / 'LS_daily_composites'
outdir.mkdir(exist_ok=True)

for day, flist in sorted(files_by_day.items()):
    # Concatenate all files for this day into a single dataframe
    df_day = pd.concat(
        (pd.read_parquet(f, columns=cols, engine="pyarrow") for f in flist),
        ignore_index=True,
    )
    df_day.to_parquet(outdir / f"dkp_fast-SWOT_{day}.parquet", engine="pyarrow")
    print(day, len(flist), "files ->", df_day.shape)