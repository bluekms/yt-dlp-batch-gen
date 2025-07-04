#!/usr/bin/env python3
import os
import sys

input_file = "input.txt"
output_file = "ytd.sh"

# 옵션 처리
use_mp3 = "--mp3" in sys.argv

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

with open(input_file, "r") as infile, open(output_file, "w") as outfile:
    outfile.write("#!/bin/bash\n\n")
    for index, line in enumerate(infile, start=order_start or 1):
        url = line.strip()
        if url:
            number_prefix = f"{index:02}. " if order_start is not None else ""
            output_template = f'storage/downloads/{number_prefix}[%(uploader)s] %(title)s.%(ext)s'
            mp3_option = "-x --audio-format mp3 " if use_mp3 else ""
            outfile.write(
                f'yt-dlp {mp3_option}-o "{output_template}" --no-overwrites "{url}"\n'
            )

os.chmod(output_file, 0o755)

print(f"{output_file} 파일이 생성되었고 실행 권한이 부여되었습니다.")
