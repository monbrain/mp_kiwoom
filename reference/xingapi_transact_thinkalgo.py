## https://thinkalgo.tistory.com/60

#-*-coding: utf-8 -*-
 
import win32com.client
import pythoncom
import os, sys
import inspect
 
import pandas as pd
from pandas import DataFrame, Series, Panel
 
class XASessionEvents:
    상태 = False
 
    def OnLogin(self, code, msg):
        print("OnLogin : ", code, msg)
        XASessionEvents.상태 = True
 
    def OnLogout(self):
        pass
 
    def OnDisconnect(self):
        pass
 
class XAQueryEvents:
    상태 = False
 
    def OnReceiveData(self, szTrCode):
        print("OnReceiveData : %s" % szTrCode)
        XAQueryEvents.상태 = True
 
    def OnReceiveMessage(self, systemError, messageCode, message):
        print("OnReceiveMessage : ", systemError, messageCode, message)
 
 
def Login(url='demo.ebestsec.co.kr', port=200001, svrtype=0, id='userid', pwd='password', cert='공인인증 비밀번호'):
    session = win32com.client.DispatchWithEvents("XA_Session.XASession", XASessionEvents)
    session.SetMode("_XINGAPI7_","TRUE")
    result = session.ConnectServer(url, port)
 
    if not result:
        nErrCode = session.GetLastError()
        strErrMsg = session.GetErrorMessage(nErrCode)
        return (False, nErrCode, strErrMsg, None, session)
 
    session.Login(id, pwd, cert, svrtype, 0)
 
    while XASessionEvents.상태 == False:
        pythoncom.PumpWaitingMessages()
 
    계좌 = []
    계좌수 = session.GetAccountListCount()
 
    for i in range(계좌수):
        계좌.append(session.GetAccountList(i))
 
    return (True, 0, "OK", 계좌, session)
 
 
def CSPAT00600(계좌번호,입력비밀번호,종목번호,주문수량,주문가,매매구분,호가유형코드,신용거래코드,주문조건구분):
    pathname = os.path.dirname(sys.argv[0])
    resdir = os.path.abspath(pathname)
    
    query = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEvents)
 
    MYNAME = inspect.currentframe().f_code.co_name
    INBLOCK = "%sInBlock" % MYNAME
    INBLOCK1 = "%sInBlock1" % MYNAME
    OUTBLOCK = "%sOutBlock" % MYNAME
    OUTBLOCK1 = "%sOutBlock1" % MYNAME
    OUTBLOCK2 = "%sOutBlock2" % MYNAME
    RESFILE = "%s\\Res\\%s.res" % (resdir, MYNAME)
 
    print(MYNAME, RESFILE)
 
    query.LoadFromResFile(RESFILE)
    query.SetFieldData(INBLOCK1, "AcntNo", 0, 계좌번호)
    query.SetFieldData(INBLOCK1, "InptPwd", 0, 입력비밀번호)
    query.SetFieldData(INBLOCK1, "IsuNo", 0, 종목번호)
    query.SetFieldData(INBLOCK1, "OrdQty", 0, 주문수량)
    query.SetFieldData(INBLOCK1, "OrdPrc", 0, 주문가)
    query.SetFieldData(INBLOCK1, "BnsTpCode", 0, 매매구분)
    query.SetFieldData(INBLOCK1, "OrdprcPtnCode", 0, 호가유형코드)
    query.SetFieldData(INBLOCK1, "MgntrnCode", 0, 신용거래코드)
    query.SetFieldData(INBLOCK1, "LoanDt", 0, 대출일)
    query.SetFieldData(INBLOCK1, "OrdCndiTpCode", 0, 주문조건구분)
    query.Request(0)
 
    while XAQueryEvents.상태 == False:
        pythoncom.PumpWaitingMessages()
 
    result = []
    nCount = query.GetBlockCount(OUTBLOCK1)
    for i in range(nCount):
        레코드갯수 = int(query.GetFieldData(OUTBLOCK1, "RecCnt", i).strip())
        계좌번호 = query.GetFieldData(OUTBLOCK1, "AcntNo", i).strip()
        입력비밀번호 = query.GetFieldData(OUTBLOCK1, "InptPwd", i).strip()
        종목번호 = query.GetFieldData(OUTBLOCK1, "IsuNo", i).strip()
        주문수량 = int(query.GetFieldData(OUTBLOCK1, "OrdQty", i).strip())
        주문가 = query.GetFieldData(OUTBLOCK1, "OrdPrc", i).strip()
        매매구분 = query.GetFieldData(OUTBLOCK1, "BnsTpCode", i).strip()
        호가유형코드 = query.GetFieldData(OUTBLOCK1, "OrdprcPtnCode", i).strip()
        프로그램호가유형코드 = query.GetFieldData(OUTBLOCK1, "PrgmOrdprcPtnCode", i).strip()
        공매도가능여부 = query.GetFieldData(OUTBLOCK1, "StslAbleYn", i).strip()
        공매도호가구분 = query.GetFieldData(OUTBLOCK1, "StslOrdprcTpCode", i).strip()
        통신매체코드 = query.GetFieldData(OUTBLOCK1, "CommdaCode", i).strip()
        신용거래코드 = query.GetFieldData(OUTBLOCK1, "MgntrnCode", i).strip()
        대출일 = query.GetFieldData(OUTBLOCK1, "LoanDt", i).strip()
        회원번호 = query.GetFieldData(OUTBLOCK1, "MbrNo", i).strip()
        주문조건구분 = query.GetFieldData(OUTBLOCK1, "OrdCndiTpCode", i).strip()
        전략코드 = query.GetFieldData(OUTBLOCK1, "StrtgCode", i).strip()
        그룹ID = query.GetFieldData(OUTBLOCK1, "GrpId", i).strip()
        주문회차 = int(query.GetFieldData(OUTBLOCK1, "OrdSeqNo", i).strip())
        포트폴리오번호 = int(query.GetFieldData(OUTBLOCK1, "PtflNo", i).strip())
        바스켓번호 = int(query.GetFieldData(OUTBLOCK1, "BskNo", i).strip())
        트렌치번호 = int(query.GetFieldData(OUTBLOCK1, "TrchNo", i).strip())
        아이템번호 = int(query.GetFieldData(OUTBLOCK1, "ItemNo", i).strip())
        운용지시번호 = query.GetFieldData(OUTBLOCK1, "OpDrtnNo", i).strip()
        유동성공급자여부 = query.GetFieldData(OUTBLOCK1, "LpYn", i).strip()
        반대매매구분 = query.GetFieldData(OUTBLOCK1, "CvrgTpCode", i).strip()
 
        lst = [레코드갯수,계좌번호,입력비밀번호,종목번호,주문수량,주문가,매매구분,호가유형코드,프로그램호가유형코드,공매도가능여부,공매도호가구분,통신매체코드,신용거래코드,대출일,회원번호,주문조건구분,전략코드,그룹ID,주문회차,포트폴리오번호,바스켓번호,트렌치번호,아이템번호,운용지시번호,유동성공급자여부,반대매매구분]
        result.append(lst)
 
    columns=['레코드갯수','계좌번호','입력비밀번호','종목번호','주문수량','주문가','매매구분','호가유형코드','프로그램호가유형코드','공매도가능여부','공매도호가구분','통신매체코드','신용거래코드','대출일','회원번호','주문조건구분','전략코드','그룹ID','주문회차','포트폴리오번호','바스켓번호','트렌치번호','아이템번호','운용지시번호','유동성공급자여부','반대매매구분']
    df = DataFrame(data=result, columns=columns)
 
    result = []
    nCount = query.GetBlockCount(OUTBLOCK2)
    for i in range(nCount):
        레코드갯수 = int(query.GetFieldData(OUTBLOCK2, "RecCnt", i).strip())
        주문번호 = int(query.GetFieldData(OUTBLOCK2, "OrdNo", i).strip())
        주문시각 = query.GetFieldData(OUTBLOCK2, "OrdTime", i).strip()
        주문시장코드 = query.GetFieldData(OUTBLOCK2, "OrdMktCode", i).strip()
        주문유형코드 = query.GetFieldData(OUTBLOCK2, "OrdPtnCode", i).strip()
        단축종목번호 = query.GetFieldData(OUTBLOCK2, "ShtnIsuNo", i).strip()
        관리사원번호 = query.GetFieldData(OUTBLOCK2, "MgempNo", i).strip()
        주문금액 = int(query.GetFieldData(OUTBLOCK2, "OrdAmt", i).strip())
        예비주문번호 = int(query.GetFieldData(OUTBLOCK2, "SpareOrdNo", i).strip())
        반대매매일련번호 = int(query.GetFieldData(OUTBLOCK2, "CvrgSeqno", i).strip())
        예약주문번호 = int(query.GetFieldData(OUTBLOCK2, "RsvOrdNo", i).strip())
        실물주문수량 = int(query.GetFieldData(OUTBLOCK2, "SpotOrdQty", i).strip())
        재사용주문수량 = int(query.GetFieldData(OUTBLOCK2, "RuseOrdQty", i).strip())
        현금주문금액 = int(query.GetFieldData(OUTBLOCK2, "MnyOrdAmt", i).strip())
        대용주문금액 = int(query.GetFieldData(OUTBLOCK2, "SubstOrdAmt", i).strip())
        재사용주문금액 = int(query.GetFieldData(OUTBLOCK2, "RuseOrdAmt", i).strip())
        계좌명 = query.GetFieldData(OUTBLOCK2, "AcntNm", i).strip()
        종목명 = query.GetFieldData(OUTBLOCK2, "IsuNm", i).strip()
 
        lst = [레코드갯수,주문번호,주문시각,주문시장코드,주문유형코드,단축종목번호,관리사원번호,주문금액,예비주문번호,반대매매일련번호,예약주문번호,실물주문수량,재사용주문수량,현금주문금액,대용주문금액,재사용주문금액,계좌명,종목명]
        result.append(lst)
 
    columns=['레코드갯수','주문번호','주문시각','주문시장코드','주문유형코드','단축종목번호','관리사원번호','주문금액','예비주문번호','반대매매일련번호','예약주문번호','실물주문수량','재사용주문수량','현금주문금액','대용주문금액','재사용주문금액','계좌명','종목명']
    df1 = DataFrame(data=result, columns=columns)
 
    XAQueryEvents.상태 = False
 
    return (df, df1)
 
