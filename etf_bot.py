#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import time
from datetime import datetime

TOKEN = '8208099153:AAH_RKGn2AaWDYN3vzYPMxDlRYuWY0538gA'
CHAT_ID = '645537358'
INTERVAL = 10800  # 3시간

# 수정된 실제 데이터
PORTFOLIO = {
    "KODEX AI반도체": {
        "ticker": "304100.KS",
        "investment": 286448140,
        "current_value": 352770980,
        "profit": 66322840,
        "current_return": 23.15
    },
    "신한스노우볼인컴증권": {
        "ticker": "BOND",
        "investment": 48120738,
        "current_value": 67384547,
        "profit": 19263809,
        "current_return": 40.04
    }
}

def format_krw(amount):
    """원화 포맷팅 (예: 420,155,207 → 4억 2,015만원)"""
    if amount >= 100000000:
        uk = int(amount / 100000000)
        man = int((amount % 100000000) / 10000)
        won = int(amount % 10000)
        if man > 0 and won > 0:
            return f"{uk}억 {man:,}만 {won:,}원"
        elif man > 0:
            return f"{uk}억 {man:,}만원"
        else:
            return f"{uk}억원"
    elif amount >= 10000:
        man = int(amount / 10000)
        won = int(amount % 10000)
        if won > 0:
            return f"{man:,}만 {won:,}원"
        return f"{man:,}만원"
    else:
        return f"{int(amount):,}원"

def send_telegram(text):
    """텔레그램 메시지 전송"""
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": text,
            "parse_mode": "HTML"
        }
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            print(f"✅ 메시지 전송 성공: {datetime.now()}")
            return True
        else:
            print(f"❌ 전송 실패: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 오류: {e}")
        return False

def create_portfolio_report():
    """포트폴리오 리포트 생성 및 전송"""
    # 전체 합계 계산
    total_investment = sum(item["investment"] for item in PORTFOLIO.values())
    total_value = sum(item["current_value"] for item in PORTFOLIO.values())
    total_profit = total_value - total_investment
    total_return = (total_profit / total_investment * 100) if total_investment > 0 else 0
    
    # 개별 ETF
    kodex = PORTFOLIO["KODEX AI반도체"]
    shinhan = PORTFOLIO["신한스노우볼인컴증권"]
    
    # 현재 시간
    now = datetime.now().strftime("%Y년 %m월 %d일 %H:%M")
    
    # 메시지 생성
    message = f"""📊 <b>ETF 포트폴리오 리포트</b>
🕐 {now}

━━━━━━━━━━━━━━━━━━━━━━

💰 <b>총 투자금</b>
   {format_krw(total_investment)}

📈 <b>현재 평가액</b>
   {format_krw(total_value)}

💵 <b>총 수익금</b>
   <b>+{format_krw(total_profit)}</b>

📊 <b>전체 수익률</b>
   <b>+{total_return:.2f}%</b>

━━━━━━━━━━━━━━━━━━━━━━

📊 <b>KODEX AI반도체</b> (304100.KS)

💼 투자금: {format_krw(kodex["investment"])}
💰 평가액: {format_krw(kodex["current_value"])}
📈 수익률: <b>+{kodex["current_return"]:.2f}%</b>
💵 수익금: <b>+{format_krw(kodex["profit"])}</b>

━━━━━━━━━━━━━━━━━━━━━━

💼 <b>신한스노우볼인컴증권</b>

💼 투자금: {format_krw(shinhan["investment"])}
💰 평가액: {format_krw(shinhan["current_value"])}
📈 수익률: <b>+{shinhan["current_return"]:.2f}%</b>
💵 수익금: <b>+{format_krw(shinhan["profit"])}</b>

━━━━━━━━━━━━━━━━━━━━━━

⏰ <i>다음 리포트: 3시간 후</i>
"""
    
    return send_telegram(message)

def main():
    """메인 실행 함수"""
    print("=" * 60)
    print("💼 ETF 텔레그램 알림 봇 시작")
    print(f"⏰ 시작 시간: {datetime.now()}")
    print(f"📅 알림 주기: {INTERVAL}초 (3시간)")
    print("=" * 60)
    
    # 시작 메시지
    start_msg = f"""🚀 <b>ETF 알림 봇이 시작되었습니다!</b>

⏰ 시작 시간: {datetime.now().strftime("%Y년 %m월 %d일 %H:%M")}
📅 알림 주기: 3시간마다 자동 전송

━━━━━━━━━━━━━━━━━━━━━━

💼 <b>모니터링 중인 자산</b>
• KODEX AI반도체 (304100.KS)
• 신한스노우볼인컴증권

━━━━━━━━━━━━━━━━━━━━━━

📊 첫 번째 리포트를 전송합니다...
"""
    send_telegram(start_msg)
    
    # 첫 번째 리포트 전송
    print("\n📤 첫 번째 리포트 전송 중...")
    time.sleep(2)  # 2초 간격
    create_portfolio_report()
    
    # 주기적 전송 루프
    while True:
        try:
            next_report = datetime.now()
            print(f"\n⏰ {INTERVAL}초 대기 중... (다음 전송 예정: 약 {next_report.strftime('%H:%M')} + 3시간)")
            time.sleep(INTERVAL)
            
            print(f"\n📤 리포트 전송 중... ({datetime.now()})")
            create_portfolio_report()
            
        except KeyboardInterrupt:
            print("\n⚠️ 봇이 수동으로 종료되었습니다")
            stop_msg = "⚠️ <b>ETF 알림 봇이 종료되었습니다</b>"
            send_telegram(stop_msg)
            break
        except Exception as e:
            print(f"\n❌ 오류 발생: {e}")
            time.sleep(60)  # 오류 시 1분 대기 후 재시도

if __name__ == "__main__":
    main()
