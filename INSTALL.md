# ETF 텔레그램 봇 설치 가이드

## 📋 목차
1. [시스템 요구사항](#시스템-요구사항)
2. [텔레그램 봇 생성](#텔레그램-봇-생성)
3. [AWS LightSail 설정](#aws-lightsail-설정)
4. [봇 설치 및 실행](#봇-설치-및-실행)
5. [문제 해결](#문제-해결)

---

## 시스템 요구사항

### 최소 사양
- **OS**: Ubuntu 20.04 LTS 이상
- **RAM**: 512MB 이상
- **Python**: 3.6 이상
- **저장공간**: 1GB 이상

### 필요한 패키지
```bash
sudo apt update
sudo apt install -y python3 python3-pip git
pip3 install requests
```

---

## 텔레그램 봇 생성

### 1. BotFather와 대화
1. 텔레그램에서 `@BotFather` 검색
2. `/start` 명령어 입력
3. `/newbot` 명령어로 새 봇 생성

### 2. 봇 정보 입력
```
봇 이름: ETF Portfolio Bot
봇 유저네임: your_etf_bot (반드시 'bot'으로 끝나야 함)
```

### 3. 봇 토큰 저장
BotFather가 제공하는 토큰을 안전하게 보관:
```
예시: 1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
```

### 4. Chat ID 얻기

**방법 1: @userinfobot 사용**
1. `@userinfobot` 검색 후 시작
2. 아무 메시지 전송
3. `Id: 123456789` 형태로 표시됨

**방법 2: API 직접 호출**
1. 봇에게 메시지 전송
2. 브라우저에서 접속:
```
https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
```
3. JSON에서 `chat.id` 값 확인

---

## AWS LightSail 설정

### 1. 인스턴스 생성
1. AWS LightSail 콘솔 접속
2. **인스턴스 생성** 클릭
3. **플랫폼**: Linux/Unix
4. **청사진**: Ubuntu 20.04 LTS
5. **플랜**: $3.50/월 (512MB RAM)

### 2. 방화벽 설정
- SSH (22): ✅ 허용
- HTTP (80): ✅ 허용 (선택사항)
- HTTPS (443): ✅ 허용 (선택사항)

### 3. SSH 키 다운로드
- `.pem` 파일을 안전한 위치에 저장
- 권한 설정:
```bash
chmod 400 LightsailDefaultKey.pem
```

### 4. SSH 접속
```bash
ssh -i LightsailDefaultKey.pem ubuntu@<YOUR_SERVER_IP>
```

---

## 봇 설치 및 실행

### 1. 저장소 클론
```bash
cd /home/ubuntu
git clone https://github.com/thelab-bobkim/ETF.git
cd ETF
```

### 2. 봇 설정 수정
```bash
nano etf_bot.py
```

아래 부분을 수정:
```python
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'  # BotFather에서 받은 토큰
CHAT_ID = 'YOUR_CHAT_ID'           # 본인의 Chat ID
```

### 3. 포트폴리오 데이터 수정
```python
PORTFOLIO = {
    "KODEX AI반도체": {
        "investment": 220125300,      # 원금
        "current_value": 286448140,   # 평가액
        "profit": 66322840            # 수익금
    },
    "신한스노우볼인컴증권": {
        "investment": 114998945,
        "current_value": 133679962,
        "profit": 18681017
    }
}
```

### 4. 테스트 실행
```bash
# 10초 테스트
timeout 10 python3 etf_bot.py
```

텔레그램에서 메시지를 확인하세요!

### 5. 백그라운드 실행
```bash
nohup python3 etf_bot.py > etf_bot.log 2>&1 &
```

### 6. 실행 확인
```bash
# 프로세스 확인
ps aux | grep etf_bot | grep -v grep

# 로그 확인
tail -f etf_bot.log
```

---

## 문제 해결

### 봇이 메시지를 보내지 않는 경우

**1. 토큰 확인**
```bash
# 봇 토큰 테스트
curl https://api.telegram.org/bot<YOUR_TOKEN>/getMe
```

**2. Chat ID 확인**
```bash
# 최근 메시지 확인
curl https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates
```

**3. 로그 확인**
```bash
tail -50 etf_bot.log
```

### UTF-8 인코딩 오류

**해결방법**:
```bash
# 로케일 설정
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8

# 봇 재시작
sudo pkill -f etf_bot
nohup python3 etf_bot.py > etf_bot.log 2>&1 &
```

### 봇이 자동으로 중지되는 경우

**원인**: 서버 재부팅, 메모리 부족

**해결방법**: Systemd 서비스 등록
```bash
sudo nano /etc/systemd/system/etf-bot.service
```

내용:
```ini
[Unit]
Description=ETF Telegram Bot
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/ETF
ExecStart=/usr/bin/python3 /home/ubuntu/ETF/etf_bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

서비스 시작:
```bash
sudo systemctl daemon-reload
sudo systemctl enable etf-bot
sudo systemctl start etf-bot
sudo systemctl status etf-bot
```

### 최신 코드 업데이트

```bash
cd /home/ubuntu/ETF

# 기존 봇 중지
sudo pkill -f etf_bot
sleep 2

# 최신 코드 가져오기
git pull

# 봇 재시작
nohup python3 etf_bot.py > etf_bot.log 2>&1 &
```

---

## 유용한 명령어 모음

### 봇 관리
```bash
# 봇 상태 확인
ps aux | grep etf_bot

# 봇 중지
sudo pkill -f etf_bot

# 봇 시작
cd /home/ubuntu/ETF
nohup python3 etf_bot.py > etf_bot.log 2>&1 &

# 로그 실시간 보기
tail -f etf_bot.log

# 최근 로그 20줄
tail -20 etf_bot.log
```

### 서버 관리
```bash
# 디스크 사용량
df -h

# 메모리 사용량
free -h

# 프로세스 목록
top

# 시스템 재부팅
sudo reboot
```

---

## 보안 주의사항

⚠️ **중요**:
1. 봇 토큰을 절대 공개하지 마세요
2. GitHub에 토큰을 커밋하지 마세요
3. Chat ID도 비공개로 유지하세요
4. SSH 키를 안전하게 보관하세요
5. 정기적으로 서버 업데이트를 실행하세요

```bash
sudo apt update && sudo apt upgrade -y
```

---

## 추가 기능 (선택사항)

### 자동 업데이트 스크립트
```bash
nano /home/ubuntu/ETF/update.sh
```

내용:
```bash
#!/bin/bash
cd /home/ubuntu/ETF
sudo pkill -f etf_bot
sleep 2
git pull
nohup python3 etf_bot.py > etf_bot.log 2>&1 &
echo "✅ 봇이 업데이트되고 재시작되었습니다!"
```

실행 권한:
```bash
chmod +x /home/ubuntu/ETF/update.sh
```

사용:
```bash
./update.sh
```

---

**설치 완료!** 🎉

이제 3시간마다 자동으로 포트폴리오 알림을 받으실 수 있습니다.