def CSPAT00700(원주문번호,계좌번호,입력비밀번호,종목번호,주문수량,호가유형코드,주문조건구분,주문가):
    pathname = os.path.dirname(sys.argv[0])
    resdir = os.path.abspath(pathname)
    
    query = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEvents)
 
    MYNAME = inspect.currentframe().f_code.co_name
    INBLOCK = "%sInBlock" % MYNAME
    INBLOCK1 = "%sInBlock1" % MYNAME
    OUTBLOCK = "%sOutBlock" % MYNAME
    OUTBLOCK1 = "%sOutBlock1" % MYNAME
    OUTBLOCK2 = "%sOutBlock2" % MYNAME
    RESFILE = "%s\\Res\\%s.res" % (resdir, MYNAME)
 
    print(MYNAME, RESFILE)
 
    query.LoadFromResFile(RESFILE)
    query.SetFieldData(INBLOCK1, "OrgOrdNo", 0, 원주문번호)
    query.SetFieldData(INBLOCK1, "AcntNo", 0, 계좌번호)
    query.SetFieldData(INBLOCK1, "InptPwd", 0, 입력비밀번호)
    query.SetFieldData(INBLOCK1, "IsuNo", 0, 종목번호)
    query.SetFieldData(INBLOCK1, "OrdQty", 0, 주문수량)
    query.SetFieldData(INBLOCK1, "OrdprcPtnCode", 0, 호가유형코드)
    query.SetFieldData(INBLOCK1, "OrdCndiTpCode", 0, 주문조건구분)
    query.SetFieldData(INBLOCK1, "OrdPrc", 0, 주문가)
    query.Request(0)
 
    while XAQueryEvents.상태 == False:
        pythoncom.PumpWaitingMessages()
 
    result = []
    nCount = query.GetBlockCount(OUTBLOCK1)
    for i in range(nCount):
        레코드갯수 = int(query.GetFieldData(OUTBLOCK1, "RecCnt", i).strip())
        원주문번호 = int(query.GetFieldData(OUTBLOCK1, "OrgOrdNo", i).strip())
        계좌번호 = query.GetFieldData(OUTBLOCK1, "AcntNo", i).strip()
        입력비밀번호 = query.GetFieldData(OUTBLOCK1, "InptPwd", i).strip()
        종목번호 = query.GetFieldData(OUTBLOCK1, "IsuNo", i).strip()
        주문수량 = int(query.GetFieldData(OUTBLOCK1, "OrdQty", i).strip())
        호가유형코드 = query.GetFieldData(OUTBLOCK1, "OrdprcPtnCode", i).strip()
        주문조건구분 = query.GetFieldData(OUTBLOCK1, "OrdCndiTpCode", i).strip()
        주문가 = query.GetFieldData(OUTBLOCK1, "OrdPrc", i).strip()
        통신매체코드 = query.GetFieldData(OUTBLOCK1, "CommdaCode", i).strip()
        전략코드 = query.GetFieldData(OUTBLOCK1, "StrtgCode", i).strip()
        그룹ID = query.GetFieldData(OUTBLOCK1, "GrpId", i).strip()
        주문회차 = int(query.GetFieldData(OUTBLOCK1, "OrdSeqNo", i).strip())
        포트폴리오번호 = int(query.GetFieldData(OUTBLOCK1, "PtflNo", i).strip())
        바스켓번호 = int(query.GetFieldData(OUTBLOCK1, "BskNo", i).strip())
        트렌치번호 = int(query.GetFieldData(OUTBLOCK1, "TrchNo", i).strip())
        아이템번호 = int(query.GetFieldData(OUTBLOCK1, "ItemNo", i).strip())
 
        lst = [레코드갯수,원주문번호,계좌번호,입력비밀번호,종목번호,주문수량,호가유형코드,주문조건구분,주문가,통신매체코드,전략코드,그룹ID,주문회차,포트폴리오번호,바스켓번호,트렌치번호,아이템번호]
        result.append(lst)
 
    columns=['레코드갯수','원주문번호','계좌번호','입력비밀번호','종목번호','주문수량','호가유형코드','주문조건구분','주문가','통신매체코드','전략코드','그룹ID','주문회차','포트폴리오번호','바스켓번호','트렌치번호','아이템번호']
    df = DataFrame(data=result, columns=columns)
 
    result = []
    nCount = query.GetBlockCount(OUTBLOCK2)
    for i in range(nCount):
        레코드갯수 = int(query.GetFieldData(OUTBLOCK2, "RecCnt", i).strip())
        주문번호 = int(query.GetFieldData(OUTBLOCK2, "OrdNo", i).strip())
        모주문번호 = int(query.GetFieldData(OUTBLOCK2, "PrntOrdNo", i).strip())
        주문시각 = query.GetFieldData(OUTBLOCK2, "OrdTime", i).strip()
        주문시장코드 = query.GetFieldData(OUTBLOCK2, "OrdMktCode", i).strip()
        주문유형코드 = query.GetFieldData(OUTBLOCK2, "OrdPtnCode", i).strip()
        단축종목번호 = query.GetFieldData(OUTBLOCK2, "ShtnIsuNo", i).strip()
        프로그램호가유형코드 = query.GetFieldData(OUTBLOCK2, "PrgmOrdprcPtnCode", i).strip()
        공매도호가구분 = query.GetFieldData(OUTBLOCK2, "StslOrdprcTpCode", i).strip()
        공매도가능여부 = query.GetFieldData(OUTBLOCK2, "StslAbleYn", i).strip()
        신용거래코드 = query.GetFieldData(OUTBLOCK2, "MgntrnCode", i).strip()
        대출일 = query.GetFieldData(OUTBLOCK2, "LoanDt", i).strip()
        반대매매주문구분 = query.GetFieldData(OUTBLOCK2, "CvrgOrdTp", i).strip()
        유동성공급자여부 = query.GetFieldData(OUTBLOCK2, "LpYn", i).strip()
        관리사원번호 = query.GetFieldData(OUTBLOCK2, "MgempNo", i).strip()
        주문금액 = int(query.GetFieldData(OUTBLOCK2, "OrdAmt", i).strip())
        매매구분 = query.GetFieldData(OUTBLOCK2, "BnsTpCode", i).strip()
        예비주문번호 = int(query.GetFieldData(OUTBLOCK2, "SpareOrdNo", i).strip())
        반대매매일련번호 = int(query.GetFieldData(OUTBLOCK2, "CvrgSeqno", i).strip())
        예약주문번호 = int(query.GetFieldData(OUTBLOCK2, "RsvOrdNo", i).strip())
        현금주문금액 = int(query.GetFieldData(OUTBLOCK2, "MnyOrdAmt", i).strip())
        대용주문금액 = int(query.GetFieldData(OUTBLOCK2, "SubstOrdAmt", i).strip())
        재사용주문금액 = int(query.GetFieldData(OUTBLOCK2, "RuseOrdAmt", i).strip())
        계좌명 = query.GetFieldData(OUTBLOCK2, "AcntNm", i).strip()
        종목명 = query.GetFieldData(OUTBLOCK2, "IsuNm", i).strip()
 
        lst = [레코드갯수,주문번호,모주문번호,주문시각,주문시장코드,주문유형코드,단축종목번호,프로그램호가유형코드,공매도호가구분,공매도가능여부,신용거래코드,대출일,반대매매주문구분,유동성공급자여부,관리사원번호,주문금액,매매구분,예비주문번호,반대매매일련번호,예약주문번호,현금주문금액,대용주문금액,재사용주문금액,계좌명,종목명]
        result.append(lst)
 
    columns=['레코드갯수','주문번호','모주문번호','주문시각','주문시장코드','주문유형코드','단축종목번호','프로그램호가유형코드','공매도호가구분','공매도가능여부','신용거래코드','대출일','반대매매주문구분','유동성공급자여부','관리사원번호','주문금액','매매구분','예비주문번호','반대매매일련번호','예약주문번호','현금주문금액','대용주문금액','재사용주문금액','계좌명','종목명']
    df1 = DataFrame(data=result, columns=columns)
 
    XAQueryEvents.상태 = False
 
    return (df, df1)
 
