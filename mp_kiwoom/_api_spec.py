# -*- coding=utf-8 -*-
"""
주요 기능: 
    - eBest API spec 추출: C:/eBEST/xingAPI/Res/*.Res -> mongodb/sats/collections
    - 저장(mongodb/xlsx)/변경
        - api_requests_spec_ebest: spec 원본
        - api_requests_user_ebest: 사용자 수정본
        - api_requests_spec_ebest_bk: spec 원본 백업
사용례: 
    - Res 파일 -> Database(mongodb) 저장: save_all_res_to_db()
    - Database(mongodb) -> 파일(../staff/api_ebest_for_data.py, ...) blocks 부분 업데이트
        - insert_blocks_file_by_db(path='../staff/api_ebest_for_condition_.py', res_codes=['t1857'], division='spec')
        실제 사용할 block, field만 파일에 입력
        - insert_blocks_file_by_db(path='../staff/api_ebest_for_data.py', res_codes=['t0150', 't0424', 't8411'], division='user')
        * block, field 사용여부에 관계없이 모두 파일에 입력

    - 파일(../staff/api_ebest_for_data.py, ...) -> Database(mongodb) 업데이트
        - update_db_by_file(path='../staff/api_ebest_for_order.py', agency='ebest', separator='`')
        - update_db_by_file(path='../staff/api_ebest_for_data.py', agency='ebest', separator='`')

    - 리스트 저장
        - list_req_to_file(kind='TR', agency='ebest')
        - list_req_to_file(kind='Real', agency='ebest')

    - usage(용도) / priority(중요도: 1~5) / goods(현물/선물/EUREX/...) 업데이트
        - update_db_usage_by_file(path="_api_res/list_TR.py")
            * res_codes = find_reqs_by_query(query={'kind': 'TR', 'goods': '현물', 'usage': 'order', 'priority': {'$gt' : 3}}, fields=['res_code'], agency='ebest')

    - 용도/중요도에 맞는 request 파일에 입력
        - query={'kind': 'TR', 'goods': '현물', 'usage': 'order', 'priority': {'$gt' : 3}}
        - insert_blocks_file_by_query(path='../staff/api_ebest_for_order.py', query=query, use=False, agency='ebest')

        - query={'kind': 'TR', 'goods': '현물', 'usage': 'data', 'priority': {'$gt' : 4}}
        - insert_blocks_file_by_query(path='../staff/api_ebest_for_data.py', query=query, use=False, agency='ebest')

    - field의 eng, kor값 획득
        r = find_fields_eng_kor(agency='ebest')
        print(r)

        {'kind': 'TR', 'usage': {'$exists': False}}
        db.api_requests_user_ebest.count({'kind': 'TR', 'usage': {'$exists': false}})

        count_eng_kor()

    - 초기 설정 순서
        1: save_all_res_to_db()
        1.5: req 리스트 파일 생성 -> 편집(있는 경우 생략)
        list_req_to_file(kind='TR', agency='ebest') / list_req_to_file(kind='Real', agency='ebest')
        2: 사용, 중요도 등 표시 -> DB update
        update_db_usage_by_file(path="_api_res/list_TR.py") / update_db_usage_by_file(path="_api_res/list_Real.py")
        3: .py 파일 변경
        query={'kind': 'TR', 'goods': '현물', 'usage': 'order', 'priority': {'$gt' : 3}}

"""

##@@@ 모듈 import
##============================================================

##@@ Built-In 모듈
##------------------------------------------------------------
import sys, os, re, json, time, shutil
from ast import literal_eval

##@@ Package 모듈
##------------------------------------------------------------


##@@ User 모듈
##------------------------------------------------------------
sys.path.append(os.path.join(os.path.dirname(__file__), '../../_public'))
from utils_basic import (
    _read_file, 
    _write_file, 
    _create_folder
)

from utils_mongo import (
    upsert_docs, 
    upsert_doc, 
    find_doc, 
    find_docs, 
    collection_to_json,
    copy_collection, 
    drop_collection
)

from utils_xlsx import (
    read_xsheet,
    write_xsheet
)

##@@@ 전역 상수/변수
##============================================================

##@@ 파일 경로
##------------------------------------------------------------
RES_PATH = "C:/eBEST/xingAPI/Res/"

