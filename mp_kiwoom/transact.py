# -*- coding=utf-8 -*-
"""
주요 기능: 
    - 주식 매매/취소/정정

사용례: 
    - 
"""

##@@@ Package/Module
##============================================================

##@@ Built-In Package/Module
##------------------------------------------------------------
import os, sys
import time
from datetime import datetime

##@@ External Package/Module
##------------------------------------------------------------


##@@ User Package/Module
##------------------------------------------------------------
from _session import Session
from _queryBasic import query

##@@@ Constant/Varible
##============================================================
##@@ 전역 상수/변수
TODAY = datetime.now().strftime('%Y%m%d')  # NOTE: 오늘 날짜
ORDERS_COLLECTION = f'orders_ebest_{TODAY}'
REQ_LIMIT = 5  # NOTE: 주문 체결 확인 request 반복 횟수 제한
READY = 300  # START 상태 시간 READY(초) 전에 앱 실행

EXCHANGE_TIMES = {
    '장전 시간외': {'bgn': 83000, 'end': 84000},
    '장시작 동시호가': {'bgn': 83000, 'end': 90000},
    '정규시간': {'bgn': 90000, 'end': 153000},
    '장마감 동시호가': {'bgn': 152000, 'end': 153000},
    '장후 시간외': {'bgn': 154000, 'end': 160000},
    '시간외 단일가': {'bgn': 160000, 'end': 180000},
}

side_codes = {
    "sell": 1,
    "buy": 2,
    "ask": 2,
    "bid": 1,
    "매도": 1,
    "매수": 2
}

ba_type_codes = {
    "지정가": "00",
    "시장가": "03",
    "조건부지정가": "05",
    "최유리지정가": "06",
    "최우선지정가": "07",
    "장개시전시간외종가": "61",
    "시간외종가": "81",
    "시간외단일가": "82",
}


##@@ ebest request blocks
##------------------------------------------------------------

