# -*- coding=utf-8 -*-
"""
주요 기능: 
    - ebest XINGAPI 접속
    - 계좌별 로그인(동일 계좌 접속 세션 존재시 재접속 안함)

사용례: 
    - 
"""

##@@@ 모듈 import
##============================================================

##@@ Built-In 모듈
##------------------------------------------------------------
import os, sys
import time
import json

##@@ Package 모듈
##------------------------------------------------------------
import yaml
import pythoncom
from win32com.client import DispatchWithEvents

##@@ User 모듈
##------------------------------------------------------------

##@@@ 전역 상수/변수
##============================================================
# ACNTS_PATH = "./settings/accounts.yml"
ACNTS_PATH = "./settings/accounts.json"

# ##@@@ Private Class/function
# ##============================================================

# ##@@ 계정/계좌 설정
# ##------------------------------------------------------------
def _load_acnts(path=ACNTS_PATH):
    """[계정/계좌 설정]

    Args:
        acntNo (str): 계좌 번호
        acnts (dict, optional): 계정/계좌 정보. Defaults to {}.

    Returns:
        [dict]: 계정/계좌 정보
    """
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
    # with open(path, "r", encoding="utf-8") as f:
    #     return yaml.load(f, Loader=yaml.FullLoader)


def _get_account(acntNo, acnts={}):
    """[계정/계좌 설정]

    Args:
        acntNo (str): 계좌 번호
        acnts (dict, optional): 계정/계좌 정보. Defaults to {}.

    Returns:
        [dict]: 계정/계좌 정보
    """
    return acnts[acntNo]


##@@@ Public Class/function
##============================================================

##@@ 세션 핸들러
##------------------------------------------------------------
class _SessionHandler:
    def OnLogin(self, code, msg):
        """서버 접속시 실행

        Args:
            code (str): 서버에서 받은 메시지 코드
            msg (str): 서버에서 받은 메시지 정보
        """
        self.waiting = False
    
        if code == '0000':
            print('[*] 로그인 성공')
        else:
            print(f'[*] 로그인 실패 : {msg}')
            exit()

    def OnDisconnect(self):
        """ 서버 접속 종료시 실행
        """
        self.waiting = False
        print('[*] 서버와의 연결이 끊어졌습니다')


##@@ 세션
##------------------------------------------------------------
class Session():
    _session = DispatchWithEvents('XA_Session.XASession', _SessionHandler)

    def __init__(self, acntNo="55501071053", acnts=ACNTS_PATH):
        """Session 클래스 생성시 실행

        Args:
            acntNo (str, optional): 계좌 번호. Defaults to "55501071053".
            acnts (str|dict, optional): str: 계좌/계정 정보 파일(.json) 경로. dict: 계좌/계정 정보
            TODO: private package에서 dict로 직접 설정 예정!!!
        """
        acnts = _load_acnts(path=acnts) if not acnts or type(acnts) == str else acnts

        # NOTE: 동일 계좌 연결이 있으면 pass
        if self._session.IsConnected() and self._session.acntNo == acntNo:
            # print(f"이미 '{acntNo}'로 로그인 중입니다.")
            pass
            # self._session.DisconnectServer()
        else:
            account = _get_account(acntNo, acnts)
            if self._session.IsConnected():
                print(f"연결 계좌를 '{self._session.acntNo}'에서 '{acntNo}'로 변경합니다.")

            # 로그인
            print(f"ebest로 로그인합니다.")
            url = {
                'r': 'hts.ebestsec.co.kr',
                'd': 'demo.ebestsec.co.kr',
                'a': '127.0.0.1'
            }.get(account['mode'].lower()[:1], 'demo.ebestsec.co.kr')
            port = 20001
            cert = '' if url == 'demo.ebestsec.co.kr' else account['cert']

            print(f"{acntNo}, {account}")
            
            # 로그인 요청
            self._session.acntNo = acntNo  # NOTE: 동일 계좌 여부 확인용
            self._session.waiting = True
            self._session.ConnectServer(url, port)
            self._session.Login(account['id'], account['pw'], cert, 0, 0)

            self.account = account  # TODO: 보안을 위해 삭제 예정!!, NOTE: 세션 정보 확인용

            while self._session.waiting:
                pythoncom.PumpWaitingMessages()
        

if __name__ == "__main__":
    acnts = _load_acnts()
    print(acnts)

    # with open(ACNTS_PATH, 'w', encoding='utf8') as f:
    #     json.dump(acnts, f, ensure_ascii=False, indent=4)