##@@ 정규표현식(Regex): .Res 파일 Read -> Json
##------------------------------------------------------------
DEL3 = [r'(.*?),(.*?),(.*?),(.*?),(.*?);', r'\1,\2,\4,\5;']  # 중복 삭제 : 수수료금액,CmsnAmt,CmsnAmt,long,16 -> 수수료금액,CmsnAmt,long,16

REPLACEMETS = {
    r'\s*\n+\s*': ';', 
    r'\s*,+\s*': ',',
    r';\/\*(.+?)\*\/': r'(\1);', # TODO: 코멘트도 저장(t1901) ETP상품구분코드,etp_gb,etp_gb,char,1;/*1:ETF(투자회사형)2:ETF(수익증권형)3:ETN4:손실제한ETN*/
    r';{2,}': ';',
}

REPLACEMETS_BLOCKS = {
    r'\{\n *"desc" *: *"(.+)",': r'{  ### \1', # desc 코멘트 처리
    r'"([a-zA-Z_0-9]+)" *: *"([io])`(.*?`.*?`.*?`n`.*?`.*?)"(,*)': r'# "\1": "\2`\3"\4', # TODO: use 여부 표시(코멘트 처리)
    r'"([a-zA-Z_0-9]+)" *: *"i`(.*?)`(.*?)`(.*?)`(.*?)`([\d\-\.]+)`(.*?)"(,*)': r'"\1": \6\8  # {\2} \7',  #  숫자, '.', '-'로만 이루어진 경우 따옴표 제거  # inblock
    r'"([a-zA-Z_0-9]+)" *: *"i`(.*?)`(.*?)`(.*?)`(.*?)`([a-zA-Z_\(\)]{5,}.*)`(.*?)"(,*)': r'"\1": \6\8  # {\2} \7',  #  숫자, '.', '-'로만 이루어진 경우 따옴표 제거  # inblock
    r'"([a-zA-Z_0-9]+)" *: *"i`(.*?)`(.*?)`(.*?)`(.*?)`(.*?)`(.*?)"(,*)': r'"\1": "\6"\8  # {\2} \7',  # inblock 일반
    r'"([a-zA-Z_0-9]+)" *: *"o`(.*?)`(.*?)`(.*?)`(.*?)`(.*?)`(.*?)"(,*)': r'"\1": "\6`\3"\8  # {\2} \7', # outblock
}

REPLACEMETS_BLOCKS2 = {
    r'\{ *#.+': '{',
    r'# *\{.+\} *': '#',
    r'"([a-zA-Z_0-9]+)": *"(.*?)`.*?"[, ]*# *(.*)': r'"\1": "\2`\3",',  # outblock
    r'"([a-zA-Z_0-9]+)":[ "]*(.*?)[", ]*# *(.*)': r'"\1": "\2`\3",',  # inblock
}

## NOTE: inblock 디폴트값 변경
REPLACEMETS_INBLOCKS3 = {
    '"sdate": " "': '"sdate": datetime.now().strftime' + "('%Y%m%d')",  # 조회 시작일
    '"edate": " "': '"edate": datetime.now().strftime' + "('%Y%m%d')",  # 조회 종료일
    '"comp_yn": " "': '"comp_yn": "Y"',  # 압축 전송 여부
    '"shcode": " "': '"shcode": "005930"',  # 종목코드
    '"qrycnt": 0': '"qrycnt": 2000',  # 1회 조회 건수
    '"ncnt": 0': '"ncnt": 1',  # 틱(분)개수 단위?
}

## NOTE: outnblock nick값 변경
REPLACEMETS_OUTBLOCKS3 = {

}


##@@@ 보조 함수
##============================================================

##@@ 치환, 파일
##------------------------------------------------------------

def _replace_re(replace_dict="", string=""):
    """문자열 치환(정규식)

    Args:
        replace_dict (str, optional): {r'old': r'new', ...}. Defaults to "".
        string (str, optional): [description]. Defaults to "".

    Returns:
        [type]: [description]
    """
    for key, val in replace_dict.items():
        string = re.sub(key, val, string)
    return string