blocks = {
    "CSPAT00600": {  ### 현물주문
        "inblock": {
            "InBlock1": {
               "AcntNo": "55501067600",  # {계좌번호} 20350571501
               "InptPwd": "0000",  # {입력비밀번호} 525221
               "IsuNo": "005930",  # {종목번호} shcode
               "OrdQty": 0,  # {주문수량} volume
               "OrdPrc": 0.0,  # {주문가} price
               "BnsTpCode": "1",  # {매매구분} side_map[side] 1:매도 2:매수
               "OrdprcPtnCode": "00",  # {호가유형코드} ba_type_map[ba_type] 00@지정가 03@시장가 05@조건부지정가 06@최유리지정가 07@최우선지정가 61@장개시전시간외종가 81@시간외종가 82@시간외단일가
               "MgntrnCode": "000",  # {신용거래코드} 신용거래코드 000:보통 003:유통/자기융자신규 005:유통대주신규 007:자기대주신규 101:유통융자상환 103:자기융자상환 105:유통대주상환 107:자기대주상환 180:예탁담보대출상환(신용) 
               "LoanDt": " ",  # {대출일} 
               "OrdCndiTpCode": "0"  # {주문조건구분} 주문조건구분 0:없음,1:IOC,2:FOK
            }
        },
        "outblock": {
            "OutBlock1": {
               "RecCnt": "count1`long",  # {레코드갯수} 
               "AcntNo": "acnt_no`char",  # {계좌번호} 
            #    "InptPwd": "InptPwd`char",  # {입력비밀번호} 
            #    "IsuNo": "shcode`char",  # {종목번호} 
               "OrdQty": "_volume`long",  # {주문수량} 
               "OrdPrc": "_price`double",  # {주문가} 
               "BnsTpCode": "side`char",  # {매매구분} 
            #    "OrdprcPtnCode": "ba_type`char",  # {호가유형코드} 
            #    "PrgmOrdprcPtnCode": "PrgmOrdprcPtnCode`char",  # {프로그램호가유형코드} 
            #    "StslAbleYn": "StslAbleYn`char",  # {공매도가능여부} 
            #    "StslOrdprcTpCode": "StslOrdprcTpCode`char",  # {공매도호가구분} 
            #    "CommdaCode": "CommdaCode`char",  # {통신매체코드} 
            #    "MgntrnCode": "MgntrnCode`char",  # {신용거래코드} 
            #    "LoanDt": "LoanDt`char",  # {대출일} 
            #    "MbrNo": "MbrNo`char",  # {회원번호} 
            #    "OrdCndiTpCode": "OrdCndiTpCode`char",  # {주문조건구분} !확인 필요
            #    "StrtgCode": "StrtgCode`char",  # {전략코드} 
            #    "GrpId": "GrpId`char",  # {그룹ID} 
            #    "OrdSeqNo": "OrdSeqNo`long",  # {주문회차} 
            #    "PtflNo": "PtflNo`long",  # {포트폴리오번호} 
            #    "BskNo": "BskNo`long",  # {바스켓번호} 
            #    "TrchNo": "TrchNo`long",  # {트렌치번호} 
            #    "ItemNo": "ItemNo`long",  # {아이템번호} 
            #    "OpDrtnNo": "OpDrtnNo`char",  # {운용지시번호} 
            #    "LpYn": "LpYn`char",  # {유동성공급자여부} 
            #    "CvrgTpCode": "CvrgTpCode`char"  # {반대매매구분} 
            },
            # {'IsuNo': '001340', 'OrdQty': 15, 'OrdPrc': 6800.0, 'BnsTpCode': '2', 'OrdprcPtnCode': '00', 'OrdCndiTpCode': '0', 'order_no': 12, 'order_time': '160118454', 
            # 'market': '40', 'ba_type': '02', 'shcode': '001340', 'amount': 102000}
            "OutBlock2": {
               "RecCnt": "count2`long",  # {레코드갯수} 
               "OrdNo": "order_no`long",  # {주문번호} 
               "OrdTime": "order_time`char",  # {주문시각} 
               "OrdMktCode": "market`char",  # {주문시장코드}  # 10: 코스피?
               "OrdPtnCode": "ba_type`char",  # {주문유형코드} 
               "ShtnIsuNo": "shcode`char",  # {단축종목번호} 
            #    "MgempNo": "MgempNo`char",  # {관리사원번호} 
            #    "OrdAmt": "amount`long",  # {주문금액} 
            #    "SpareOrdNo": "SpareOrdNo`long",  # {예비주문번호} 
            #    "CvrgSeqno": "CvrgSeqno`long",  # {반대매매일련번호} 
            #    "RsvOrdNo": "RsvOrdNo`long",  # {예약주문번호} 
               "SpotOrdQty": "volume`long",  # {실물주문수량} 
            #    "RuseOrdQty": "RuseOrdQty`long",  # {재사용주문수량} 
               "MnyOrdAmt": "amount`long",  # {현금주문금액} 
            #    "SubstOrdAmt": "SubstOrdAmt`long",  # {대용주문금액} 
            #    "RuseOrdAmt": "RuseOrdAmt`long",  # {재사용주문금액} 
            #    "AcntNm": "AcntNm`char",  # {계좌명} 
            #    "IsuNm": "IsuNm`char"  # {종목명} 
            }
        }
    },
    "CSPAT00700": {  ### 현물정정주문
        "inblock": {
            "InBlock1": {
               "OrgOrdNo": 0,  # {원주문번호} 
               "AcntNo": "55501067600",  # {계좌번호} 
               "InptPwd": "0000",  # {입력비밀번호} 
               "IsuNo": " ",  # {종목번호} 
               "OrdQty": 0,  # {주문수량} 
               "OrdprcPtnCode": " ",  # {호가유형코드} 
               "OrdCndiTpCode": " ",  # {주문조건구분} 
               "OrdPrc": 0.0  # {주문가} 
            }
        },
        "outblock": {
            "OutBlock1": {
            #    "RecCnt": "RecCnt`long",  # {레코드갯수} 
               "OrgOrdNo": "OrgOrdNo`long",  # {원주문번호} 
               "AcntNo": "AcntNo`char",  # {계좌번호} 
            #    "InptPwd": "InptPwd`char",  # {입력비밀번호} 
               "IsuNo": "IsuNo`char",  # {종목번호} 
               "OrdQty": "OrdQty`long",  # {주문수량} 
               "OrdprcPtnCode": "OrdprcPtnCode`char",  # {호가유형코드} 
               "OrdCndiTpCode": "OrdCndiTpCode`char",  # {주문조건구분} 
               "OrdPrc": "OrdPrc`double",  # {주문가} 
            #    "CommdaCode": "CommdaCode`char",  # {통신매체코드} 
            #    "StrtgCode": "StrtgCode`char",  # {전략코드} 
            #    "GrpId": "GrpId`char",  # {그룹ID} 
            #    "OrdSeqNo": "OrdSeqNo`long",  # {주문회차} 
            #    "PtflNo": "PtflNo`long",  # {포트폴리오번호} 
            #    "BskNo": "BskNo`long",  # {바스켓번호} 
            #    "TrchNo": "TrchNo`long",  # {트렌치번호} 
            #    "ItemNo": "ItemNo`long"  # {아이템번호} 
            },
            "OutBlock2": {
            #    "RecCnt": "RecCnt`long",  # {레코드갯수} 
               "OrdNo": "order_no`long",  # {주문번호} 새로운 주문번호가 부여되는지 확인 필요
               "PrntOrdNo": "PrntOrdNo`long",  # {모주문번호} 원래 주문 번호인지 확인 필요
               "OrdTime": "order_time`char",  # {주문시각} 
               "OrdMktCode": "market`char",  # {주문시장코드} 
               "OrdPtnCode": "hoga_typ`char",  # {주문유형코드} 
               "ShtnIsuNo": "shcode`char",  # {단축종목번호} 
            #    "PrgmOrdprcPtnCode": "PrgmOrdprcPtnCode`char",  # {프로그램호가유형코드} 
            #    "StslOrdprcTpCode": "StslOrdprcTpCode`char",  # {공매도호가구분} 
            #    "StslAbleYn": "StslAbleYn`char",  # {공매도가능여부} 
            #    "MgntrnCode": "MgntrnCode`char",  # {신용거래코드} 
            #    "LoanDt": "LoanDt`char",  # {대출일} 
            #    "CvrgOrdTp": "CvrgOrdTp`char",  # {반대매매주문구분} 
            #    "LpYn": "LpYn`char",  # {유동성공급자여부} 
            #    "MgempNo": "MgempNo`char",  # {관리사원번호} 
               "OrdAmt": "OrdAmt`long",  # {주문금액} 
               "BnsTpCode": "BnsTpCode`char",  # {매매구분} 
            #    "SpareOrdNo": "SpareOrdNo`long",  # {예비주문번호} 
            #    "CvrgSeqno": "CvrgSeqno`long",  # {반대매매일련번호} 
               "RsvOrdNo": "RsvOrdNo`long",  # {예약주문번호} 
               "MnyOrdAmt": "MnyOrdAmt`long",  # {현금주문금액} 
            #    "SubstOrdAmt": "SubstOrdAmt`long",  # {대용주문금액} 
            #    "RuseOrdAmt": "RuseOrdAmt`long",  # {재사용주문금액} 
            #    "AcntNm": "AcntNm`char",  # {계좌명} 
            #    "IsuNm": "IsuNm`char"  # {종목명} 
            }
        }
    },
    "CSPAT00800": {  ### 현물취소주문
        "inblock": {
            "InBlock1": {
               "OrgOrdNo": 0,  # {원주문번호} 
               "AcntNo": "55501067600",  # {계좌번호} 
               "InptPwd": "0000",  # {입력비밀번호} 
               "IsuNo": " ",  # {종목번호} 
               "OrdQty": 0  # {주문수량} 
            }
        },
        "outblock": {
            "OutBlock1": {
            #    "RecCnt": "RecCnt`long",  # {레코드갯수} 
            #    "OrgOrdNo": "OrgOrdNo`long",  # {원주문번호} 
            #    "AcntNo": "AcntNo`char",  # {계좌번호} 
            #    "InptPwd": "InptPwd`char",  # {입력비밀번호} 
            #    "IsuNo": "IsuNo`char",  # {종목번호} 
            #    "OrdQty": "OrdQty`long",  # {주문수량} 
            #    "CommdaCode": "CommdaCode`char",  # {통신매체코드} 
            #    "GrpId": "GrpId`char",  # {그룹ID} 
            #    "StrtgCode": "StrtgCode`char",  # {전략코드} 
            #    "OrdSeqNo": "OrdSeqNo`long",  # {주문회차} 
            #    "PtflNo": "PtflNo`long",  # {포트폴리오번호} 
            #    "BskNo": "BskNo`long",  # {바스켓번호} 
            #    "TrchNo": "TrchNo`long",  # {트렌치번호} 
            #    "ItemNo": "ItemNo`long"  # {아이템번호} 
            },
            "OutBlock2": {
            #    "RecCnt": "RecCnt`long",  # {레코드갯수} 
               "OrdNo": "order_no`long",  # {주문번호} 
               "PrntOrdNo": "PrntOrdNo`long",  # {모주문번호} 
               "OrdTime": "order_time`char",  # {주문시각} 
               "OrdMktCode": "market`char",  # {주문시장코드} 
               "OrdPtnCode": "ba_type`char",  # {주문유형코드} 
               "ShtnIsuNo": "shcode`char",  # {단축종목번호} 
            #    "PrgmOrdprcPtnCode": "PrgmOrdprcPtnCode`char",  # {프로그램호가유형코드} 
            #    "StslOrdprcTpCode": "StslOrdprcTpCode`char",  # {공매도호가구분} 
            #    "StslAbleYn": "StslAbleYn`char",  # {공매도가능여부} 
            #    "MgntrnCode": "MgntrnCode`char",  # {신용거래코드} 
            #    "LoanDt": "LoanDt`char",  # {대출일} 
            #    "CvrgOrdTp": "CvrgOrdTp`char",  # {반대매매주문구분} 
            #    "LpYn": "LpYn`char",  # {유동성공급자여부} 
            #    "MgempNo": "MgempNo`char",  # {관리사원번호} 
            #    "BnsTpCode": "BnsTpCode`char",  # {매매구분} 
            #    "SpareOrdNo": "SpareOrdNo`long",  # {예비주문번호} 
            #    "CvrgSeqno": "CvrgSeqno`long",  # {반대매매일련번호} 
            #    "RsvOrdNo": "RsvOrdNo`long",  # {예약주문번호} 
            #    "AcntNm": "AcntNm`char",  # {계좌명} 
            #    "IsuNm": "IsuNm`char"  # {종목명} 
            }
        }
    }
}

