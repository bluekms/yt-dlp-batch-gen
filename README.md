# yt-dlp-batch-gen
input.txt의 URL 목록을 기반으로 yt-dlp 다운로드 스크립트(output.sh)를 생성하는 개인용 도구입니다.

# 환경설정
## F-Droid 설치 (https://f-droid.org/)
* termux 검색 및 설치
* 브라우저와 F-Droid에서 '출처를 알 수 없는 앱 설치 권한' 제거

## termux 설정
```
pkg update
pkg install -y -U nano git python curl wget ffmpeg deno yt-dlp
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
```
```
./ytd.sh
```


# 옵션
## --order N
다운받는 파일명 앞에 input.txt의 순서를 가지는 두 자리 숫자를 추가합니다.
```
python gen.py --order 1
```

> 기존)  
> [체널명] 영상명.mp4  
> 
> 옵션 사용)  
> 01. [체널명] 영상명.mp4  

## --q N
영상의 퀄리티를 선택합니다. <br/>
N값은 0, 720, 1080 3가지만 유효합니다.

```
python gen.py --q 0
./ytd.sh
```
기존의 --mp3 옵션과 같습니다. mp3 파일로 영상 없이 다운로드 합니다.

```
python gen.py --q 720
./ytd.sh
```
영상의 품질을 720 이하로 제한합니다.

```
python gen.py --q 720
./ytd.sh
```
영상의 품질을 1080 이하로 제한합니다.


## -w
sh파일 대신 ytd.bat로 출력합니다.