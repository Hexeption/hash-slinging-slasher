from pathlib import Path
for x in Path(__file__).with_name('bo3_sab_direct_to_bo4_asset_20260829.candidates.txt').read_text().splitlines():
    if x.strip(): print(x.strip())