def CSPAT00800(원주문번호,계좌번호,입력비밀번호,종목번호,주문수량):
    pathname = os.path.dirname(sys.argv[0])
    resdir = os.path.abspath(pathname)
    
    query = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEvents)
 
    MYNAME = inspect.currentframe().f_code.co_name
    INBLOCK = "%sInBlock" % MYNAME
    INBLOCK1 = "%sInBlock1" % MYNAME
    OUTBLOCK = "%sOutBlock" % MYNAME
    OUTBLOCK1 = "%sOutBlock1" % MYNAME
    OUTBLOCK2 = "%sOutBlock2" % MYNAME
    RESFILE = "%s\\Res\\%s.res" % (resdir, MYNAME)
 
    print(MYNAME, RESFILE)
 
    query.LoadFromResFile(RESFILE)
    query.SetFieldData(INBLOCK1, "OrgOrdNo", 0, 원주문번호)
    query.SetFieldData(INBLOCK1, "AcntNo", 0, 계좌번호)
    query.SetFieldData(INBLOCK1, "InptPwd", 0, 입력비밀번호)
    query.SetFieldData(INBLOCK1, "IsuNo", 0, 종목번호)
    query.SetFieldData(INBLOCK1, "OrdQty", 0, 주문수량)
    query.Request(0)
 
    while XAQueryEvents.상태 == False:
        pythoncom.PumpWaitingMessages()
 
    result = []
    nCount = query.GetBlockCount(OUTBLOCK1)
    for i in range(nCount):
        레코드갯수 = int(query.GetFieldData(OUTBLOCK1, "RecCnt", i).strip())
        원주문번호 = int(query.GetFieldData(OUTBLOCK1, "OrgOrdNo", i).strip())
        계좌번호 = query.GetFieldData(OUTBLOCK1, "AcntNo", i).strip()
        입력비밀번호 = query.GetFieldData(OUTBLOCK1, "InptPwd", i).strip()
        종목번호 = query.GetFieldData(OUTBLOCK1, "IsuNo", i).strip()
        주문수량 = int(query.GetFieldData(OUTBLOCK1, "OrdQty", i).strip())
        통신매체코드 = query.GetFieldData(OUTBLOCK1, "CommdaCode", i).strip()
        그룹ID = query.GetFieldData(OUTBLOCK1, "GrpId", i).strip()
        전략코드 = query.GetFieldData(OUTBLOCK1, "StrtgCode", i).strip()
        주문회차 = int(query.GetFieldData(OUTBLOCK1, "OrdSeqNo", i).strip())
        포트폴리오번호 = int(query.GetFieldData(OUTBLOCK1, "PtflNo", i).strip())
        바스켓번호 = int(query.GetFieldData(OUTBLOCK1, "BskNo", i).strip())
        트렌치번호 = int(query.GetFieldData(OUTBLOCK1, "TrchNo", i).strip())
        아이템번호 = int(query.GetFieldData(OUTBLOCK1, "ItemNo", i).strip())
 
        lst = [레코드갯수,원주문번호,계좌번호,입력비밀번호,종목번호,주문수량,통신매체코드,그룹ID,전략코드,주문회차,포트폴리오번호,바스켓번호,트렌치번호,아이템번호]
        result.append(lst)
 
    columns=['레코드갯수','원주문번호','계좌번호','입력비밀번호','종목번호','주문수량','통신매체코드','그룹ID','전략코드','주문회차','포트폴리오번호','바스켓번호','트렌치번호','아이템번호']
    df = DataFrame(data=result, columns=columns)
 
    result = []
    nCount = query.GetBlockCount(OUTBLOCK2)
    for i in range(nCount):
        레코드갯수 = int(query.GetFieldData(OUTBLOCK2, "RecCnt", i).strip())
        주문번호 = int(query.GetFieldData(OUTBLOCK2, "OrdNo", i).strip())
        모주문번호 = int(query.GetFieldData(OUTBLOCK2, "PrntOrdNo", i).strip())
        주문시각 = query.GetFieldData(OUTBLOCK2, "OrdTime", i).strip()
        주문시장코드 = query.GetFieldData(OUTBLOCK2, "OrdMktCode", i).strip()
        주문유형코드 = query.GetFieldData(OUTBLOCK2, "OrdPtnCode", i).strip()
        단축종목번호 = query.GetFieldData(OUTBLOCK2, "ShtnIsuNo", i).strip()
        프로그램호가유형코드 = query.GetFieldData(OUTBLOCK2, "PrgmOrdprcPtnCode", i).strip()
        공매도호가구분 = query.GetFieldData(OUTBLOCK2, "StslOrdprcTpCode", i).strip()
        공매도가능여부 = query.GetFieldData(OUTBLOCK2, "StslAbleYn", i).strip()
        신용거래코드 = query.GetFieldData(OUTBLOCK2, "MgntrnCode", i).strip()
        대출일 = query.GetFieldData(OUTBLOCK2, "LoanDt", i).strip()
        반대매매주문구분 = query.GetFieldData(OUTBLOCK2, "CvrgOrdTp", i).strip()
        유동성공급자여부 = query.GetFieldData(OUTBLOCK2, "LpYn", i).strip()
        관리사원번호 = query.GetFieldData(OUTBLOCK2, "MgempNo", i).strip()
        매매구분 = query.GetFieldData(OUTBLOCK2, "BnsTpCode", i).strip()
        예비주문번호 = int(query.GetFieldData(OUTBLOCK2, "SpareOrdNo", i).strip())
        반대매매일련번호 = int(query.GetFieldData(OUTBLOCK2, "CvrgSeqno", i).strip())
        예약주문번호 = int(query.GetFieldData(OUTBLOCK2, "RsvOrdNo", i).strip())
        계좌명 = query.GetFieldData(OUTBLOCK2, "AcntNm", i).strip()
        종목명 = query.GetFieldData(OUTBLOCK2, "IsuNm", i).strip()
 
        lst = [레코드갯수,주문번호,모주문번호,주문시각,주문시장코드,주문유형코드,단축종목번호,프로그램호가유형코드,공매도호가구분,공매도가능여부,신용거래코드,대출일,반대매매주문구분,유동성공급자여부,관리사원번호,매매구분,예비주문번호,반대매매일련번호,예약주문번호,계좌명,종목명]
        result.append(lst)
 
    columns=['레코드갯수','주문번호','모주문번호','주문시각','주문시장코드','주문유형코드','단축종목번호','프로그램호가유형코드','공매도호가구분','공매도가능여부','신용거래코드','대출일','반대매매주문구분','유동성공급자여부','관리사원번호','매매구분','예비주문번호','반대매매일련번호','예약주문번호','계좌명','종목명']
    df1 = DataFrame(data=result, columns=columns)
 
    XAQueryEvents.상태 = False
 
    return (df, df1)
 
 
