import subprocess
from pathlib import Path

current_dir = Path()  # 当前目录，或 Path('path/to/directory')

# 获取所有文件
files: list[str] = [f.name for f in current_dir.iterdir()]
files: list[str] = list(
    filter(
        lambda name: (not name.startswith(".")) and (not name.startswith("_")), files
    )
)

for file in files:
    result = subprocess.run(
        [
            "powershell",
            "-Command",
            "scp",
            "-r",
            f"./{file}",
            f"root@112.125.89.224:/opt/app/shakespeare-x-dir/shakespeare-x-server/{file}",
        ],
        capture_output=True,
        text=True,
        shell=True,
    )
    print(f"{file} upload success")

result = subprocess.run(
    [
        "ssh",
        "root@112.125.89.224",
        "cd /opt/app/shakespeare-x-dir/shakespeare-x-server && chmod +x build.sh && sh build.sh",
    ],
    capture_output=True,
    text=True,
    shell=True,
)
print(result.stderr)
