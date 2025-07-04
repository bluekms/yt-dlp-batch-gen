#!/usr/bin/env python3
import os
import sys

input_file = "input.txt"
output_file = "ytd.sh"

# 옵션 처리
use_order_num = "--order-num" in sys.argv
use_mp3 = "--mp3" in sys.argv

# 기존 ytd.sh 파일 삭제
if os.path.exists(output_file):
    os.remove(output_file)

# input.txt 읽고 ytd.sh 작성
with open(input_file, "r") as infile, open(output_file, "w") as outfile:
    outfile.write("#!/bin/bash\n\n")
    for index, line in enumerate(infile, start=1):
        url = line.strip()
        if url:
            number_prefix = f"{index:02}. " if use_order_num else ""
            output_template = f'storage/downloads/{number_prefix}[%(uploader)s] %(title)s.%(ext)s'

            mp3_option = "-x --audio-format mp3 " if use_mp3 else ""
            outfile.write(
                f'yt-dlp {mp3_option}-o "{output_template}" --no-overwrites "{url}"\n'
            )

# 실행 권한 부여
os.chmod(output_file, 0o755)

print(f"{output_file} 파일이 생성되었고 실행 권한이 부여되었습니다.")