def _files_in_folder(folder='', filter_fn=None):
    """폴더 내의 파일 리스트

    Args:
        folder (str, optional): 폴더 이름. 예) "C:/eBEST/xingAPI/Res/" Defaults to ''.
        filter_fn (function, optional): callback(filter 함수). 예) lambda x: x.find("_1") < 1 and x.find("_2") < 1 Defaults to None.

    Returns:
        [type]: [description]
    """
    files = os.listdir(folder)
    if filter_fn != None:
        files = filter(filter_fn, files)
    return list(files)


# def _indent(n=1, indent_unit=4, use=False):
#     if use:
#         space = "\t"*n
#     else:
#         space = " "*indent_unit*n
#     return space

##@@ Res 파일 -> Database(mongodb) 저장
##------------------------------------------------------------

def _set_feild_key_val(old=[], order=[1, 7, 0, 2, 3, 6, 5, 4], separator='`'):
    """필드 key, val 설정

    Args:
        old (list, optional): 기존 순서. ex) [eng, kor, type, len, use, default, remark] Defaults to [].
        order (list, optional): 변경 순서. ex) [1, 0, 2, 3, 6, 5, 4]. Defaults to [1, 7, 0, 2, 3, 6, 5, 4].
        separator (str, optional): [description]. Defaults to '`'.
    Usages:
        inblock: 
        [eng, kor, type, len, use, default, remark]
        [1, 0, 2, 3, 6, 5, 4] 'eng`kor`type`len`use`default`remark'
        outblock
        [eng, kor, type, len, use, nick, remark]
        [1, 0, 2, 3, 6, 5, 4] 'eng`kor`type`len`use`nick`remark'
    """
    new = [old[i] for i in order]
    return [new[0], separator.join(new[1:])]


def _set_inblock_dict(block_name='InBlock', field='', separator='`'):
    """InBlock 설정

    Args:
        block_name (str, optional): 'InBlock' . Defaults to 'InBlock'.
        field (str, optional): 필드명. Defaults to ''.
        separator (str, optional): 필드 구분자. Defaults to '`'.

    Returns:
        [type]: [description]
    """

    _list = ['' for _ in range(0, 8)]  # NOTE: ['kor', 'eng', 'type', 'len', 'remark']
    for i, v in enumerate(field.split(',')):
        if '('  in v and (':'  in v or '/' in v):  # NOTE: '요청건수(최대-압축:2000비압축:500)' 등 괄호 안에 있는 내용은 remark로
            idx = v.index('(')
            _list[i] = v[:idx]
            _list[4] = v[idx+1:-1]
        else:
            _list[i] = v
    
    if _list[2] == 'long' or _list[2] == 'int':
        default = '0'
    elif _list[2] == 'double' or _list[2] == 'float':
        default = '0.0'
    else:  # 'char', 'string'
        default = ' '

    _list[5] = default  # default 추가
    _list[6] = 'n'  # use 추가 (y: 사용, n: 미사용 / default: n)
    _list[7] = 'i'  # NOTE: inblock 표시

    return _set_feild_key_val(_list)


def _set_outblock_dict(block_name='OutBlock', field=''):
    """OutBlock 설정

    Args:
        block_name (str, optional): [description]. Defaults to 'OutBlock'.
        field (str, optional): [description]. Defaults to ''.

    Returns:
        [type]: [description]
    """

    _list = ['' for _ in range(0, 8)]  # NOTE: ['kor', 'eng', 'type', 'len', 'remark']
    for i, v in enumerate(field.split(',')):
        if '('  in v and (':'  in v or '/' in v):  # NOTE: '요청건수(최대-압축:2000비압축:500)' 등 괄호 안에 있는 내용은 remark로
            idx = v.index('(')
            _list[i] = v[:idx]
            _list[4] = v[idx+1:-1]
        else:
            _list[i] = v
    
    _list[5] = _list[1]  # nick 추가
    _list[6] = 'n'  # use 추가 (y: 사용, n: 미사용 / default: n)
    _list[7] = 'o'  # NOTE: outblock 표시

    return _set_feild_key_val(_list)