def CSPAQ12200(레코드갯수='',관리지점번호='',계좌번호='',비밀번호='',잔고생성구분='0'):
    '''
    현물계좌예수금 주문가능금액 총평가 조회
    '''
    pathname = os.path.dirname(sys.argv[0])
    resdir = os.path.abspath(pathname)
    
    query = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEvents)
 
    MYNAME = inspect.currentframe().f_code.co_name
    INBLOCK = "%sInBlock" % MYNAME
    INBLOCK1 = "%sInBlock1" % MYNAME
    OUTBLOCK = "%sOutBlock" % MYNAME
    OUTBLOCK1 = "%sOutBlock1" % MYNAME
    OUTBLOCK2 = "%sOutBlock2" % MYNAME
    RESFILE = "%s\\Res\\%s.res" % (resdir, MYNAME)
 
    print(MYNAME, RESFILE)
 
    query.LoadFromResFile(RESFILE)
    query.SetFieldData(INBLOCK1, "RecCnt", 0, 레코드갯수)
    query.SetFieldData(INBLOCK1, "MgmtBrnNo", 0, 관리지점번호)
    query.SetFieldData(INBLOCK1, "AcntNo", 0, 계좌번호)
    query.SetFieldData(INBLOCK1, "Pwd", 0, 비밀번호)
    query.SetFieldData(INBLOCK1, "BalCreTp", 0, 잔고생성구분)
    query.Request(0)
 
    while XAQueryEvents.상태 == False:
        pythoncom.PumpWaitingMessages()
 
    result = []
    nCount = query.GetBlockCount(OUTBLOCK1)
    for i in range(nCount):
        레코드갯수 = int(query.GetFieldData(OUTBLOCK1, "RecCnt", i).strip())
        관리지점번호 = query.GetFieldData(OUTBLOCK1, "MgmtBrnNo", i).strip()
        계좌번호 = query.GetFieldData(OUTBLOCK1, "AcntNo", i).strip()
        비밀번호 = query.GetFieldData(OUTBLOCK1, "Pwd", i).strip()
        잔고생성구분 = query.GetFieldData(OUTBLOCK1, "BalCreTp", i).strip()
 
        lst = [레코드갯수,관리지점번호,계좌번호,비밀번호,잔고생성구분]
        result.append(lst)
 
    df = DataFrame(data=result, columns=['레코드갯수','관리지점번호','계좌번호','비밀번호','잔고생성구분'])
 
    result = []
    nCount = query.GetBlockCount(OUTBLOCK2)
    for i in range(nCount):
        레코드갯수 = int(query.GetFieldData(OUTBLOCK2, "RecCnt", i).strip())
        지점명 = query.GetFieldData(OUTBLOCK2, "BrnNm", i).strip()
        계좌명 = query.GetFieldData(OUTBLOCK2, "AcntNm", i).strip()
        현금주문가능금액 = int(query.GetFieldData(OUTBLOCK2, "MnyOrdAbleAmt", i).strip())
        출금가능금액 = int(query.GetFieldData(OUTBLOCK2, "MnyoutAbleAmt", i).strip())
        거래소금액 = int(query.GetFieldData(OUTBLOCK2, "SeOrdAbleAmt", i).strip())
        코스닥금액 = int(query.GetFieldData(OUTBLOCK2, "KdqOrdAbleAmt", i).strip())
        잔고평가금액 = int(query.GetFieldData(OUTBLOCK2, "BalEvalAmt", i).strip())
        미수금액 = int(query.GetFieldData(OUTBLOCK2, "RcvblAmt", i).strip())
        예탁자산총액 = int(query.GetFieldData(OUTBLOCK2, "DpsastTotamt", i).strip())
        손익율 = float(query.GetFieldData(OUTBLOCK2, "PnlRat", i).strip())
        투자원금 = int(query.GetFieldData(OUTBLOCK2, "InvstOrgAmt", i).strip())
        투자손익금액 = int(query.GetFieldData(OUTBLOCK2, "InvstPlAmt", i).strip())
        신용담보주문금액 = int(query.GetFieldData(OUTBLOCK2, "CrdtPldgOrdAmt", i).strip())
        예수금 = int(query.GetFieldData(OUTBLOCK2, "Dps", i).strip())
        대용금액 = int(query.GetFieldData(OUTBLOCK2, "SubstAmt", i).strip())
        D1예수금 = int(query.GetFieldData(OUTBLOCK2, "D1Dps", i).strip())
        D2예수금 = int(query.GetFieldData(OUTBLOCK2, "D2Dps", i).strip())
        현금미수금액 = int(query.GetFieldData(OUTBLOCK2, "MnyrclAmt", i).strip())
        증거금현금 = int(query.GetFieldData(OUTBLOCK2, "MgnMny", i).strip())
        증거금대용 = int(query.GetFieldData(OUTBLOCK2, "MgnSubst", i).strip())
        수표금액 = int(query.GetFieldData(OUTBLOCK2, "ChckAmt", i).strip())
        대용주문가능금액 = int(query.GetFieldData(OUTBLOCK2, "SubstOrdAbleAmt", i).strip())
        증거금률100퍼센트주문가능금액 = int(query.GetFieldData(OUTBLOCK2, "MgnRat100pctOrdAbleAmt", i).strip())
        증거금률35주문가능금액 = int(query.GetFieldData(OUTBLOCK2, "MgnRat35ordAbleAmt", i).strip())
        증거금률50주문가능금액 = int(query.GetFieldData(OUTBLOCK2, "MgnRat50ordAbleAmt", i).strip())
        전일매도정산금액 = int(query.GetFieldData(OUTBLOCK2, "PrdaySellAdjstAmt", i).strip())
        전일매수정산금액 = int(query.GetFieldData(OUTBLOCK2, "PrdayBuyAdjstAmt", i).strip())
        금일매도정산금액 = int(query.GetFieldData(OUTBLOCK2, "CrdaySellAdjstAmt", i).strip())
        금일매수정산금액 = int(query.GetFieldData(OUTBLOCK2, "CrdayBuyAdjstAmt", i).strip())
        D1연체변제소요금액 = int(query.GetFieldData(OUTBLOCK2, "D1ovdRepayRqrdAmt", i).strip())
        D2연체변제소요금액 = int(query.GetFieldData(OUTBLOCK2, "D2ovdRepayRqrdAmt", i).strip())
        D1추정인출가능금액 = int(query.GetFieldData(OUTBLOCK2, "D1PrsmptWthdwAbleAmt", i).strip())
        D2추정인출가능금액 = int(query.GetFieldData(OUTBLOCK2, "D2PrsmptWthdwAbleAmt", i).strip())
        예탁담보대출금액 = int(query.GetFieldData(OUTBLOCK2, "DpspdgLoanAmt", i).strip())
        신용설정보증금 = int(query.GetFieldData(OUTBLOCK2, "Imreq", i).strip())
        융자금액 = int(query.GetFieldData(OUTBLOCK2, "MloanAmt", i).strip())
        변경후담보비율 = float(query.GetFieldData(OUTBLOCK2, "ChgAfPldgRat", i).strip())
        원담보금액 = int(query.GetFieldData(OUTBLOCK2, "OrgPldgAmt", i).strip())
        부담보금액 = int(query.GetFieldData(OUTBLOCK2, "SubPldgAmt", i).strip())
        소요담보금액 = int(query.GetFieldData(OUTBLOCK2, "RqrdPldgAmt", i).strip())
        원담보부족금액 = int(query.GetFieldData(OUTBLOCK2, "OrgPdlckAmt", i).strip())
        담보부족금액 = int(query.GetFieldData(OUTBLOCK2, "PdlckAmt", i).strip())
        추가담보현금 = int(query.GetFieldData(OUTBLOCK2, "AddPldgMny", i).strip())
        D1주문가능금액 = int(query.GetFieldData(OUTBLOCK2, "D1OrdAbleAmt", i).strip())
        신용이자미납금액 = int(query.GetFieldData(OUTBLOCK2, "CrdtIntdltAmt", i).strip())
        기타대여금액 = int(query.GetFieldData(OUTBLOCK2, "EtclndAmt", i).strip())
        익일추정반대매매금액 = int(query.GetFieldData(OUTBLOCK2, "NtdayPrsmptCvrgAmt", i).strip())
        원담보합계금액 = int(query.GetFieldData(OUTBLOCK2, "OrgPldgSumAmt", i).strip())
        신용주문가능금액 = int(query.GetFieldData(OUTBLOCK2, "CrdtOrdAbleAmt", i).strip())
        부담보합계금액 = int(query.GetFieldData(OUTBLOCK2, "SubPldgSumAmt", i).strip())
        신용담보금현금 = int(query.GetFieldData(OUTBLOCK2, "CrdtPldgAmtMny", i).strip())
        신용담보대용금액 = int(query.GetFieldData(OUTBLOCK2, "CrdtPldgSubstAmt", i).strip())
        추가신용담보현금 = int(query.GetFieldData(OUTBLOCK2, "AddCrdtPldgMny", i).strip())
        신용담보재사용금액 = int(query.GetFieldData(OUTBLOCK2, "CrdtPldgRuseAmt", i).strip())
        추가신용담보대용 = int(query.GetFieldData(OUTBLOCK2, "AddCrdtPldgSubst", i).strip())
        매도대금담보대출금액 = int(query.GetFieldData(OUTBLOCK2, "CslLoanAmtdt1", i).strip())
        처분제한금액 = int(query.GetFieldData(OUTBLOCK2, "DpslRestrcAmt", i).strip())
 
        lst = [레코드갯수,지점명,계좌명,현금주문가능금액,출금가능금액,거래소금액,코스닥금액,잔고평가금액,미수금액,
            예탁자산총액,손익율,투자원금,투자손익금액,신용담보주문금액,예수금,대용금액,D1예수금,D2예수금,
            현금미수금액,증거금현금,증거금대용,수표금액,대용주문가능금액,증거금률100퍼센트주문가능금액,
            증거금률35주문가능금액,증거금률50주문가능금액,전일매도정산금액,전일매수정산금액,금일매도정산금액,
            금일매수정산금액,D1연체변제소요금액,D2연체변제소요금액,D1추정인출가능금액,D2추정인출가능금액,
            예탁담보대출금액,신용설정보증금,융자금액,변경후담보비율,원담보금액,부담보금액,소요담보금액,원담보부족금액,
            담보부족금액,추가담보현금,D1주문가능금액,신용이자미납금액,기타대여금액,익일추정반대매매금액,
            원담보합계금액,신용주문가능금액,부담보합계금액,신용담보금현금,신용담보대용금액,추가신용담보현금,
            신용담보재사용금액,추가신용담보대용,매도대금담보대출금액,처분제한금액]
        result.append(lst)
 
    columns=['레코드갯수','지점명','계좌명','현금주문가능금액','출금가능금액','거래소금액','코스닥금액','잔고평가금액','미수금액','예탁자산총액','손익율','투자원금','투자손익금액','신용담보주문금액','예수금','대용금액','D1예수금','D2예수금','현금미수금액','증거금현금','증거금대용','수표금액','대용주문가능금액','증거금률100퍼센트주문가능금액','증거금률35주문가능금액','증거금률50주문가능금액','전일매도정산금액','전일매수정산금액','금일매도정산금액','금일매수정산금액','D1연체변제소요금액','D2연체변제소요금액','D1추정인출가능금액','D2추정인출가능금액','예탁담보대출금액','신용설정보증금','융자금액','변경후담보비율','원담보금액','부담보금액','소요담보금액','원담보부족금액','담보부족금액','추가담보현금','D1주문가능금액','신용이자미납금액','기타대여금액','익일추정반대매매금액','원담보합계금액','신용주문가능금액','부담보합계금액','신용담보금현금','신용담보대용금액','추가신용담보현금','신용담보재사용금액','추가신용담보대용','매도대금담보대출금액','처분제한금액']
    df1 = DataFrame(data=result, columns=columns)
 
    XAQueryEvents.상태 = False
 
    return (df, df1)
 
