#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import time
from datetime import datetime

TOKEN = '8208099153:AAH_RKGn2AaWDYN3vzYPMxDlRYuWY0538gA'
CHAT_ID = '645537358'
INTERVAL = 10800  # 3시간

# 실제 데이터
PORTFOLIO = {
    "KODEX AI반도체": {
        "ticker": "304100.KS",
        "current_value": 286448140,
        "profit": 66322840,
        "investment": 220125300
    },
    "신한스노우볼인컴증권": {
        "ticker": "BOND",
        "current_value": 133679962,
        "profit": 18681017,
        "investment": 114998945
    }
}

def format_krw(amount):
    """원화 포맷팅"""
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
        payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            print(f"[OK] {datetime.now()}")
            return True
        else:
            print(f"[FAIL] {response.status_code}")
            return False
    except Exception as e:
        print(f"[ERROR] {e}")
        return False

def create_portfolio_report():
    """전문가 스타일 포트폴리오 리포트"""
    ti = sum(p["investment"] for p in PORTFOLIO.values())
    tp = sum(p["profit"] for p in PORTFOLIO.values())
    tv = sum(p["current_value"] for p in PORTFOLIO.values())
    tr = (tp/ti*100) if ti > 0 else 0
    
    k = PORTFOLIO["KODEX AI반도체"]
    kr = (k["profit"]/k["investment"]*100) if k["investment"] > 0 else 0
    
    s = PORTFOLIO["신한스노우볼인컴증권"]
    sr = (s["profit"]/s["investment"]*100) if s["investment"] > 0 else 0
    
    now = datetime.now().strftime('%Y년 %m월 %d일 %H:%M')
    
    # 수익률 상태 이모지
    profit_emoji = "🟢" if tr > 0 else "🔴" if tr < 0 else "⚪"
    k_emoji = "🟢" if kr > 0 else "🔴" if kr < 0 else "⚪"
    s_emoji = "🟢" if sr > 0 else "🔴" if sr < 0 else "⚪"
    
    msg = f"""╔═══════════════════════╗
   📊 <b>ETF 포트폴리오 리포트</b>
╚═══════════════════════╝

🕐 {now}

┏━━━━━━━━━━━━━━━━━━━━━━┓
┃  <b>💼 전체 포트폴리오 현황</b>  ┃
┗━━━━━━━━━━━━━━━━━━━━━━┛

💰 <b>총 투자금</b>
   {format_krw(ti)}

📈 <b>현재 평가액</b>
   {format_krw(tv)}

💵 <b>총 수익금</b>
   <b>+{format_krw(tp)}</b>

📊 <b>전체 수익률</b>  {profit_emoji}
   <b>+{tr:.2f}%</b>


┏━━━━━━━━━━━━━━━━━━━━━━┓
┃  <b>📈 개별 종목 현황</b>       ┃
┗━━━━━━━━━━━━━━━━━━━━━━┛

<b>📊 KODEX AI반도체</b> (304100.KS) {k_emoji}

├ 💼 투자금: {format_krw(k["investment"])}
├ 📈 평가액: {format_krw(k["current_value"])}
├ 📊 수익률: <b>+{kr:.2f}%</b>
└ 💵 수익금: <b>+{format_krw(k["profit"])}</b>

━━━━━━━━━━━━━━━━━━━━━━

<b>💼 신한스노우볼인컴증권</b> {s_emoji}

├ 💼 투자금: {format_krw(s["investment"])}
├ 📈 평가액: {format_krw(s["current_value"])}
├ 📊 수익률: <b>+{sr:.2f}%</b>
└ 💵 수익금: <b>+{format_krw(s["profit"])}</b>


┏━━━━━━━━━━━━━━━━━━━━━━┓
┃  <b>⏰ 알림 정보</b>            ┃
┗━━━━━━━━━━━━━━━━━━━━━━┛

📅 다음 리포트: <i>3시간 후</i>
🔔 알림 주기: <i>3시간 자동</i>

<i>※ 본 정보는 자동으로 생성되었습니다.</i>
"""
    return send_telegram(msg)

def main():
    """메인 실행"""
    print(f"ETF Bot Started - {datetime.now()}")
    
    now = datetime.now().strftime('%Y년 %m월 %d일 %H:%M')
    start_msg = f"""╔═══════════════════════╗
   🚀 <b>ETF 알림 봇 시작</b>
╚═══════════════════════╝

⏰ <b>시작 시간</b>
   {now}

📅 <b>알림 주기</b>
   3시간마다 자동 전송


┏━━━━━━━━━━━━━━━━━━━━━━┓
┃  <b>💼 모니터링 자산</b>        ┃
┗━━━━━━━━━━━━━━━━━━━━━━┛

✅ KODEX AI반도체 (304100.KS)
✅ 신한스노우볼인컴증권


┏━━━━━━━━━━━━━━━━━━━━━━┓
┃  <b>📊 포트폴리오 리포트</b>    ┃
┗━━━━━━━━━━━━━━━━━━━━━━┛

첫 번째 리포트를 전송합니다...

<i>※ 성공적인 투자를 응원합니다! 📈</i>"""
    
    send_telegram(start_msg)
    time.sleep(2)
    create_portfolio_report()
    
    while True:
        try:
            print(f"\nWaiting {INTERVAL}s...")
            time.sleep(INTERVAL)
            create_portfolio_report()
        except KeyboardInterrupt:
            print("\nBot stopped")
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(60)

if __name__ == "__main__":
    main()