##@@@ Private Class/function
##============================================================

# ##@@ 로그인
# ##------------------------------------------------------------

def _login(acntNo="", acnts={}):
    s = Session(acntNo=acntNo, acnts=acnts)
    return s.account


##@@@ Public Class/function
##============================================================

# def order(ticker, acntNo, price=0, volume=0, side="매수", type="지정가"):
def order(acntNo, **kwarg):
    """Order by Ebest
    Args:
        kwarg (dict):
            - ticker
            # - acntNo
            - price=0
            - volume=0
            - side="매수"
            - type="지정가"

    Returns:
        [type]: [description]
    """
    _login(acntNo=acntNo, acnts={})
    defaults = {
        'ticker': None,
        'acntNo': None,
        'price': 0,
        'volume': 0,
        'side': '매수',
        'type': '지정가'
    }
    params = {}
        # "mode": "REAL",
        # "id": "monwater",
        # "pw": "Mo5221on",
        # "cert": "Moon5221!!",
        # "acnt_pw": "525221",
        # "market": "KOSPI",
        # "agency": "ebest"
    for k, v in defaults.items():
        params[k] = kwarg[k] if k in kwarg else v

    input = {
        "AcntNo": params['acntNo'],  # 계좌번호 "20350571501"
        "InptPwd": params['acntNo'],  # 입력비밀번호 "525221"
        "IsuNo": shcode,  # 종목번호
        "OrdQty": volume,  # 주문수량
        "OrdPrc": price,  # 주문가
        "BnsTpCode": side_codes[side],  # 매매구분 1:매도 2:매수
        "OrdprcPtnCode": ba_type_codes[ba_type],  # 호가유형코드  00@지정가 03@시장가 05@조건부지정가 06@최유리지정가 07@최우선지정가 61@장개시전시간외종가 81@시간외종가 82@시간외단일가
        # "MgntrnCode": "000",  # 신용거래코드 000:보통 003:유통/자기융자신규 005:유통대주신규 007:자기대주신규 101:유통융자상환 103:자기융자상환 105:유통대주상환 107:자기대주상환 180:예탁담보대출상환(신용) 
        # "LoanDt": "", # 대출일
        # "OrdCndiTpCode": "0"  # 주문조건구분 0:없음,1:IOC,2:FOK
    }

    kwargs = {
        'res_code': 'CSPAT00600',
        'input': input,
        'out_type': 'dicts',
        'mode': mode,
        # 'out_key': 'multi',
        'out_keys': ['OutBlock1', 'OutBlock2']  # 전일: OutBlock, 당일: OutBlock1
        # 'out_keys': ['OutBlock2'] 
    }

    query("CSPAT00600", params['acntNo'], **kwargs)
    