def CSPAQ12300(레코드갯수,계좌번호,비밀번호,잔고생성구분,수수료적용구분,D2잔고기준조회구분,단가구분):
    '''
    현물계좌잔고내역조회
    '''
    pathname = os.path.dirname(sys.argv[0])
    resdir = os.path.abspath(pathname)
    
    query = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEvents)
 
    MYNAME = inspect.currentframe().f_code.co_name
    INBLOCK = "%sInBlock" % MYNAME
    INBLOCK1 = "%sInBlock1" % MYNAME
    OUTBLOCK = "%sOutBlock" % MYNAME
    OUTBLOCK1 = "%sOutBlock1" % MYNAME
    OUTBLOCK2 = "%sOutBlock2" % MYNAME
    OUTBLOCK3 = "%sOutBlock3" % MYNAME
    RESFILE = "%s\\Res\\%s.res" % (resdir, MYNAME)
 
    print(MYNAME, RESFILE)
 
    query.LoadFromResFile(RESFILE)
    query.SetFieldData(INBLOCK1, "RecCnt", 0, 레코드갯수)
    query.SetFieldData(INBLOCK1, "AcntNo", 0, 계좌번호)
    query.SetFieldData(INBLOCK1, "Pwd", 0, 비밀번호)
    query.SetFieldData(INBLOCK1, "BalCreTp", 0, 잔고생성구분)
    query.SetFieldData(INBLOCK1, "CmsnAppTpCode", 0, 수수료적용구분)
    query.SetFieldData(INBLOCK1, "D2balBaseQryTp", 0, D2잔고기준조회구분)
    query.SetFieldData(INBLOCK1, "UprcTpCode", 0, 단가구분)
    query.Request(0)
 
    while XAQueryEvents.상태 == False:
        pythoncom.PumpWaitingMessages()
 
    result = []
    nCount = query.GetBlockCount(OUTBLOCK1)
    for i in range(nCount):
        레코드갯수 = int(query.GetFieldData(OUTBLOCK1, "RecCnt", i).strip())
        계좌번호 = query.GetFieldData(OUTBLOCK1, "AcntNo", i).strip()
        비밀번호 = query.GetFieldData(OUTBLOCK1, "Pwd", i).strip()
        잔고생성구분 = query.GetFieldData(OUTBLOCK1, "BalCreTp", i).strip()
        수수료적용구분 = query.GetFieldData(OUTBLOCK1, "BalCreTp", i).strip()
        D2잔고기준조회구분 = query.GetFieldData(OUTBLOCK1, "BalCreTp", i).strip()
        단가구분 = query.GetFieldData(OUTBLOCK1, "BalCreTp", i).strip()
 
        lst = [레코드갯수,계좌번호,비밀번호,잔고생성구분,수수료적용구분,D2잔고기준조회구분,단가구분]
        result.append(lst)
 
    df = DataFrame(data=result, columns=['레코드갯수','계좌번호','비밀번호','잔고생성구분','수수료적용구분','D2잔고기준조회구분','단가구분'])
 
    result = []
    nCount = query.GetBlockCount(OUTBLOCK2)
    for i in range(nCount):
        레코드갯수 = int(query.GetFieldData(OUTBLOCK2, "RecCnt", i).strip())
        지점명 = query.GetFieldData(OUTBLOCK2, "BrnNm", i).strip()
        계좌명 = query.GetFieldData(OUTBLOCK2, "AcntNm", i).strip()
        현금주문가능금액 = int(query.GetFieldData(OUTBLOCK2, "MnyOrdAbleAmt", i).strip())
        출금가능금액 = int(query.GetFieldData(OUTBLOCK2, "MnyoutAbleAmt", i).strip())
        거래소금액 = int(query.GetFieldData(OUTBLOCK2, "SeOrdAbleAmt", i).strip())
        코스닥금액 = int(query.GetFieldData(OUTBLOCK2, "KdqOrdAbleAmt", i).strip())
        HTS주문가능금액 = int(query.GetFieldData(OUTBLOCK2, "HtsOrdAbleAmt", i).strip())
        증거금률100퍼센트주문가능금액 = int(query.GetFieldData(OUTBLOCK2, "MgnRat100pctOrdAbleAmt", i).strip())
        잔고평가금액 = int(query.GetFieldData(OUTBLOCK2, "BalEvalAmt", i).strip())
        매입금액 = int(query.GetFieldData(OUTBLOCK2, "PchsAmt", i).strip())
        미수금액 = int(query.GetFieldData(OUTBLOCK2, "RcvblAmt", i).strip())
        손익율 = float(query.GetFieldData(OUTBLOCK2, "PnlRat", i).strip())
        투자원금 = int(query.GetFieldData(OUTBLOCK2, "InvstOrgAmt", i).strip())
        투자손익금액 = int(query.GetFieldData(OUTBLOCK2, "InvstPlAmt", i).strip())
        신용담보주문금액 = int(query.GetFieldData(OUTBLOCK2, "CrdtPldgOrdAmt", i).strip())
        예수금 = int(query.GetFieldData(OUTBLOCK2, "Dps", i).strip())
        D1예수금 = int(query.GetFieldData(OUTBLOCK2, "D1Dps", i).strip())
        D2예수금 = int(query.GetFieldData(OUTBLOCK2, "D2Dps", i).strip())
        주문일 = query.GetFieldData(OUTBLOCK2, "OrdDt", i).strip()
        현금증거금액 = int(query.GetFieldData(OUTBLOCK2, "MnyMgn", i).strip())
        대용증거금액 = int(query.GetFieldData(OUTBLOCK2, "SubstMgn", i).strip())
        대용금액 = int(query.GetFieldData(OUTBLOCK2, "SubstAmt", i).strip())
        전일매수체결금액 = int(query.GetFieldData(OUTBLOCK2, "PrdayBuyExecAmt", i).strip())
        전일매도체결금액 = int(query.GetFieldData(OUTBLOCK2, "PrdaySellExecAmt", i).strip())
        금일매수체결금액 = int(query.GetFieldData(OUTBLOCK2, "CrdayBuyExecAmt", i).strip())
        금일매도체결금액 = int(query.GetFieldData(OUTBLOCK2, "CrdaySellExecAmt", i).strip())
        평가손익합계 = int(query.GetFieldData(OUTBLOCK2, "EvalPnlSum", i).strip())
        예탁자산총액 = int(query.GetFieldData(OUTBLOCK2, "DpsastTotamt", i).strip())
        제비용 = int(query.GetFieldData(OUTBLOCK2, "Evrprc", i).strip())
        재사용금액 = int(query.GetFieldData(OUTBLOCK2, "RuseAmt", i).strip())
        기타대여금액 = int(query.GetFieldData(OUTBLOCK2, "EtclndAmt", i).strip())
        가정산금액 = int(query.GetFieldData(OUTBLOCK2, "PrcAdjstAmt", i).strip())
        D1수수료 = int(query.GetFieldData(OUTBLOCK2, "D1CmsnAmt", i).strip())
        D2수수료 = int(query.GetFieldData(OUTBLOCK2, "D2CmsnAmt", i).strip())
        D1제세금 = int(query.GetFieldData(OUTBLOCK2, "D1EvrTax", i).strip())
        D2제세금 = int(query.GetFieldData(OUTBLOCK2, "D2EvrTax", i).strip())
        D1결제예정금액 = int(query.GetFieldData(OUTBLOCK2, "D1SettPrergAmt", i).strip())
        D2결제예정금액 = int(query.GetFieldData(OUTBLOCK2, "D2SettPrergAmt", i).strip())
        전일KSE현금증거금 = int(query.GetFieldData(OUTBLOCK2, "PrdayKseMnyMgn", i).strip())
        전일KSE대용증거금 = int(query.GetFieldData(OUTBLOCK2, "PrdayKseSubstMgn", i).strip())
        전일KSE신용현금증거금 = int(query.GetFieldData(OUTBLOCK2, "PrdayKseCrdtMnyMgn", i).strip())
        전일KSE신용대용증거금 = int(query.GetFieldData(OUTBLOCK2, "PrdayKseCrdtSubstMgn", i).strip())
        금일KSE현금증거금 = int(query.GetFieldData(OUTBLOCK2, "CrdayKseMnyMgn", i).strip())
        금일KSE대용증거금 = int(query.GetFieldData(OUTBLOCK2, "CrdayKseSubstMgn", i).strip())
        금일KSE신용현금증거금 = int(query.GetFieldData(OUTBLOCK2, "CrdayKseCrdtMnyMgn", i).strip())
        금일KSE신용대용증거금 = int(query.GetFieldData(OUTBLOCK2, "CrdayKseCrdtSubstMgn", i).strip())
        전일코스닥현금증거금 = int(query.GetFieldData(OUTBLOCK2, "PrdayKdqMnyMgn", i).strip())
        전일코스닥대용증거금 = int(query.GetFieldData(OUTBLOCK2, "PrdayKdqSubstMgn", i).strip())
        전일코스닥신용현금증거금 = int(query.GetFieldData(OUTBLOCK2, "PrdayKdqCrdtMnyMgn", i).strip())
        전일코스닥신용대용증거금 = int(query.GetFieldData(OUTBLOCK2, "PrdayKdqCrdtSubstMgn", i).strip())
        금일코스닥현금증거금 = int(query.GetFieldData(OUTBLOCK2, "CrdayKdqMnyMgn", i).strip())
        금일코스닥대용증거금 = int(query.GetFieldData(OUTBLOCK2, "CrdayKdqSubstMgn", i).strip())
        금일코스닥신용현금증거금 = int(query.GetFieldData(OUTBLOCK2, "CrdayKdqCrdtMnyMgn", i).strip())
        금일코스닥신용대용증거금 = int(query.GetFieldData(OUTBLOCK2, "CrdayKdqCrdtSubstMgn", i).strip())
        전일프리보드현금증거금 = int(query.GetFieldData(OUTBLOCK2, "PrdayFrbrdMnyMgn", i).strip())
        전일프리보드대용증거금 = int(query.GetFieldData(OUTBLOCK2, "PrdayFrbrdSubstMgn", i).strip())
        금일프리보드현금증거금 = int(query.GetFieldData(OUTBLOCK2, "CrdayFrbrdMnyMgn", i).strip())
        금일프리보드대용증거금 = int(query.GetFieldData(OUTBLOCK2, "CrdayFrbrdSubstMgn", i).strip())
        전일장외현금증거금 = int(query.GetFieldData(OUTBLOCK2, "PrdayCrbmkMnyMgn", i).strip())
        전일장외대용증거금 = int(query.GetFieldData(OUTBLOCK2, "PrdayCrbmkSubstMgn", i).strip())
        금일장외현금증거금 = int(query.GetFieldData(OUTBLOCK2, "CrdayCrbmkMnyMgn", i).strip())
        금일장외대용증거금 = int(query.GetFieldData(OUTBLOCK2, "CrdayCrbmkSubstMgn", i).strip())
        예탁담보수량 = int(query.GetFieldData(OUTBLOCK2, "DpspdgQty", i).strip())
        매수정산금D2 = int(query.GetFieldData(OUTBLOCK2, "BuyAdjstAmtD2", i).strip())
        매도정산금D2 = int(query.GetFieldData(OUTBLOCK2, "SellAdjstAmtD2", i).strip())
        변제소요금D2 = int(query.GetFieldData(OUTBLOCK2, "RepayRqrdAmtD1", i).strip())
        변제소요금D2 = int(query.GetFieldData(OUTBLOCK2, "RepayRqrdAmtD2", i).strip())
        대출금액 = int(query.GetFieldData(OUTBLOCK2, "LoanAmt", i).strip())
 
        lst = [레코드갯수,지점명,계좌명,현금주문가능금액,출금가능금액,거래소금액,코스닥금액,HTS주문가능금액,증거금률100퍼센트주문가능금액,
            잔고평가금액,매입금액,미수금액,손익율,투자원금,투자손익금액,신용담보주문금액,예수금,D1예수금,D2예수금,주문일,현금증거금액,대용증거금액,
            대용금액,전일매수체결금액,전일매도체결금액,금일매수체결금액,금일매도체결금액,평가손익합계,예탁자산총액,제비용,재사용금액,기타대여금액,
            가정산금액,D1수수료,D2수수료,D1제세금,D2제세금,D1결제예정금액,D2결제예정금액,전일KSE현금증거금,전일KSE대용증거금,전일KSE신용현금증거금,
            전일KSE신용대용증거금,금일KSE현금증거금,금일KSE대용증거금,금일KSE신용현금증거금,금일KSE신용대용증거금,전일코스닥현금증거금,전일코스닥대용증거금,
            전일코스닥신용현금증거금,전일코스닥신용대용증거금,금일코스닥현금증거금,금일코스닥대용증거금,금일코스닥신용현금증거금,금일코스닥신용대용증거금,
            전일프리보드현금증거금,전일프리보드대용증거금,금일프리보드현금증거금,금일프리보드대용증거금,전일장외현금증거금,전일장외대용증거금,금일장외현금증거금,
            금일장외대용증거금,예탁담보수량,매수정산금D2,매도정산금D2,변제소요금D2,변제소요금D2,대출금액]
        result.append(lst)
 
    df1 = DataFrame(data=result, columns=['레코드갯수','지점명','계좌명','현금주문가능금액','출금가능금액','거래소금액','코스닥금액','HTS주문가능금액','증거금률100퍼센트주문가능금액','잔고평가금액','매입금액','미수금액','손익율','투자원금','투자손익금액','신용담보주문금액','예수금','D1예수금','D2예수금','주문일','현금증거금액','대용증거금액','대용금액','전일매수체결금액','전일매도체결금액','금일매수체결금액','금일매도체결금액','평가손익합계','예탁자산총액','제비용','재사용금액','기타대여금액','가정산금액','D1수수료','D2수수료','D1제세금','D2제세금','D1결제예정금액','D2결제예정금액','전일KSE현금증거금','전일KSE대용증거금','전일KSE신용현금증거금','전일KSE신용대용증거금','금일KSE현금증거금','금일KSE대용증거금','금일KSE신용현금증거금','금일KSE신용대용증거금','전일코스닥현금증거금','전일코스닥대용증거금','전일코스닥신용현금증거금','전일코스닥신용대용증거금','금일코스닥현금증거금','금일코스닥대용증거금','금일코스닥신용현금증거금','금일코스닥신용대용증거금','전일프리보드현금증거금','전일프리보드대용증거금','금일프리보드현금증거금','금일프리보드대용증거금','전일장외현금증거금','전일장외대용증거금','금일장외현금증거금','금일장외대용증거금','예탁담보수량','매수정산금D2','매도정산금D2','변제소요금D2','변제소요금D2','대출금액'])
 
    result = []
    nCount = query.GetBlockCount(OUTBLOCK3)
    for i in range(nCount):
        종목번호 = query.GetFieldData(OUTBLOCK3, "IsuNo", i).strip()
        종목명 = query.GetFieldData(OUTBLOCK3, "IsuNm", i).strip()
        유가증권잔고유형코드 = query.GetFieldData(OUTBLOCK3, "SecBalPtnCode", i).strip()
        유가증권잔고유형명 = query.GetFieldData(OUTBLOCK3, "SecBalPtnNm", i).strip()
        잔고수량 = int(query.GetFieldData(OUTBLOCK3, "BalQty", i).strip())
        매매기준잔고수량 = int(query.GetFieldData(OUTBLOCK3, "BnsBaseBalQty", i).strip())
        금일매수체결수량 = int(query.GetFieldData(OUTBLOCK3, "CrdayBuyExecQty", i).strip())
        금일매도체결수량 = int(query.GetFieldData(OUTBLOCK3, "CrdaySellExecQty", i).strip())
        매도가 = float(query.GetFieldData(OUTBLOCK3, "SellPrc", i).strip())
        매수가 = float(query.GetFieldData(OUTBLOCK3, "BuyPrc", i).strip())
        매도손익금액 = int(query.GetFieldData(OUTBLOCK3, "SellPnlAmt", i).strip())
        손익율 = float(query.GetFieldData(OUTBLOCK3, "PnlRat", i).strip())
        현재가 = float(query.GetFieldData(OUTBLOCK3, "NowPrc", i).strip())
        신용금액 = int(query.GetFieldData(OUTBLOCK3, "CrdtAmt", i).strip())
        만기일 = query.GetFieldData(OUTBLOCK3, "DueDt", i).strip()
        전일매도체결가 = float(query.GetFieldData(OUTBLOCK3, "PrdaySellExecPrc", i).strip())
        전일매도수량 = int(query.GetFieldData(OUTBLOCK3, "PrdaySellQty", i).strip())
        전일매수체결가 = float(query.GetFieldData(OUTBLOCK3, "PrdayBuyExecPrc", i).strip())
        전일매수수량 = int(query.GetFieldData(OUTBLOCK3, "PrdayBuyQty", i).strip())
        대출일 = query.GetFieldData(OUTBLOCK3, "LoanDt", i).strip()
        평균단가 = float(query.GetFieldData(OUTBLOCK3, "AvrUprc", i).strip())
        매도가능수량 = int(query.GetFieldData(OUTBLOCK3, "SellAbleQty", i).strip())
        매도주문수량 = int(query.GetFieldData(OUTBLOCK3, "SellOrdQty", i).strip())
        금일매수체결금액 = int(query.GetFieldData(OUTBLOCK3, "CrdayBuyExecAmt", i).strip())
        금일매도체결금액 = int(query.GetFieldData(OUTBLOCK3, "CrdaySellExecAmt", i).strip())
        전일매수체결금액 = int(query.GetFieldData(OUTBLOCK3, "PrdayBuyExecAmt", i).strip())
        전일매도체결금액 = int(query.GetFieldData(OUTBLOCK3, "PrdaySellExecAmt", i).strip())
        잔고평가금액 = int(query.GetFieldData(OUTBLOCK3, "BalEvalAmt", i).strip())
        평가손익 = int(query.GetFieldData(OUTBLOCK3, "EvalPnl", i).strip())
        현금주문가능금액 = int(query.GetFieldData(OUTBLOCK3, "MnyOrdAbleAmt", i).strip())
        주문가능금액 = int(query.GetFieldData(OUTBLOCK3, "OrdAbleAmt", i).strip())
        매도미체결수량 = int(query.GetFieldData(OUTBLOCK3, "SellUnercQty", i).strip())
        매도미결제수량 = int(query.GetFieldData(OUTBLOCK3, "SellUnsttQty", i).strip())
        매수미체결수량 = int(query.GetFieldData(OUTBLOCK3, "BuyUnercQty", i).strip())
        매수미결제수량 = int(query.GetFieldData(OUTBLOCK3, "BuyUnsttQty", i).strip())
        미결제수량 = int(query.GetFieldData(OUTBLOCK3, "UnsttQty", i).strip())
        미체결수량 = int(query.GetFieldData(OUTBLOCK3, "UnercQty", i).strip())
        전일종가 = float(query.GetFieldData(OUTBLOCK3, "PrdayCprc", i).strip())
        매입금액 = int(query.GetFieldData(OUTBLOCK3, "PchsAmt", i).strip())
        등록시장코드 = query.GetFieldData(OUTBLOCK3, "RegMktCode", i).strip()
        대출상세분류코드 = query.GetFieldData(OUTBLOCK3, "LoanDtlClssCode", i).strip()
        예탁담보대출수량 = int(query.GetFieldData(OUTBLOCK3, "DpspdgLoanQty", i).strip())
 
        lst = [종목번호,종목명,유가증권잔고유형코드,유가증권잔고유형명,잔고수량,매매기준잔고수량,금일매수체결수량,금일매도체결수량,매도가,
            매수가,매도손익금액,손익율,현재가,신용금액,만기일,전일매도체결가,전일매도수량,전일매수체결가,전일매수수량,대출일,평균단가,매도가능수량,
            매도주문수량,금일매수체결금액,금일매도체결금액,전일매수체결금액,전일매도체결금액,잔고평가금액,평가손익,현금주문가능금액,
            주문가능금액,매도미체결수량,매도미결제수량,매수미체결수량,매수미결제수량,미결제수량,미체결수량,전일종가,매입금액,등록시장코드,
            대출상세분류코드,예탁담보대출수량]
        result.append(lst)
 
    df2 = DataFrame(data=result, columns=['종목번호','종목명','유가증권잔고유형코드','유가증권잔고유형명','잔고수량','매매기준잔고수량','금일매수체결수량','금일매도체결수량','매도가','매수가','매도손익금액','손익율','현재가','신용금액','만기일','전일매도체결가','전일매도수량','전일매수체결가','전일매수수량','대출일','평균단가','매도가능수량','매도주문수량','금일매수체결금액','금일매도체결금액','전일매수체결금액','전일매도체결금액','잔고평가금액','평가손익','현금주문가능금액','주문가능금액','매도미체결수량','매도미결제수량','매수미체결수량','매수미결제수량','미결제수량','미체결수량','전일종가','매입금액','등록시장코드','대출상세분류코드','예탁담보대출수량'])
 
    XAQueryEvents.상태 = False
 
    return (df, df1, df2)
 
