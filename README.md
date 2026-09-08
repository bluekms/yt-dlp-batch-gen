# yt-dlp-batch-gen
input.txt의 URL 목록을 기반으로 yt-dlp 다운로드 스크립트(output.sh)를 생성하는 개인용 도구입니다.

# 환경설정
## F-Droid 설치 (https://f-droid.org/)
* termux 검색 및 설치
* 브라우저와 F-Droid에서 '출처를 알 수 없는 앱 설치 권한' 제거

## termux 설정
아래 블록을 통째로 붙여넣으면 확인 질문 없이 끝까지 진행됩니다.  
마지막 `termux-setup-storage`만 안드로이드 권한 팝업에서 **허용**을 한 번 눌러야 합니다.
```
export DEBIAN_FRONTEND=noninteractive
apt-get update -y
apt-get -o Dpkg::Options::="--force-confold" full-upgrade -y
apt-get -o Dpkg::Options::="--force-confold" install -y nano git python curl wget ffmpeg deno yt-dlp
termux-setup-storage
```
* `pkg` 대신 `apt-get`을 쓰는 이유: `pkg`는 내부에서 curl을 호출하는데, 패키지가 일부만 갱신된 상태면 curl 자체가 깨져서(`CANNOT LINK EXECUTABLE "curl"`) `pkg`가 동작하지 않습니다. `apt-get`은 curl 없이 동작합니다.
* `full-upgrade`를 먼저 하는 이유: 라이브러리 버전이 서로 어긋나는 상태를 한 번에 정리하기 위해서입니다. `--force-confold`는 설정 파일 덮어쓰기 질문을 기존 유지로 자동 처리합니다.
* **ffmpeg는 필수**입니다. 없으면 1080p 등 영상·오디오가 분리된 포맷을 병합하지 못해 **소리 없는 mp4**와 `.m4a`가 따로 저장되고, `-q 0`(mp3)도 동작하지 않습니다.

설치 확인 (세 줄 모두 버전이 출력되어야 합니다):
```
curl --version | head -1
ffmpeg -version | head -1
yt-dlp --version
```

## yt-dlp-batch-gen 설치
```
wget -O gen.py https://raw.githubusercontent.com/bluekms/yt-dlp-batch-gen/main/gen.py
```

# 사용법
## input.txt파일 준비
```
rm -f input.txt; nano input.txt
```
이후 준비한 url들을 붙여넣고 ctrl+x, y를 눌러 nano 종료.

## gen.py 및 생성된 ytd.sh 실행
```
python gen.py
```
```
./ytd.sh
```


# 문제 해결
## `CANNOT LINK EXECUTABLE "curl": cannot locate symbol ...` 가 뜨고 `pkg`가 실패한다
패키지가 일부만 갱신되어 curl 라이브러리 버전이 어긋난 상태입니다. 위 termux 설정 블록을 다시 붙여넣으면 `apt-get full-upgrade`가 정리해 줍니다.

## `WARNING: ... ffmpeg is not installed. The formats won't be merged` 가 뜨고 영상에 소리가 없다
ffmpeg가 없어 영상(`*.f299.mp4`)과 오디오(`*.f140-1.m4a`)가 따로 저장된 것입니다. ffmpeg를 설치한 뒤 **같은 명령을 다시 실행**하면 이미 받은 조각을 재사용해 병합만 수행합니다.
```
apt-get -o Dpkg::Options::="--force-confold" install -y ffmpeg
python gen.py
```

## 더빙(`-l`)이나 1080p를 지정했는데 360p 영어로 받아진다
오래된 gen.py입니다. 아래로 다시 받으세요.
```
wget -O gen.py https://raw.githubusercontent.com/bluekms/yt-dlp-batch-gen/main/gen.py
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

## -q N
영상의 퀄리티를 선택합니다. <br/>
N값은 0, 720, 1080 3가지만 유효합니다.

```
python gen.py -q 0
./ytd.sh
```
기존의 --mp3 옵션과 같습니다. mp3 파일로 영상 없이 다운로드 합니다.

```
python gen.py -q 720
./ytd.sh
```
영상의 품질을 720 이하로 제한합니다.

```
python gen.py -q 1080
./ytd.sh
```
영상의 품질을 1080 이하로 제한합니다.


## -w
windows. sh파일 대신 ytd.bat로 출력합니다.


## -p
pure. 경로명, 파일명 옵션을 제외한 다른 옵션들을 무시합니다.


## -l LANG
자동번역(더빙) 오디오 트랙의 언어를 선택합니다(예: ko, ja, en).  
해당 언어 트랙이 없는 영상은 기본 오디오로 자동 대체되어 실패 없이 다운로드됩니다.  
`-q`, `-p` 옵션과 함께 사용할 수 있습니다.  
`-l` 지정 시 Termux 모드의 android 클라이언트 우회 옵션은 더빙 트랙을 노출하지 않아 자동으로 제외됩니다.

```
python gen.py -l ko
python gen.py -l ko -q 720
python gen.py -l ko -q 0
python gen.py -l ko -p
```