def _extract_block(block="InBlock", content=""):
    """Block 추출(InBlock, OutBlock -> fields(dict))

    Args:
        block (str, optional): [description]. Defaults to "InBlock".
        content (str, optional): [description]. Defaults to "".

    Returns:
        [type]: [description]
    """

    block_names = re.findall(f"{block}\d?", content)
    result = {}

    for block_name in block_names:
        bl = re.findall(f"{block_name}.*?begin;.*?end;", content)

        _block = ";".join(bl[0].split(';')[2:-2]) + ";"
        _block = re.sub(DEL3[0], DEL3[1], _block)[:-1] # 중복 삭제, 마지막 ';' 제거

        fields = _block.split(';')
        result[block_name] = {}

        if 'occurs' in re.findall(f"{block_name}.*?begin;", content)[0]:
            result[block_name]['occurs'] = True

        if 'InBlock' in block_name:
            for field in fields:
                (key, val) = _set_inblock_dict(block_name=block_name, field=field)
                result[block_name][key] = val
        else:
            for field in fields:
                (key, val) = _set_outblock_dict(block_name=block_name, field=field)
                result[block_name][key] = val
    
    return result


def _extract(res_code, content):
    """TR 목록 추출

    Args:
        res_code ([type]): [description]
        content ([type]): [description]

    Returns:
        [type]: [description]
    """

    if content.find('Func,') > 0:
        kind = 'TR'
        desc = re.findall("Func,.*?,", content)[0].split(',')[1]
    elif content.find('Feed,') > 0:
        kind = 'Real'
        desc = re.findall("Feed,.*?,", content)[0].split(',')[1]
    else:
        kind = ""
        desc = ""

    inblock = _extract_block(block="InBlock", content=content)
    outblock = _extract_block(block="OutBlock", content=content)
    uses = []  # NOTE: 실제 사용할 OutBlock, ['OutBlock', 'OutBlock1', ...]

    desc = desc.replace(f"({res_code})", '') if f"({res_code})" in desc else desc  # '(t1803)' 부분 제거

    return {'res_code': res_code, 'kind': kind, 'desc': desc, 'uses': uses, 'inblock': inblock, 'outblock': outblock}


def _save_res_to_db(files=[], agency='ebest'):
    """Res 파일 -> mongodb 저장
        files: 파일 이름 't0150.res', 'B7_.res'
    """

    collection=f"api_requests_spec_{agency}"
    for file in files:
        path = RES_PATH + file
        content = _replace_re(replace_dict=REPLACEMETS, string=_read_file(path=path, encoding="cp949"))
        res = _extract(file.split('.')[0], content)
        upsert_doc({'res_code': res['res_code']}, doc=res, collection=collection)

    to_collection = f'api_requests_user_{agency}'  # NOTE: 사용자용(실제 사용 block, field 표시)
    copy_collection(from_collection=collection, to_collection=to_collection)  # NOTE: collection 복사

    to_collection = f'api_requests_spec_{agency}_bk'  # NOTE: 백업용
    copy_collection(from_collection=collection, to_collection=to_collection)  # NOTE: collection 복사


##@@ Database(mongodb) -> 파일(../staff/api_ebest_for_data.py, ...) 변경
##------------------------------------------------------------
def _block_dict_from_db(res_code='', fields=['inblock', 'outblock', 'uses', 'desc'], division='spec', agency='ebest', separator='`'):
    """res_code에 해당하는 api request spec 불러오기

    Args:
        res_code (str, optional): [description]. Defaults to ''.
        fields (list, optional): [description]. Defaults to ['inblock', 'outblock', 'uses', 'desc'].
        division (str, optional): 'spec': 원본(use, uses 적용되지 않음) , user: 사용자 설정(block/field 사용여부 적용) Defaults to 'spec'.
        agency (str, optional): [description]. Defaults to 'ebest'.
        separator (str, optional): [description]. Defaults to '`'.

    Returns:
        [type]: [description]
    """

    project = {'_id': 0}
    for field in fields:
        project[field] = 1

    doc = find_doc(query={'res_code': res_code}, project=project, collection=f"api_requests_{division}_{agency}")
    return _apply_use(res_code=res_code, doc=doc, division=division, separator='`')