def CSPAQ13700(레코드갯수,계좌번호,입력비밀번호,주문시장코드,매매구분,종목번호,체결여부,주문일,시작주문번호2,역순구분,주문유형코드):
    '''
    현물계좌 주문체결 내역 조회
    '''
    pathname = os.path.dirname(sys.argv[0])
    resdir = os.path.abspath(pathname)
    
    query = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEvents)
 
    MYNAME = inspect.currentframe().f_code.co_name
    INBLOCK = "%sInBlock" % MYNAME
    INBLOCK1 = "%sInBlock1" % MYNAME
    OUTBLOCK = "%sOutBlock" % MYNAME
    OUTBLOCK1 = "%sOutBlock1" % MYNAME
    OUTBLOCK2 = "%sOutBlock2" % MYNAME
    OUTBLOCK3 = "%sOutBlock3" % MYNAME
    RESFILE = "%s\\Res\\%s.res" % (resdir, MYNAME)
 
    print(MYNAME, RESFILE)
 
    query.LoadFromResFile(RESFILE)
    query.SetFieldData(INBLOCK1, "RecCnt", 0, 레코드갯수)
    query.SetFieldData(INBLOCK1, "AcntNo", 0, 계좌번호)
    query.SetFieldData(INBLOCK1, "InptPwd", 0, 입력비밀번호)
    query.SetFieldData(INBLOCK1, "OrdMktCode", 0, 주문시장코드)
    query.SetFieldData(INBLOCK1, "BnsTpCode", 0, 매매구분)
    query.SetFieldData(INBLOCK1, "IsuNo", 0, 종목번호)
    query.SetFieldData(INBLOCK1, "ExecYn", 0, 체결여부)
    query.SetFieldData(INBLOCK1, "OrdDt", 0, 주문일)
    query.SetFieldData(INBLOCK1, "SrtOrdNo2", 0, 시작주문번호2)
    query.SetFieldData(INBLOCK1, "BkseqTpCode", 0, 역순구분)
    query.SetFieldData(INBLOCK1, "OrdPtnCode", 0, 주문유형코드)
    query.Request(0)
 
    while XAQueryEvents.상태 == False:
        pythoncom.PumpWaitingMessages()
 
    result = []
    nCount = query.GetBlockCount(OUTBLOCK1)
    for i in range(nCount):
        레코드갯수 = int(query.GetFieldData(OUTBLOCK1, "RecCnt", i).strip())
        계좌번호 = query.GetFieldData(OUTBLOCK1, "AcntNo", i).strip()
        입력비밀번호 = query.GetFieldData(OUTBLOCK1, "InptPwd", i).strip()
        주문시장코드 = query.GetFieldData(OUTBLOCK1, "OrdMktCode", i).strip()
        매매구분 = query.GetFieldData(OUTBLOCK1, "BnsTpCode", i).strip()
        종목번호 = query.GetFieldData(OUTBLOCK1, "IsuNo", i).strip()
        체결여부 = query.GetFieldData(OUTBLOCK1, "ExecYn", i).strip()
        주문일 = query.GetFieldData(OUTBLOCK1, "OrdDt", i).strip()
        시작주문번호2 = int(query.GetFieldData(OUTBLOCK1, "SrtOrdNo2", i).strip())
        역순구분 = query.GetFieldData(OUTBLOCK1, "BkseqTpCode", i).strip()
        주문유형코드 = query.GetFieldData(OUTBLOCK1, "OrdPtnCode", i).strip()
 
        lst = [레코드갯수,계좌번호,입력비밀번호,주문시장코드,매매구분,종목번호,체결여부,주문일,시작주문번호2,역순구분,주문유형코드]
        result.append(lst)
 
    df = DataFrame(data=result, columns=['레코드갯수','계좌번호','입력비밀번호','주문시장코드','매매구분','종목번호','체결여부','주문일','시작주문번호2','역순구분','주문유형코드'])
 
    result = []
    nCount = query.GetBlockCount(OUTBLOCK2)
    for i in range(nCount):
        레코드갯수 = int(query.GetFieldData(OUTBLOCK2, "RecCnt", i).strip())
        매도체결금액 = int(query.GetFieldData(OUTBLOCK2, "SellExecAmt", i).strip())
        매수체결금액 = int(query.GetFieldData(OUTBLOCK2, "BuyExecAmt", i).strip())
        매도체결수량 = int(query.GetFieldData(OUTBLOCK2, "SellExecQty", i).strip())
        매수체결수량 = int(query.GetFieldData(OUTBLOCK2, "BuyExecQty", i).strip())
        매도주문수량 = int(query.GetFieldData(OUTBLOCK2, "SellOrdQty", i).strip())
        매수주문수량 = int(query.GetFieldData(OUTBLOCK2, "BuyOrdQty", i).strip())
 
        lst = [레코드갯수,매도체결금액,매수체결금액,매도체결수량,매수체결수량,매도주문수량,매수주문수량]
        result.append(lst)
 
    df1 = DataFrame(data=result, columns=['레코드갯수','매도체결금액','매수체결금액','매도체결수량','매수체결수량','매도주문수량','매수주문수량'])
 
    result = []
    nCount = query.GetBlockCount(OUTBLOCK3)
    for i in range(nCount):
        주문일 = query.GetFieldData(OUTBLOCK3, "OrdDt", i).strip()
        관리지점번호 = query.GetFieldData(OUTBLOCK3, "MgmtBrnNo", i).strip()
        주문시장코드 = query.GetFieldData(OUTBLOCK3, "OrdMktCode", i).strip()
        주문번호 = int(query.GetFieldData(OUTBLOCK3, "OrdNo", i).strip())
        원주문번호 = int(query.GetFieldData(OUTBLOCK3, "OrgOrdNo", i).strip())
        종목번호 = query.GetFieldData(OUTBLOCK3, "IsuNo", i).strip()
        종목명 = query.GetFieldData(OUTBLOCK3, "IsuNm", i).strip()
        매매구분 = query.GetFieldData(OUTBLOCK3, "BnsTpCode", i).strip()
        매매구분 = query.GetFieldData(OUTBLOCK3, "BnsTpNm", i).strip()
        주문유형코드 = query.GetFieldData(OUTBLOCK3, "OrdPtnCode", i).strip()
        주문유형명 = query.GetFieldData(OUTBLOCK3, "OrdPtnNm", i).strip()
        주문처리유형코드 = int(query.GetFieldData(OUTBLOCK3, "OrdTrxPtnCode", i).strip())
        주문처리유형명 = query.GetFieldData(OUTBLOCK3, "OrdTrxPtnNm", i).strip()
        정정취소구분 = query.GetFieldData(OUTBLOCK3, "MrcTpCode", i).strip()
        정정취소구분명 = query.GetFieldData(OUTBLOCK3, "MrcTpNm", i).strip()
        정정취소수량 = int(query.GetFieldData(OUTBLOCK3, "MrcQty", i).strip())
        정정취소가능수량 = int(query.GetFieldData(OUTBLOCK3, "MrcAbleQty", i).strip())
        주문수량 = int(query.GetFieldData(OUTBLOCK3, "OrdQty", i).strip())
        주문가격 = float(query.GetFieldData(OUTBLOCK3, "OrdPrc", i).strip())
        체결수량 = int(query.GetFieldData(OUTBLOCK3, "ExecQty", i).strip())
        체결가 = float(query.GetFieldData(OUTBLOCK3, "ExecPrc", i).strip())
        체결처리시각 = query.GetFieldData(OUTBLOCK3, "ExecTrxTime", i).strip()
        최종체결시각 = query.GetFieldData(OUTBLOCK3, "LastExecTime", i).strip()
        호가유형코드 = query.GetFieldData(OUTBLOCK3, "OrdprcPtnCode", i).strip()
        호가유형명 = query.GetFieldData(OUTBLOCK3, "OrdprcPtnNm", i).strip()
        주문조건구분 = query.GetFieldData(OUTBLOCK3, "OrdCndiTpCode", i).strip()
        전체체결수량 = int(query.GetFieldData(OUTBLOCK3, "AllExecQty", i).strip())
        통신매체코드 = query.GetFieldData(OUTBLOCK3, "RegCommdaCode", i).strip()
        통신매체명 = query.GetFieldData(OUTBLOCK3, "CommdaNm", i).strip()
        회원번호 = query.GetFieldData(OUTBLOCK3, "MbrNo", i).strip()
        예약주문여부 = query.GetFieldData(OUTBLOCK3, "RsvOrdYn", i).strip()
        대출일 = query.GetFieldData(OUTBLOCK3, "LoanDt", i).strip()
        주문시각 = query.GetFieldData(OUTBLOCK3, "OrdTime", i).strip()
        운용지시번호 = query.GetFieldData(OUTBLOCK3, "OpDrtnNo", i).strip()
        주문자ID = query.GetFieldData(OUTBLOCK3, "OdrrId", i).strip()
 
        lst = [주문일,관리지점번호,주문시장코드,주문번호,원주문번호,종목번호,종목명,매매구분,매매구분,주문유형코드,주문유형명,주문처리유형코드,주문처리유형명,
            정정취소구분,정정취소구분명,정정취소수량,정정취소가능수량,주문수량,주문가격,체결수량,체결가,체결처리시각,최종체결시각,호가유형코드,호가유형명,
            주문조건구분,전체체결수량,통신매체코드,통신매체명,회원번호,예약주문여부,대출일,주문시각,운용지시번호,주문자ID]
        result.append(lst)
 
    df2 = DataFrame(data=result, columns=['주문일','관리지점번호','주문시장코드','주문번호','원주문번호','종목번호','종목명','매매구분','매매구분','주문유형코드','주문유형명','주문처리유형코드','주문처리유형명','정정취소구분','정정취소구분명','정정취소수량','정정취소가능수량','주문수량','주문가격','체결수량','체결가','체결처리시각','최종체결시각','호가유형코드','호가유형명','주문조건구분','전체체결수량','통신매체코드','통신매체명','회원번호','예약주문여부','대출일','주문시각','운용지시번호','주문자ID'])
 
    XAQueryEvents.상태 = False
 
    return (df, df1, df2)
 
 
