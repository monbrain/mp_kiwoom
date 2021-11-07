
# -*- coding=utf-8 -*-
"""
주요 기능: 
    - Process XingAPI Query

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
from pythoncom import PumpWaitingMessages
from win32com.client import DispatchWithEvents

##@@ User Package/Module
##------------------------------------------------------------
from _session import Session

##@@@ Constant/Varible
##============================================================
##@@ 전역 상수/변수

RES_PATH = "C:/eBest/xingAPI/Res/{res_code}.res"

blocks = {
    "t0167": {  ### 서버시간조회
        "inblock": {
            "InBlock": {
                "id": " "  # {id} 
            }
        },
        "outblock": {
            "OutBlock": {
                # "dt": "dt`char",  # {일자(YYYYMMDD)} 
                "time": "time`char"  # {시간(HHMMSSssssss)} 
            }
        }
    },
    "CSPAQ12200": {  ### 현물계좌예수금 주문가능금액 총평가 조회
        "inblock": {
            "InBlock1": {
                "RecCnt": "00001",  # {레코드갯수} 
                "MgmtBrnNo": "0",  # {관리지점번호} 
                "AcntNo": "55501071053",  # {계좌번호} 
                "Pwd": "0000",  # {비밀번호} 
                "BalCreTp": "0"  # {잔고생성구분}  HTS 는 0 0:주식잔고 1:기타  2:재투자잔고 3:유통대주 4:자기융자 5:유통대주 6:자기대주
            }
        },
        "outblock": {
            # "OutBlock1": {
            #     "RecCnt": "RecCnt`long",  # {레코드갯수} 
            #     "MgmtBrnNo": "MgmtBrnNo`char",  # {관리지점번호} 
            #     "AcntNo": "AcntNo`char",  # {계좌번호} 
            #     "Pwd": "Pwd`char",  # {비밀번호} 
            #     "BalCreTp": "BalCreTp`char"  # {잔고생성구분} 
            # },
            "OutBlock2": {
                # "RecCnt": "RecCnt`long",  # {레코드갯수} 
                # "BrnNm": "BrnNm`char",  # {지점명} 
                # "AcntNm": "AcntNm`char",  # {계좌명} 
                "MnyOrdAbleAmt": "amount`long",  # {현금주문가능금액} 
                # "MnyoutAbleAmt": "MnyoutAbleAmt`long",  # {출금가능금액} 
                # "SeOrdAbleAmt": "SeOrdAbleAmt`long",  # {거래소금액} 
                # "KdqOrdAbleAmt": "KdqOrdAbleAmt`long",  # {코스닥금액} 
                # "BalEvalAmt": "BalEvalAmt`long",  # {잔고평가금액} 
                # "RcvblAmt": "RcvblAmt`long",  # {미수금액} 
                # "DpsastTotamt": "DpsastTotamt`long",  # {예탁자산총액} 
                # "PnlRat": "PnlRat`double",  # {손익율} 
                # "InvstOrgAmt": "InvstOrgAmt`long",  # {투자원금} 
                # "InvstPlAmt": "InvstPlAmt`long",  # {투자손익금액} 
                # "CrdtPldgOrdAmt": "CrdtPldgOrdAmt`long",  # {신용담보주문금액} 
                "Dps": "deposit`long",  # {예수금} 계좌 입금액
                # "SubstAmt": "SubstAmt`long",  # {대용금액} 
                # "D1Dps": "D1Dps`long",  # {D1예수금} 
                # "D2Dps": "D2Dps`long",  # {D2예수금} 
                # "MnyrclAmt": "MnyrclAmt`long",  # {현금미수금액} 
                # "MgnMny": "MgnMny`long",  # {증거금현금} 
                # "MgnSubst": "MgnSubst`long",  # {증거금대용} 
                # "ChckAmt": "ChckAmt`long",  # {수표금액} 
                # "SubstOrdAbleAmt": "SubstOrdAbleAmt`long",  # {대용주문가능금액} 
                # "MgnRat100pctOrdAbleAmt": "MgnRat100pctOrdAbleAmt`long",  # {증거금률100퍼센트주문가능금액} 
                # "MgnRat35ordAbleAmt": "MgnRat35ordAbleAmt`long",  # {증거금률35%주문가능금액} 
                # "MgnRat50ordAbleAmt": "MgnRat50ordAbleAmt`long",  # {증거금률50%주문가능금액} 
                # "PrdaySellAdjstAmt": "PrdaySellAdjstAmt`long",  # {전일매도정산금액} 
                # "PrdayBuyAdjstAmt": "PrdayBuyAdjstAmt`long",  # {전일매수정산금액} 
                # "CrdaySellAdjstAmt": "CrdaySellAdjstAmt`long",  # {금일매도정산금액} 
                # "CrdayBuyAdjstAmt": "CrdayBuyAdjstAmt`long",  # {금일매수정산금액} 
                # "D1ovdRepayRqrdAmt": "D1ovdRepayRqrdAmt`long",  # {D1연체변제소요금액} 
                # "D2ovdRepayRqrdAmt": "D2ovdRepayRqrdAmt`long",  # {D2연체변제소요금액} 
                # "D1PrsmptWthdwAbleAmt": "D1PrsmptWthdwAbleAmt`long",  # {D1추정인출가능금액} 
                # "D2PrsmptWthdwAbleAmt": "D2PrsmptWthdwAbleAmt`long",  # {D2추정인출가능금액} 
                # "DpspdgLoanAmt": "DpspdgLoanAmt`long",  # {예탁담보대출금액} 
                # "Imreq": "Imreq`long",  # {신용설정보증금} 
                # "MloanAmt": "MloanAmt`long",  # {융자금액} 
                # "ChgAfPldgRat": "ChgAfPldgRat`double",  # {변경후담보비율} 
                # "OrgPldgAmt": "OrgPldgAmt`long",  # {원담보금액} 
                # "SubPldgAmt": "SubPldgAmt`long",  # {부담보금액} 
                # "RqrdPldgAmt": "RqrdPldgAmt`long",  # {소요담보금액} 
                # "OrgPdlckAmt": "OrgPdlckAmt`long",  # {원담보부족금액} 
                # "PdlckAmt": "PdlckAmt`long",  # {담보부족금액} 
                # "AddPldgMny": "AddPldgMny`long",  # {추가담보현금} 
                # "D1OrdAbleAmt": "D1OrdAbleAmt`long",  # {D1주문가능금액} 
                # "CrdtIntdltAmt": "CrdtIntdltAmt`long",  # {신용이자미납금액} 
                # "EtclndAmt": "EtclndAmt`long",  # {기타대여금액} 
                # "NtdayPrsmptCvrgAmt": "NtdayPrsmptCvrgAmt`long",  # {익일추정반대매매금액} 
                # "OrgPldgSumAmt": "OrgPldgSumAmt`long",  # {원담보합계금액} 
                # "CrdtOrdAbleAmt": "CrdtOrdAbleAmt`long",  # {신용주문가능금액} 
                # "SubPldgSumAmt": "SubPldgSumAmt`long",  # {부담보합계금액} 
                # "CrdtPldgAmtMny": "CrdtPldgAmtMny`long",  # {신용담보금현금} 
                # "CrdtPldgSubstAmt": "CrdtPldgSubstAmt`long",  # {신용담보대용금액} 
                # "AddCrdtPldgMny": "AddCrdtPldgMny`long",  # {추가신용담보현금} 
                # "CrdtPldgRuseAmt": "CrdtPldgRuseAmt`long",  # {신용담보재사용금액} 
                # "AddCrdtPldgSubst": "AddCrdtPldgSubst`long",  # {추가신용담보대용} 
                # "CslLoanAmtdt1": "CslLoanAmtdt1`long",  # {매도대금담보대출금액} 
                # "DpslRestrcAmt": "DpslRestrcAmt`long"  # {처분제한금액} 
            }
        }
    },
}

##@@@ Private Class/function
##============================================================

# ##@@ Handler
# ##------------------------------------------------------------
class _QueryHandler:

    def OnReceiveData(self, res_code):
        """ 요청 데이터 도착 Listener
        """
        # self.response = {}
 
        for block in self.outblock.keys():
            row_res = []
            for i in range(self.GetBlockCount(f"{res_code}{block}")):
                data = []
                for name in self.outblock[block].keys():
                    data.append(self.GetFieldData(res_code + block, name, i))
                    row_res.append(data)
            self.response[block] = row_res
        
        print(f"response: {self.response}")
        self.waiting = False


    def OnReceiveMessage(self, systemError, messageCode, message):
        """ 메시지(에러) 도착 Listener
        """
        print("OnReceiveMessage : ", systemError, messageCode, message)


##@@@ Public Class/function
##============================================================

def query(res_code, acntNo, **kwargs):
    """Query 요청

    Args:
        res_code (str, optional): [description]. Defaults to "t1857".
        acntNo (str, optional): [description]. Defaults to "".
        acnts (dict): 계정/계좌 정보
        inblock (dict, optional): [description]. Defaults to {}.
        outblock (dict, optional): [description]. Defaults to {}.
        callback ([type], optional): [description]. Defaults to None.

    Returns:
        [type]: [description]
    """
    defaults = {
        # 'res_code': None,
        # 'acntNo': None,
        'acnts': None,
        'inblock': {},
        'outblock': {},
        'callback': print,
    }
    params = {}
    
    for k, v in defaults.items():
        params[k] = kwargs[k] if k in kwargs else v

    account = Session(acntNo=acntNo, acnts=params['acnts']).account # NOTE: 로그인(실거래REAL)
    qHandler = DispatchWithEvents("XA_DataSet.XAQuery", _QueryHandler)  # NOTE: 핸들러 바인딩

    qHandler.LoadFromResFile(RES_PATH.format(res_code=res_code))
    qHandler.outblock = params['outblock']
    qHandler.response = {'account': account}
    qHandler.callback = params['callback']

    _key = list(params['inblock'].keys())[0]
    for k, v in params['inblock'][_key].items():  # NOTE: 입력 데이터 설정
        qHandler.SetFieldData(f"{res_code}{_key}", k, 0, v)
    
    try:
        qHandler.Request(False)  # False: 연속 조회(X)
    except:
        print("exception")
        sys.exit()

    qHandler.waiting = True

    while qHandler.waiting:
        # print("success!!")
        PumpWaitingMessages()
        time.sleep(1)  ## TODO: tr_code, real에 따라 조정 필요

    return qHandler.response


if __name__ == "__main__":
    # res_code = "CSPAQ12200"
    res_code = "t0167"
    acntNo = "55501071053"
    ACCOUNTS = {
        "20350571501": {
            "mode": "REAL",
            "id": "monwater",
            "pw": "Mo5221on",
            "cert": "Moon5221!!",
            "acnt_pw": "525221",
            "market": "KOSPI",
            "agency": "ebest"
        },
        "55501071053": {
            "mode": "DEMO",
            "id": "monwater",
            "pw": "moon1",
            "cert": "Moon5221!!",
            "acnt_pw": "0000",
            "market": "KOSPI",
            "agency": "ebest"
        },
        "A2030571501": {
            "mode": "ACE",
            "id": "monwater",
            "pw": "Mo5221on",
            "cert": "Moon5221!!",
            "acnt_pw": "525221",
            "market": "KOSPI",
            "agency": "ebest"
        }
    }
    kwargs = dict(
        acnts = ACCOUNTS,
        inblock = blocks[res_code]['inblock'],
        # inblock = blocks[res_code]['inblock'],
        outblock = blocks[res_code]['outblock'],
    )
    query(res_code, acntNo, **kwargs)
