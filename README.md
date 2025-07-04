# yt-dlp-batch-gen
input.txt의 URL 목록을 기반으로 yt-dlp 다운로드 스크립트(ytd.sh)를 생성하는 개인용 도구입니다.

# 환경설정
## F-Droid 설치 (https://f-droid.org/)
* termux 검색 및 설치
* 브라우저와 F-Droid에서 '출처를 알 수 없는 앱 설치 권한' 제거

## termux 설정
```
pkg update
pkg install -U nano git python curl wget ffmpeg yt-dlp
termux-setup-storage
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
.\ytd.sh
```


# 옵션
## --order-num
다운받는 파일명 앞에 input.txt의 순서를 가지는 두 자리 숫자를 추가합니다.
> python gen.py --order-num
```
기존)
[체널명] 영상명.mp4

옵션 사용)
00. [체널명] 영상명.mp4
```

## --mp3
소리만 mp3포멧으로 다운로드
> python gen.py --mp3
