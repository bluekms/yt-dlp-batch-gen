#!/usr/bin/env python3
import os
import sys
import subprocess

input_file = "input.txt"
output_file = "ytd.sh"

# 옵션 처리
quality = None
if "-q" in sys.argv:
    try:
        idx = sys.argv.index("-q")
        quality = int(sys.argv[idx + 1])
        if quality not in (0, 720, 1080):
            raise ValueError
    except (IndexError, ValueError):
        print("에러: -q 옵션 뒤에는 0, 720 또는 1080 중 하나를 입력해야 합니다.")
        sys.exit(1)

# --order N 처리
order_start = None
if "--order" in sys.argv:
    try:
        idx = sys.argv.index("--order")
        order_start = int(sys.argv[idx + 1])
    except (IndexError, ValueError):
        print("에러: --order 옵션 뒤에는 정수를 입력해야 합니다.")
        sys.exit(1)

# 기존 ytd.sh 파일 삭제
if os.path.exists(output_file):
    os.remove(output_file)

# input.txt 읽고 ytd.sh 작성
with open(input_file, "r") as infile, open(output_file, "w") as outfile:
    outfile.write("#!/bin/bash\n\n")
    for index, line in enumerate(infile, start=order_start or 1):
        url = line.strip()
        if url:
            number_prefix = f"{index:03}. " if order_start is not None else ""
            output_template = f'storage/downloads/{number_prefix}[%(uploader)s] %(title)s.%(ext)s'

            if quality == 0:
                extra_options = "-x --audio-format mp3 "
            elif quality in (720, 1080):
                extra_options = f'-f "bestvideo[height<={quality}]+bestaudio" '
            else:
                extra_options = ""

            outfile.write(
                f'yt-dlp {extra_options}-o "{output_template}" --no-overwrites "{url}"\n'
            )

# 실행 권한 부여
os.chmod(output_file, 0o755)

print(f"{output_file} 파일이 생성되었고 실행 권한이 부여되었습니다.")

# 스크립트 생성 후 바로 실행
try:
    if output_file.endswith(".sh"):
        subprocess.run(["bash", output_file], check=True)
    else:  # ytd.bat
        subprocess.run([output_file], shell=True, check=True)
except subprocess.CalledProcessError as e:
    print(f"실행 중 오류 발생: {e}")
