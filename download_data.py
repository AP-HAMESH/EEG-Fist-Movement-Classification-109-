from pathlib import Path
import urllib.request

BASE_URL = "https://physionet.org/files/eegmmidb/1.0.0"
DATA_DIR = Path.cwd() / "data109" / "files"
PARTICIPANTS = range(1, 110)
RUNS = (3, 7, 11)

def download_physionet_109():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    downloaded = 0
    for sub in PARTICIPANTS:
        sub_str = f"S{sub:03d}"
        sub_dir = DATA_DIR / sub_str
        sub_dir.mkdir(parents=True, exist_ok=True)
        for run in RUNS:
            fname = f"{sub_str}R{run:02d}.edf"
            dest = sub_dir / fname
            if not dest.exists():
                url = f"{BASE_URL}/{sub_str}/{fname}"
                print(f"Downloading {fname}...")
                urllib.request.urlretrieve(url, dest)
            downloaded += 1
    print(f"Verified {downloaded}/327 EDF recordings in {DATA_DIR}")

if __name__ == "__main__":
    download_physionet_109()