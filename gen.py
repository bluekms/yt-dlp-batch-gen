#!/usr/bin/env python3
import os
import sys
import subprocess

input_file = "input.txt"
output_file = "ytd.sh"

# 옵션 처리
quality = None  # None=자동, 0=오디오(mp3), 720/1080=해상도 제한
if "-q" in sys.argv:
    try:
        idx = sys.argv.index("-q")
        quality = int(sys.argv[idx + 1])
        if quality not in (0, 720, 1080):
            raise ValueError
    except (IndexError, ValueError):
        print("에러: -q 옵션 뒤에는 0, 720 또는 1080 중 하나를 입력해야 합니다.")
        sys.exit(1)

# --order N 처리(파일명 앞에 번호 붙이기 시작값)
order_start = None
if "--order" in sys.argv:
    try:
        idx = sys.argv.index("--order")
        order_start = int(sys.argv[idx + 1])
    except (IndexError, ValueError):
        print("에러: --order 옵션 뒤에는 정수를 입력해야 합니다.")
        sys.exit(1)

# Windows 배치 모드 여부
is_windows = "-w" in sys.argv

# 순수(pure) 모드 여부: 파일명/경로 관련 옵션만 남김
is_pure = "-p" in sys.argv

# 실행 파일 prefix와 출력 경로 처리
if is_windows:
    output_path = "."
    output_file = "ytd.bat"
    yt_dlp_cmd = ".\\yt-dlp"
    title_cmd = "[%%(uploader)s] %%(title)s.%%(ext)s"  # 배치 이스케이프
else:
    # Termux: 공유저장소 심볼릭 링크(먼저 termux-setup-storage 필요)
    output_path = "$HOME/storage/downloads"
    yt_dlp_cmd = "yt-dlp"
    title_cmd = "[%(uploader)s] %(title)s.%(ext)s"

# 기존 출력 스크립트 삭제
if os.path.exists(output_file):
    os.remove(output_file)

# 공통 옵션 구성
# - Termux: IPv4 강제(-4) + 안드로이드 클라이언트 우회(--extractor-args ...)
# - Windows: 기본값
common_opts = []
if not is_windows:
    common_opts += ['-4', '--extractor-args', 'youtube:player_client=android']
else:
    # 원하면 IPv4 강제하고 싶으면 주석 해제
    # common_opts += ['-4']
    pass

# 품질별 포맷 문자열 설정
# 기본: H.264 우선 조합(299/298/136/135/134) + m4a(140) / 18(360p) 폴백
def default_format():
    return '299+140/298+140/136+140/135+140/134+140/18'

def format_for_height(h):
    # height 제한 + H.264 우선, 안되면 18 폴백
    # ba는 최고 오디오로 m4a가 붙는 경우가 많지만, 안정성을 위해 140 우선 + ba 폴백
    return f'bv*[vcodec^=avc1][height<={h}]+140/bv*[vcodec^=avc1][height<={h}]+ba/18'

# input.txt 읽고 스크립트 작성
with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", encoding="utf-8") as outfile:
    if not is_windows:
        # bash 헤더(첫 실패로 중단되지 않도록 set -e 쓰지 않음)
        outfile.write("#!/data/data/com.termux/files/usr/bin/bash\n\n")
        outfile.write('OUT_DIR="' + output_path + '"\n\n')
    else:
        # 배치 헤더
        outfile.write("@echo off\n")
        outfile.write("setlocal enabledelayedexpansion\n")
        outfile.write(f"set OUT_DIR={output_path}\n\n")

    # 한 줄씩 URL 처리
    for index, raw in enumerate(infile, start=order_start or 1):
        url = raw.strip()
        if not url:
            continue

        number_prefix = f"{index:03}. " if order_start is not None else ""
        output_template = f'%s/{number_prefix}{title_cmd}'

        # 품질 옵션에 따른 extra_options/format
        extra_options = []
        fmt = None
        if not is_pure:
            if quality == 0:
                extra_options += ['-x', '--audio-format', 'mp3']
            elif quality in (720, 1080):
                fmt = format_for_height(quality)
            else:
                fmt = default_format()

        # 공통 커맨드 문자열 만들기
        if is_windows:
            cmd_parts = [yt_dlp_cmd]
            if not is_pure:
                cmd_parts += common_opts
                if extra_options:
                    cmd_parts += extra_options
                if fmt:
                    cmd_parts += ['-f', f'"{fmt}"']
                cmd_parts += ['-o', f'"%OUT_DIR%/{number_prefix}{title_cmd}"', '--no-overwrites', f'"{url}"']
            else:
                # pure: 파일명/경로 옵션만
                cmd_parts += ['-o', f'"%OUT_DIR%/{number_prefix}{title_cmd}"', f'"{url}"']
            outfile.write(" ".join(cmd_parts) + "\n")
        else:
            cmd_parts = [yt_dlp_cmd]
            if not is_pure:
                cmd_parts += common_opts
                if extra_options:
                    cmd_parts += extra_options
                if fmt:
                    cmd_parts += ['-f', f'"{fmt}"']
                cmd_parts += ['-o', f'"${{OUT_DIR}}/{number_prefix}{title_cmd}"', '--no-overwrites', f'"{url}"']
            else:
                # pure: 파일명/경로 옵션만
                cmd_parts += ['-o', f'"${{OUT_DIR}}/{number_prefix}{title_cmd}"', f'"{url}"']
            outfile.write(" ".join(cmd_parts) + " || true\n")

# 실행 권한 부여(bash)
if not is_windows:
    os.chmod(output_file, 0o755)

print(f"{output_file} 파일이 생성되었습니다.")

# 스크립트 생성 후 바로 실행(개별 실패 무시: check=False)
try:
    if output_file.endswith(".sh"):
        # OUT_DIR 경로 확인 안내(최초 1회 termux-setup-storage 필요)
        downloads_link = os.path.expanduser("~/storage/downloads")
        if not os.path.exists(downloads_link):
            print("참고: 처음 사용하는 경우 'termux-setup-storage'를 먼저 실행해야 합니다.")
        proc = subprocess.run(["bash", output_file], check=False)
        print(f"스크립트 실행 종료 (returncode={proc.returncode})")
    else:  # ytd.bat
        proc = subprocess.run([output_file], shell=True, check=False)
        print(f"스크립트 실행 종료 (returncode={proc.returncode})")
except Exception as e:
    print(f"실행 중 오류: {e}")