def _apply_use(res_code='', doc={}, division='spec', separator='`'):
    """uses(실제 사용할 OutBlock) / use(실제 사용할 field) 적용

    Args:
        res_code (str, optional): [description]. Defaults to ''.
        doc (dict, optional): [description]. Defaults to {}.
        division (str, optional): [description]. Defaults to 'spec'.
        separator (str, optional): [description]. Defaults to '`'.

    Returns:
        [type]: [description]
    """
    if 'uses' in doc:
        if division == 'user': # uses(outblock 사용여부) 적용
            doc['outblock'] = {k: doc['outblock'][k] for k in doc['uses']}
        doc.pop('uses')

    for block in ['inblock', 'outblock']:
        for key, _block in doc[block].items():
            if 'occurs' in _block:  # 'occurs'가 있으면 삭제
                # print("occurs")
                _block.pop('occurs')

            # TODO: 필요여부 확인
            # if division == 'user': # use(field별 사용 여부) 적용
            #     doc[block][key] = {k:v for k, v in _block.items() if v.split(separator)[3] == 'y'}  # NOTE: use = 'y'
            
            # TODO: value값 변환
            # _convert_field_value()

    return doc  # NOTE: {'desc': '', 'inblock': {'InBlock': {}}, 'outblock': {{}}


def _blocks_json_from_db(res_codes=['t0150', 't0424'], fields=['inblock', 'outblock', 'uses', 'desc'], division='spec', agency='ebest', separator='`'):
    """mongodb에서 불러온 데이터 -> json

    Args:
        res_codes (list, optional): [description]. Defaults to ['t0150', 't0424'].
        fields (list, optional): [description]. Defaults to ['inblock', 'outblock', 'uses', 'desc'].
        division (str, optional): [description]. Defaults to 'spec'.
        agency (str, optional): [description]. Defaults to 'ebest'.
        separator (str, optional): [description]. Defaults to '`'.

    Returns:
        [type]: [description]
    """
    blocks = {}
    for res_code in res_codes:
        blocks[res_code] = _block_dict_from_db(res_code=res_code, fields=fields, division=division, agency=agency, separator=separator)
    
    return f"blocks = " + json.dumps(blocks, indent=4, ensure_ascii=False)


##@@ 파일(../staff/api_ebest_for_data.py, ...) -> Database(mongodb) 업데이트
##------------------------------------------------------------

def _update_req_dict_val(old_val='', new_val='', separator='`'):
    """
    use: 'y' 추가
    inblock: default, remark 변경
    outblock: nick, remark 변경
    """

    new_val = ' ' + new_val.rstrip() if new_val[0] == '`' else new_val.rstrip() # inblock 디폴트 값이 ''인 경우 ' '로 수정
    news = old_val.split(separator)[:4] + ['y'] + new_val.split(separator)
    return separator.join(news)


def _user_to_spec_doc(doc={}, separator='`'):
    """
    update_requests_user의 doc을 spec용으로 변경
    ## use='n', uses=[]으로 변경
    """
    for in_out, blocks in doc.items():
        if not 'block' in in_out:  # uses 등 block 아닌 것 제외
            continue
        for block_name, _block in blocks.items():
            for k, v in _block.items():
                if 'occurs' in _block:  # TODO: 필요한지 확인후 삭제, 'occurs'가 있으면 삭제
                    _block.pop('occurs')
                for k, v in _block.items():  # NOTE: use: 'y' -> 'n'
                    # print(f"k: {k}, v: {v}")
                    _block[k] = v.replace(f"{separator}y{separator}", f"{separator}n{separator}")

    # print(f"{doc}")
    return doc


def _update_request_by_dict(res_code='', new={}, agency='ebest', separator='`'):
# def _update_requests_user(res_code='', block_name='InBlock', new={}, agency='ebest'):
    """
    new: {'inblock': {'InBlock': {'key1': 'default1.remark1', ...}}}
         {'outblock': 'OutBlock: {'key1': 'nick1.remark1', ...}, 'OutBlock1': {,..}}}
    """

    old_block = _block_dict_from_db(res_code=res_code, fields=['inblock', 'outblock'], division='spec', agency='ebest', separator='`')

    old_block['uses'] = []
    for in_out, blocks in new.items():
        for block_name, _block in blocks.items():
            for k, v in _block.items():
                old_block[in_out][block_name][k] = _update_req_dict_val(old_val=old_block[in_out][block_name][k], new_val=v)
            if in_out == 'outblock' and _block != {}:  # NOTE: block이 비어있지 않을 때
                old_block['uses'].append(block_name)

    ## DB 업데이트(user)
    upsert_doc({'res_code': res_code}, doc=old_block, collection=f"api_requests_user_{agency}")

    ## DB 업데이트(spec)
    old_block['uses'] = []
    old_block = _user_to_spec_doc(doc=old_block, separator='`')
    upsert_doc({'res_code': res_code}, doc=old_block, collection=f"api_requests_spec_{agency}")

    return old_block