def do_order(shcode="", price=0, volume=0, side="", ba_type="", mode='DEMO'):
    """ebest 주문

    Args:
        shcode (str, optional): [description]. Defaults to "".
        price (int, optional): [description]. Defaults to 0.
        volume (int, optional): [description]. Defaults to 0.
        side (str, optional): [description]. Defaults to "".
        ba_type (str, optional): [description]. Defaults to "".
        mode (str, optional): [description]. Defaults to 'DEMO'.

    Returns:
        [type]: [description]
    """

    acnt = _account(mode=mode)  # NOTE: 계좌번호, 비밀번호

    print(f"account: {acnt}")

    input = {
        "AcntNo": acnt['acnt_no'],  # 계좌번호 "20350571501"
        "InptPwd": acnt['acnt_pw'],  # 입력비밀번호 "525221"
        "IsuNo": shcode,  # 종목번호
        "OrdQty": volume,  # 주문수량
        "OrdPrc": price,  # 주문가
        "BnsTpCode": side_codes[side],  # 매매구분 1:매도 2:매수
        "OrdprcPtnCode": ba_type_codes[ba_type],  # 호가유형코드  00@지정가 03@시장가 05@조건부지정가 06@최유리지정가 07@최우선지정가 61@장개시전시간외종가 81@시간외종가 82@시간외단일가
        # "MgntrnCode": "000",  # 신용거래코드 000:보통 003:유통/자기융자신규 005:유통대주신규 007:자기대주신규 101:유통융자상환 103:자기융자상환 105:유통대주상환 107:자기대주상환 180:예탁담보대출상환(신용) 
        # "LoanDt": "", # 대출일
        # "OrdCndiTpCode": "0"  # 주문조건구분 0:없음,1:IOC,2:FOK
    }

    kwargs = {
        'res_code': 'CSPAT00600',
        'input': input,
        'out_type': 'dicts',
        'mode': mode,
        # 'out_key': 'multi',
        'out_keys': ['OutBlock1', 'OutBlock2']  # 전일: OutBlock, 당일: OutBlock1
        # 'out_keys': ['OutBlock2'] 
    }

    # data = request_api(**set_kwargs(blocks, **kwargs))
    return request_api(**set_kwargs(blocks, **kwargs))