def t0424(계좌번호='',비밀번호='',단가구분='1',체결구분='0',단일가구분='0',제비용포함여부='1',CTS_종목번호=''):
    '''
    주식잔고2
    '''
    pathname = os.path.dirname(sys.argv[0])
    resdir = os.path.abspath(pathname)
    
    query = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEvents)
 
    MYNAME = inspect.currentframe().f_code.co_name
    INBLOCK = "%sInBlock" % MYNAME
    INBLOCK1 = "%sInBlock1" % MYNAME
    OUTBLOCK = "%sOutBlock" % MYNAME
    OUTBLOCK1 = "%sOutBlock1" % MYNAME
    OUTBLOCK2 = "%sOutBlock2" % MYNAME
    RESFILE = "%s\\Res\\%s.res" % (resdir, MYNAME)
 
    print(MYNAME, RESFILE)
 
    query.LoadFromResFile(RESFILE)
    query.SetFieldData(INBLOCK, "accno", 0, 계좌번호)
    query.SetFieldData(INBLOCK, "passwd", 0, 비밀번호)
    query.SetFieldData(INBLOCK, "prcgb", 0, 단가구분)
    query.SetFieldData(INBLOCK, "chegb", 0, 체결구분)
    query.SetFieldData(INBLOCK, "dangb", 0, 단일가구분)
    query.SetFieldData(INBLOCK, "charge", 0, 제비용포함여부)
    query.SetFieldData(INBLOCK, "cts_expcode", 0, CTS_종목번호)
    query.Request(0)
 
    while XAQueryEvents.상태 == False:
        pythoncom.PumpWaitingMessages()
 
    result = []
    nCount = query.GetBlockCount(OUTBLOCK)
    for i in range(nCount):
        추정순자산 = int(query.GetFieldData(OUTBLOCK, "sunamt", i).strip())
        실현손익 = int(query.GetFieldData(OUTBLOCK, "dtsunik", i).strip())
        매입금액 = int(query.GetFieldData(OUTBLOCK, "mamt", i).strip())
        추정D2예수금 =int( query.GetFieldData(OUTBLOCK, "sunamt1", i).strip())
        CTS_종목번호 = query.GetFieldData(OUTBLOCK, "cts_expcode", i).strip()
        평가금액 = int(query.GetFieldData(OUTBLOCK, "tappamt", i).strip())
        평가손익 = int(query.GetFieldData(OUTBLOCK, "tdtsunik", i).strip())
 
        lst = [추정순자산,실현손익,매입금액,추정D2예수금,CTS_종목번호,평가금액,평가손익]
        result.append(lst)
 
    columns=['추정순자산','실현손익','매입금액','추정D2예수금','CTS_종목번호','평가금액','평가손익']
    df = DataFrame(data=result, columns=columns)
 
    result = []
    nCount = query.GetBlockCount(OUTBLOCK1)
    for i in range(nCount):
        종목번호 = query.GetFieldData(OUTBLOCK1, "expcode", i).strip()
        잔고구분 = query.GetFieldData(OUTBLOCK1, "jangb", i).strip()
        잔고수량 = int(query.GetFieldData(OUTBLOCK1, "janqty", i).strip())
        매도가능수량 = int(query.GetFieldData(OUTBLOCK1, "mdposqt", i).strip())
        평균단가 = int(query.GetFieldData(OUTBLOCK1, "pamt", i).strip())
        매입금액 = int(query.GetFieldData(OUTBLOCK1, "mamt", i).strip())
        대출금액 = int(query.GetFieldData(OUTBLOCK1, "sinamt", i).strip())
        만기일자 = query.GetFieldData(OUTBLOCK1, "lastdt", i).strip()
        당일매수금액 = int(query.GetFieldData(OUTBLOCK1, "msat", i).strip())
        당일매수단가 = int(query.GetFieldData(OUTBLOCK1, "mpms", i).strip())
        당일매도금액 = int(query.GetFieldData(OUTBLOCK1, "mdat", i).strip())
        당일매도단가 = int(query.GetFieldData(OUTBLOCK1, "mpmd", i).strip())
        전일매수금액 = int(query.GetFieldData(OUTBLOCK1, "jsat", i).strip())
        전일매수단가 = int(query.GetFieldData(OUTBLOCK1, "jpms", i).strip())
        전일매도금액 = int(query.GetFieldData(OUTBLOCK1, "jdat", i).strip())
        전일매도단가 = int(query.GetFieldData(OUTBLOCK1, "jpmd", i).strip())
        처리순번 = int(query.GetFieldData(OUTBLOCK1, "sysprocseq", i).strip())
        대출일자 = query.GetFieldData(OUTBLOCK1, "loandt", i).strip()
        종목명 = query.GetFieldData(OUTBLOCK1, "hname", i).strip()
        시장구분 = query.GetFieldData(OUTBLOCK1, "marketgb", i).strip()
        종목구분 = query.GetFieldData(OUTBLOCK1, "jonggb", i).strip()
        보유비중 = float(query.GetFieldData(OUTBLOCK1, "janrt", i).strip())
        현재가 = int(query.GetFieldData(OUTBLOCK1, "price", i).strip())
        평가금액 = int(query.GetFieldData(OUTBLOCK1, "appamt", i).strip())
        평가손익 = int(query.GetFieldData(OUTBLOCK1, "dtsunik", i).strip())
        수익율 = float(query.GetFieldData(OUTBLOCK1, "sunikrt", i).strip())
        수수료 = int(query.GetFieldData(OUTBLOCK1, "fee", i).strip())
        제세금 = int(query.GetFieldData(OUTBLOCK1, "tax", i).strip())
        신용이자 = int(query.GetFieldData(OUTBLOCK1, "sininter", i).strip())
 
        lst = [종목번호,잔고구분,잔고수량,매도가능수량,평균단가,매입금액,대출금액,만기일자,당일매수금액,
            당일매수단가,당일매도금액,당일매도단가,전일매수금액,전일매수단가,전일매도금액,전일매도단가,
            처리순번,대출일자,종목명,시장구분,종목구분,보유비중,현재가,평가금액,평가손익,수익율,수수료,제세금,신용이자]
        result.append(lst)
 
    columns=['종목번호','잔고구분','잔고수량','매도가능수량','평균단가','매입금액','대출금액','만기일자','당일매수금액',' 당일매수단가','당일매도금액','당일매도단가','전일매수금액','전일매수단가','전일매도금액','전일매도단가',' 처리순번','대출일자','종목명','시장구분','종목구분','보유비중','현재가','평가금액','평가손익','수익율','수수료','제세금','신용이자']
    df1 = DataFrame(data=result, columns=columns)
 
    XAQueryEvents.상태 = False
 
    return (df, df1)
 
