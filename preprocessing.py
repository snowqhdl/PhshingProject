from urllib import parse
from tld import get_tld
import requests
import ssl
import socket
import datetime
import psutil
import subprocess

## URL이 가르키는 URL 반환하는 함수
## 단축된 URL일 경우 원URL, 일반 URL일 경우 자신 반환
def get_origin_url(url: str):
    parsed_url = requests.utils.urlparse(url)
    host = parsed_url.netloc.split(':')[0]
    try:
          socket.gethostbyname(host)
          return requests.head(url, allow_redirects=True).url
    except (socket.gaierror, requests.exceptions.RequestException):
          return None

'''
## 1.1. ip주소 여부를 통한 판단 기준
## 정상 : 1 / 피싱 : -1
def ip_dec(url: str):
    netloc_arr = parse.urlparse(url).netloc.split('.')
    try:
        int(netloc_arr[-1], 0)
        return -1
    except ValueError:
        return 1
'''

## 1.2. 길이를 통한 판단
## 정상 : 1 / 의심 : 0 / 피싱 : -1
def len_dec(url: str):
    if len(url) < 54:
        return 1
    elif len(url) < 75:
        return 0
    else:
        return -1

'''
## 1.3. http redirection 여부를 통한 판단 기준
##      URL이 가리키는 최종 주소를 이용해서 판단하기 때문에 불필요
## 정상 : 1 / 피싱 : -1
def tiny_dec(url: str):
    response = requests.get(url)
    ## redirection 탐지
    for res in response.history:
        if res.status_code == 301 and res.status_code == 302:
            return -1
    else:
        return 1
'''

## 1.4. @ 존재 여부를 통한 판단 기준
## 정상 : 1 / 피싱 : -1
def at_sym_dec(url: str):
    if "@" in url:
        return -1
    else:
        return 1

## 1.5. //의 존재 여부를 통한 판단 기준
## 정상 : 1 / 피싱 : -1
def red_dec(url: str):
    if "//" in (url[7:] if url[:7] == "http://" else url[8:]):
        return -1
    else:
        return 1

## 1.6. -의 존재 여부를 통한 판단 기준
## 정상 : 1 / 피싱 : -1
def dash_dec(url: str):
    if '-' in url:
        return -1
    else:
        return 1

## 1.7. 하위, 다중 하위 도메인 여부를 통한 판단 기준
## 정상 : 1 / 의심 : 0 / 피싱 : -1
def subdo_dec(url: str):
    netloc_arr = parse.urlparse(url).netloc.split('.')
    ## domain 부분에 ip 형식이 들어있을 경우
    ##get_tld가 TLD name과 일치하는 형식이 존재하지 않아 생기는 오류 방지
    try:
        int(netloc_arr[-1], 0)
        return -1
    except ValueError:
        subdomain = get_tld(url.replace("www.", "") if "www." in url[:12] else url, as_object = True).subdomain
        if subdomain == '':
            return 1
        else:
            dot = subdomain.count('.')
            if dot == 0:
                return 0
            else:
                return -1

## 1.8.1. SSL final state를 통한 판단 기준
##        URL의 hostname을 통해 인증서 작성 기관을 보고 신뢰성 판별
## 정상 : 1 / 의심 : 0 / 피싱 : -1
def ssl_fs_dec(url: str):
    try:
        ## URL로 부터 SSL 받아오기
        x509_cert = crypto.load_certificate(crypto.FILETYPE_PEM, cert_pem)
        cert = x509_cert.get_issuer().CN
        
        ## installed_cas.txt에서 신뢰 가능한 인증서 발급처 목록 읽어오기
        ## 매 순간 인증서 발급처 목록 갱신하는 get_installed_cas() 실행 예정
        with open("installed_cas.txt", "r") as file:
            installed_cas = {line.strip() for line in file.readlines()}
        
        issuer_common_name = get_cert_issuer_common_name(cert)

        ## 신뢰 가능한 인증서 사용
        if issuer_common_name in installed_cas:
            return 1
        ## 의심스러운 인증서 사용
        else:
            return 0

    ## 믿을 수 없거나 그 외의 에러를 발생시키는 경우
    except ssl.CertificateError as e:
        return -1
    except Exception as e:
        return -1
'''    
## 1.9. 도메인 유효 기간을 통한 판단 기준
def is_phishing_site(url):
    try:
        # URL에서 도메인 이름 추출
        domain_name = urlparse(url).netloc
        # 도메인의 WHOIS 정보 조회
        domain_info = whois.whois(domain_name)

        # 도메인 유효 기간 계산
        expiration_date = domain_info.expiration_date
        creation_date = domain_info.creation_date

        # 만약 여러 날짜가 반환되면 첫 번째 날짜를 선택
        if isinstance(expiration_date, list):
            expiration_date = expiration_date[-1]
        if isinstance(creation_date, list):
            creation_date = creation_date[0]

        # 유효 기간이 365일 미만이면 피싱 사이트로 판별
        if (expiration_date - creation_date).days < 365:
            return -1
        else:
            return 1
    except:
        # 예외 발생 시 (예: 도메인 정보를 찾을 수 없는 경우) 정상 사이트로 판별
        return 1
'''
'''
## 1.10. favicon을 통한 판단 기준
def check_favicon(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # favicon을 가리키는 link 태그 찾기
        favicon_link = soup.find('link', rel=lambda x: x and 'icon' in x)

        # link 태그가 없거나 href 속성이 없는 경우 정상 사이트로 판단
        if favicon_link is None or 'href' not in favicon_link.attrs:
            return 1
        
        favicon_url = favicon_link['href']
        
        # favicon URL이 절대 경로인지 확인
        if favicon_url.startswith('http') or favicon_url.startswith('//'):
            favicon_domain = urlparse(favicon_url).netloc
            original_domain = urlparse(url).netloc

            # favicon 도메인과 원본 도메인이 다른 경우 피싱 사이트로 판단
            if favicon_domain != original_domain:
                return -1

        return 1

    except Exception as e:
        print("An error occurred:", str(e))
        return 0  # 에러 발생 시 0 반환

'''

## 1.11. 비표준 포트 사용
##       HTTPS 표준 포트 연결 가능 여부 판단
##       HTTPS 표준 포트 연결 불가일 경우 예비 포트로 진입
## 정상 : 1 / 의심 : 0 / 피싱 : -1
def non_std_port(url: str):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # 타임아웃 설정
        sock.connect((url, 443))
        sock.close()
        return 1
    except (socket.timeout, ConnectionRefusedError, socket.gaierror):
        try:
              sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
              sock.settimeout(1)  # 타임아웃 설정
              sock.connect((url, 8443))
              sock.close()
              return 0
        except (socket.timeout, ConnectionRefusedError, socket.gaierror):
              return -1