def revise_order(order_no, shcode="", price=0, volume=0, ba_type="지정가", mode='DEMO'):
    """ebest 주문 정정

    Args:
        shcode (str, optional): [description]. Defaults to "".
        price (int, optional): [description]. Defaults to 0.
        volume (int, optional): [description]. Defaults to 0.
        side (str, optional): [description]. Defaults to "".
        ba_type (str, optional): [description]. Defaults to "".
        mode (str, optional): [description]. Defaults to 'DEMO'.

    Returns:
        [type]: [description]
    """

    acnt = _account(mode=mode)  # NOTE: 계좌번호, 비밀번호

    input = {
        "OrgOrdNo": order_no,  # 원주문번호
        "AcntNo": acnt['acnt_no'],  # 계좌번호 "20350571501"
        "InptPwd": acnt['acnt_pw'],  # 입력비밀번호 "525221"
        "IsuNo": shcode,  # 종목번호
        "OrdQty": volume,  # 주문수량
        "OrdPrc": price,  # 주문가
        "OrdprcPtnCode": ba_type_codes[ba_type],  # 호가유형코드  
        # "OrdCndiTpCode": "0"  # 주문조건구분 0:없음,1:IOC,2:FOK
    }

    kwargs = {
        'res_code': 'CSPAT00700',
        'input': input,
        'out_type': 'dicts',
        'mode': mode,
        # 'out_key': 'multi',
        'out_keys': ['OutBlock1', 'OutBlock2']  # 전일: OutBlock, 당일: OutBlock1
    }

    data = request_api(**set_kwargs(blocks, **kwargs))
    return data