def t0425(계좌번호='',비밀번호='',종목번호='',체결구분='0',매매구분='0',정렬순서='2',주문번호=''):
    '''
    주식 체결/미체결
    '''
    pathname = os.path.dirname(sys.argv[0])
    resdir = os.path.abspath(pathname)
    
    query = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEvents)
 
    MYNAME = inspect.currentframe().f_code.co_name
    INBLOCK = "%sInBlock" % MYNAME
    INBLOCK1 = "%sInBlock1" % MYNAME
    OUTBLOCK = "%sOutBlock" % MYNAME
    OUTBLOCK1 = "%sOutBlock1" % MYNAME
    OUTBLOCK2 = "%sOutBlock2" % MYNAME
    RESFILE = "%s\\Res\\%s.res" % (resdir, MYNAME)
 
    print(MYNAME, RESFILE)
 
    query.LoadFromResFile(RESFILE)
    query.SetFieldData(INBLOCK, "accno", 0, 계좌번호)
    query.SetFieldData(INBLOCK, "passwd", 0, 비밀번호)
    query.SetFieldData(INBLOCK, "expcode", 0, 종목번호)
    query.SetFieldData(INBLOCK, "chegb", 0, 체결구분)
    query.SetFieldData(INBLOCK, "medosu", 0, 매매구분)
    query.SetFieldData(INBLOCK, "sortgb", 0, 정렬순서)
    query.SetFieldData(INBLOCK, "cts_ordno", 0, 주문번호)
    query.Request(0)
 
    while XAQueryEvents.상태 == False:
        pythoncom.PumpWaitingMessages()
 
    result = []
    nCount = query.GetBlockCount(OUTBLOCK)
    for i in range(nCount):
        총주문수량 = int(query.GetFieldData(OUTBLOCK, "tqty", i).strip())
        총체결수량 = int(query.GetFieldData(OUTBLOCK, "tcheqty", i).strip())
        총미체
