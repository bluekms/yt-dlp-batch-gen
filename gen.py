#!/usr/bin/env python3
import os

input_file = "input.txt"
output_file = "ytd.sh"

# 기존 ytd.sh 파일 삭제
if os.path.exists(output_file):
    os.remove(output_file)

# input.txt 읽고 ytd.sh 작성
with open(input_file, "r") as infile, open(output_file, "w") as outfile:
    outfile.write("#!/bin/bash\n\n")
    # 각 URL에 대해 yt-dlp 명령어 작성 (번호 붙이기)
    for index, line in enumerate(infile, start=1):
        url = line.strip()
        if url:
            number = f"{index:02}"  # 두 자리 번호 생성
            outfile.write(f'yt-dlp -o "storage/downloads/{number}. [%(uploader)s] %(title)s.%(ext)s" --no-overwrites "{url}"\n')

# 실행 권한 부여
os.chmod(output_file, 0o755)

print(f"{output_file} 파일이 생성되었고 실행 권한이 부여되었습니다.")