def cancel_order(order_no, shcode="", volume=0, mode='DEMO'):
    """ebest 주문 취소

    Args:
        shcode (str, optional): [description]. Defaults to "".
        price (int, optional): [description]. Defaults to 0.
        volume (int, optional): [description]. Defaults to 0.
        side (str, optional): [description]. Defaults to "".
        ba_type (str, optional): [description]. Defaults to "".
        mode (str, optional): [description]. Defaults to 'DEMO'.

    Returns:
        [type]: [description]
    """

    acnt = _account(mode=mode)  # NOTE: 계좌번호, 비밀번호

    input = {
        "OrgOrdNo": order_no,  # 원주문번호
        "AcntNo": acnt['acnt_no'],  # 계좌번호 "20350571501"
        "InptPwd": acnt['acnt_pw'],  # 입력비밀번호 "525221"
        "IsuNo": shcode,  # 종목번호
        "OrdQty": volume,  # 주문수량
    }

    kwargs = {
        'res_code': 'CSPAT00800',
        'input': input,
        'out_type': 'dicts',
        'mode': mode,
        # 'out_key': 'multi',
        'out_keys': ['OutBlock1', 'OutBlock2']  # 전일: OutBlock, 당일: OutBlock1
    }

    data = request_api(**set_kwargs(blocks, **kwargs))
    return data



def cancel(**kwarg):
    """Order by Ebest
    Args:
        kwarg (dict):
            - ticker
            - acntNo
            - orderNo

    Returns:
        [type]: [description]
    """
    pass


def revise(**kwarg):
    """Order by Ebest
    Args:
        kwarg (dict):
            - ticker
            - acntNo
            - orderNo
            - volume=0
            - side="매수"
            - type="지정가"

    Returns:
        [type]: [description]
    """
    pass