def _blocks_dict_from_file(path=''):
    """
    path의 파일에서 blocks의 dict값을 반환
    """
    content = _read_file(path)  # NOTE: 편집할 파일 내용 읽어옴

    regex = "blocks *= *\{[\S\n ]*?\n\}\n"  # NOTE: blocks = {...} 부분(읽어올 dict 부분)
    o_block = re.findall(regex, content)[0]
    o_block = o_block[o_block[:20].index('{'):]  # NOTE: 'blocks = ' 제거하기 위해 첫번째 '{' 위치 찾음

    return literal_eval(_replace_re(replace_dict=REPLACEMETS_BLOCKS2, string=o_block))


##@@ request 리스트: usage(용도) / priority(중요도: 1~5) / goods(현물/선물/EUREX)
##------------------------------------------------------------

def _list_py_to_csv(path='_api_res/list_TR.py', agency='ebest'):
    content = _read_file(path)
    # "CDPCQ04700": "계좌 거래내역",  # order / 5 / 현물
    repls = {
        r'[{}].*': '',
        # r' *"([a-zA-Z_0-9]+)": *"(.+)"[, ]*#( *.*? *)/( *.*? *)/( *.+ *)': r'\1,\2,\3,\4,\5',
        r' *"([a-zA-Z_0-9]+)": *"(.+)"[, ]*#(.*?)/(.*?)/(.+)': r'\1\t\2\t \t\3\t\4\t\5\t ',
        r'\n$': '',
        r'^\n': '',
        r' *\t *': r'\t',
        # r', +': ',',
        # r' +,': ',',
    }

    for key, val in repls.items():
        content = re.sub(key, val.strip(), content)
    
    _write_file(f"{path.split('.')[0]}.csv", content)

    # return content


##@@ 실행 함수
##============================================================

##@@ 단위 실행 함수
##------------------------------------------------------------

def save_all_res_to_db(folder="C:/eBEST/xingAPI/Res/", agency='ebest'):
    """
    NOTE: Res 파일 -> Database(mongodb) 저장
    folder: Res 파일이 있는 디렉토리
    """
    files = _files_in_folder(folder=folder, filter_fn=lambda x: x.find("_1") < 1 and x.find("_2") < 1)
    _save_res_to_db(files=files, agency=agency)


def find_reqs_by_query(query={}, fields=['res_code'], agency='ebest'):
    """
    query에 맞는 req 목록: fields=
    query: ex) {'kind': 'TR', 'goods': '현물', 'usage': 'order', 'priority': {'$gt' : 3}}
    """
    project = {'_id': 0, 'res_code': 1}

    for field in fields:
        project[field] = 1

    r = find_docs(query=query, project=project, collection=f"api_requests_user_{agency}")
    if len(fields) < 2:
       return  [d['res_code'] for d in r]  # res_code 배열 반환
      
    return r 


def find_fields_eng_kor(agency='ebest'):
    """
    field 이름 일관성을 위해 전체 'eng`kor' 출력
    """
    blocks = ['inblock', 'outblock']
    sets = set()
    for block in blocks:
        r = find_docs(query={}, project={'_id': 0, block: 1}, collection=f"api_requests_spec_{agency}")
        for _block in r:
            for k, b in _block[block].items():
                if k == 'uses' or k == 'occurs':
                    continue
                sets.update(set([k + '`' + v.split('`')[1] for k, v in zip(b.keys(), b.values()) if k != 'occurs']))
    
    print(len(sets))
    return sets


def count_eng_kor(agency='ebest'):
    """
    eng/kor 키 개수
    """
    eng_kors = find_fields_eng_kor(agency=agency)
    engs = set()
    kors = set()
    for eng_kor in eng_kors:
        engs.add(eng_kor.split('`')[0])
        kors.add(eng_kor.split('`')[1])
    
    print((len(engs), len(kors)))


