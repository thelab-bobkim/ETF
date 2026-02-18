# ETF 포트폴리오 텔레그램 알림 봇

## 📊 개요

퇴직연금 ETF 포트폴리오를 3시간마다 자동으로 모니터링하고 텔레그램으로 알림을 전송하는 봇입니다.

## 🚀 설치 방법 (AWS Lightsail)

```bash
# 1. 저장소 클론
git clone https://github.com/thelab-bobkim/ETF.git
cd ETF

# 2. 필수 패키지 설치
pip3 install requests

# 3. 봇 토큰 및 채팅 ID 수정
nano etf_bot.py
# TOKEN과 CHAT_ID를 본인 것으로 수정

# 4. 백그라운드 실행
nohup python3 etf_bot.py > etf_bot.log 2>&1 &

# 5. 상태 확인
tail -f etf_bot.log
```

## 📱 텔레그램 설정

1. @BotFather에서 봇 생성 → 토큰 받기
2. @userinfobot에서 채팅 ID 확인
3. `etf_bot.py` 파일에서 TOKEN, CHAT_ID 수정

## 💼 포트폴리오

현재 모니터링 중인 자산:
- **KODEX AI반도체** (304100.KS)
- **신한스노우볼인컴증권**

## 📊 기능

- ✅ 3시간마다 자동 리포트 전송
- ✅ 실시간 평가액 및 수익률 계산
- ✅ 이모지 및 한글 포맷으로 가독성 향상
- ✅ 24시간 무정지 운영

## 🔧 관리 명령어

```bash
# 봇 상태 확인
ps aux | grep etf_bot

# 로그 확인
tail -30 etf_bot.log

# 봇 재시작
pkill -f etf_bot
nohup python3 etf_bot.py > etf_bot.log 2>&1 &
```

## 📝 업데이트 히스토리

- 2026-02-18: 초기 버전 생성
