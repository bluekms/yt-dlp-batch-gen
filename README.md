# yt-dlp-batch-gen
input.txt의 URL 목록을 기반으로 yt-dlp 다운로드 스크립트(output.sh)를 생성하는 개인용 도구입니다.

# 환경설정
## F-Droid 설치 (https://f-droid.org/)
```
pkg update
pkg install nano git python curl wget ffmpeg
```

## yt-dlp 설치
```
pip install -U yt-dlp
yt-dlp --version
```

## yt-dlp-batch-gen 설치
```
wget -O gen.py https://raw.githubusercontent.com/bluekms/yt-dlp-batch-gen/main/gen.py
```

# 사용법
## input.txt파일 준비
```
rm input.txt & nano input.txt
```
이후 준비한 url들을 붙여넣고 ctrl+x, y를 눌러 nano 종료.

## gen.py 및 생성된 ytd.sh 실행
```
python gen.py
ytd.sh
```