def list_req_to_file(kind='TR', agency='ebest'):
    """
    requests 리스트
    kind: 'TR' / 'Real'
    {'res_code1': 'desc1', 'res_code2': 'desc2', ...}
    """
    reqs = find_docs(query={'kind': kind}, project={'_id':0, 'res_code': 1, 'desc': 1}, collection=f"api_requests_user_{agency}")
    reqs = {req['res_code']: req['desc'] for req in reqs}
    
    _write_file('res_list_' + kind + '.py', json.dumps(reqs, indent=4, ensure_ascii=False))
    return reqs
    # print({req['res_code']: req['desc'] for req in reqs})


def insert_blocks_file_by_db(path='', res_codes=[], fields=['inblock', 'outblock', 'uses', 'desc'], division='spec', agency='ebest', separator='`'):
    """
    Database(mongodb) -> 파일(../staff/api_ebest_for_data.py, ...) 변경
    """
    content = _read_file(path)

    o_block = re.findall("blocks *= *\{[\S\n ]*?\n\}\n", content)[0]
    r_block = _blocks_json_from_db(res_codes=res_codes, fields=fields, division=division, agency=agency, separator=separator) + "\n"
    r_block = _replace_re(replace_dict=REPLACEMETS_BLOCKS, string=r_block)
    
    # print(r_block)
    content = content.replace(o_block, r_block)  # TODO: "\n" 필요한지 확인 필요

    _write_file(path, content)


def insert_blocks_file_by_query(path='', query={}, use=False, agency='ebest'):
    """
    Database(mongodb) -> 파일(../staff/api_ebest_for_data.py, ...) 변경
    use: False(실제 사용하지 않는 block, field도 출력), True(실제 사용하는 block, field만 출력)
    query: {'kind': 'TR', 'goods': '현물', 'usage': 'order', 'priority': {'$gt' : 3}}
    """
    res_codes = find_reqs_by_query(query=query, fields=['res_code'], agency='ebest')  # NOTE: api_requests_user_{agency} 에서 검색
    division = 'user' if use else 'spec'

    insert_blocks_file_by_db(path=path, res_codes=res_codes, division=division)


def update_db_by_file(path='', agency='ebest', separator='`'):
    """
    파일(../staff/api_ebest_for_data.py, ...) -> Database(mongodb) 업데이트
    """

    content = _read_file(path)  # NOTE: 편집할 파일 내용 읽어옴

    regex = "blocks *= *\{[\S\n ]*?\n\}\n"  # NOTE: blocks = {...} 부분(읽어올 dict 부분)
    o_block = re.findall(regex, content)[0]
    o_block = o_block[o_block[:20].index('{'):]  # NOTE: 'blocks = ' 제거하기 위해 첫번째 '{' 위치 찾음

    for res_code, block in _blocks_dict_from_file(path=path).items():
        _update_request_by_dict(res_code=res_code, new=block, agency=agency, separator=separator)


def update_db_usage_by_file(path='_api_res/list_TR.py', agency='ebest'):
    """
    path의 파일 -> usage(용도) / priority(중요도: 1~5) / goods(현물/선물/EUREX/...) 업데이트
    """
    content = _read_file(path)
    lines = re.findall(r'"([a-zA-Z_0-9]+)": *".*?", *# *(.*?)/(.*?)/(.+)', content)
    keys = ['res_code', 'usage', 'priority', 'goods']
    docs = []
    for vals in lines:
        docs.append({key: int(val.strip()) if len(val.strip()) == 1 else val.strip() for key, val in zip(keys, vals)})
    
    upsert_docs(keys=['res_code'], docs=docs, collection=f"api_requests_user_{agency}")

##@@ 초기화/업데이트
##------------------------------------------------------------

def write_requests_py(agency='ebest'):
    """
    기존 db 컬렉션 삭제
    usage/priority/goods 업데이트
    write .py files
    """
    # drop collections
    drop_collection(collection=f"api_requests_spec_{agency}")
    drop_collection(collection=f"api_requests_user_{agency}")
    time.sleep(0.1)

    # # create collections
    save_all_res_to_db()
    time.sleep(0.1)

    # udate db(usage/priority/goods)
    update_db_usage_by_file(path="_api_res/list_TR.py")
    update_db_usage_by_file(path="_api_res/list_Real.py")
    time.sleep(0.1)

    # write .py files
    query={'kind': 'TR', 'goods': '현물', 'usage': 'order', 'priority': {'$gt' : 3}}
    insert_blocks_file_by_query(path='../staff/api_ebest_for_order.py', query=query, use=False, agency='ebest')

    query={'kind': 'TR', 'goods': '현물', 'usage': 'data', 'priority': {'$gt' : 4}}
    insert_blocks_file_by_query(path='../staff/api_ebest_for_data.py', query=query, use=False, agency='ebest')

    query={'kind': 'Real', 'goods': '현물', 'priority': {'$gt' : 3}}
    insert_blocks_file_by_query(path='../staff/api_ebest_for_real.py', query=query, use=False, agency='ebest')


def write_requests_all():
    """
    주식에 관련된 requests 모두 저장
    """
    query={'kind': 'TR', 'goods': '현물'}
    insert_blocks_file_by_query(path='_api_res/blocks_order_all.py', query=query, use=False, agency='ebest')

    query={'kind': 'TR', 'goods': '현물'}
    insert_blocks_file_by_query(path='_api_res/blocks_data_all.py', query=query, use=False, agency='ebest')

    query={'kind': 'Real', 'goods': '현물'}
    insert_blocks_file_by_query(path='_api_res/blocks_real_all.py', query=query, use=False, agency='ebest')


def replace_file_blocks(paths=['../staff/api_ebest_for_data.py', '../staff/api_ebest_for_order.py']):
    """
    .py 내의 inblock, outblock 내용 수정
    """
    for path in paths:
        content = _read_file(path)
        content = _replace_re(REPLACEMETS_INBLOCKS3, content)
        _write_file(path, content)


def update_by_py():
    """
    db 업데이트
    """
    update_db_by_file(path='../staff/api_ebest_for_order.py', agency='ebest', separator='`')
    update_db_by_file(path='../staff/api_ebest_for_data.py', agency='ebest', separator='`')


def update_to_py(agency='ebest'):
    """
    파일 업데이트
    """
    # write .py files
    query={'kind': 'TR', 'goods': '현물', 'usage': 'order', 'priority': {'$gt' : 3}}
    insert_blocks_file_by_query(path='../staff/api_ebest_for_order.py', query=query, use=True, agency=agency)

    query={'kind': 'TR', 'goods': '현물', 'usage': 'data', 'priority': {'$gt' : 4}}
    insert_blocks_file_by_query(path='../staff/api_ebest_for_data.py', query=query, use=True, agency=agency)


if __name__ == "__main__":
    pass
    ## NOTE: 테스트
    save_all_res_to_db()

    # xlsx_path = '../sats/_setting/_api_res/api_requests_ebest.xlsx'
    xlsx_path = '_api_res/api_requests_ebest.xlsx'
    title = 'ebest_TR'

    fields = ['res_code', 'usage', 'priority', 'goods', 'remark']
    docs = read_xsheet(path=xlsx_path, title=title, header=0, first=(0, 0), fields=fields, out_type='dicts')
    print(docs)

    # upsert_docs(keys=['res_code'], docs=docs, collection='api_requests_user_ebest')

    # list_req_to_file(kind='TR', agency='ebest')
    # _update_requests_user(res_code='t0424', new=new, agency='ebest', separator='`')
    # r = _blocks_dict_from_file(path='../staff/api_ebest_for_order.py')
    # print(r)


    # write_requests_py()

    # blocks_dict_from_file(path='../staff/test_data.py')

    # update_db_by_file(path='../staff/api_ebest_for_data.py', agency='ebest', separator='`')

    # update_by_py()

    # update_to_py()

    ## NOTE: TEST
    # replace_file_blocks(paths=['../staff/api_ebest_for_data.py', '../staff/api_ebest_for_order.py'])

    # db.api_requests_spec_ebest.find({'res_code': 'CSPAQ12200'})
    # insert_blocks_file_by_db(path='../staff/api_ebest_test.py', res_codes=['CSPAQ12200', 'CSPAQ12300', 'CSPAQ13700'], division='spec')


    # update_db_usage_by_file(path="_api_res/list_Real.py")
    # time.sleep(0.1)

    # write .py files
    # query={'kind': 'Real', 'goods': '현물'}
    # insert_blocks_file_by_query(path='_api_res/blocks_real_all.py', query=query, use=False, agency='ebest')

    # write_requests_all()

    # _list_py_to_csv(path='_api_res/list_Real.py', agency='ebest')