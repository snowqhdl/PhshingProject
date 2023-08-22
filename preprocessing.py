from tld import get_tld
from urllib import parse
from typing import Optional
from bs4 import BeautifulSoup
from selenium import webdriver
import numpy as np
import re
import csv
import ssl
import whois
import socket
import psutil
import requests
import datetime
import subprocess

## URL이 가르키는 URL 반환하는 함수
## 단축된 URL일 경우 원URL, 일반 URL일 경우 자신 반환
def get_origin_url(url: str):
    parsed_url = requests.utils.urlparse(url)
    host = parsed_url.netloc.split(':')[0]
    try:
        socket.gethostbyname(host)
        return requests.head(url, allow_redirects=True, timeout=15).url
    except (socket.gaierror, requests.exceptions.RequestException, requests.exceptions.Timeout):
        return None

## 1.1. ip주소 여부를 통한 판단 기준
## 정상 : 1 / 피싱 : -1

def ip_dec(url: str) -> int:
    netloc = parse.urlparse(url).netloc
    ip_pattern = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')

    if ip_pattern.match(netloc):
        return -1
    else:
        return 1

## 1.2. 길이를 통한 판단
## 정상 : 1 / 의심 : 0 / 피싱 : -1
def len_dec(url: str):
    if len(url) < 54:
        return 1
    elif len(url) < 75:
        return 0
    else:
        return -1

## 1.3. http redirection 여부를 통한 판단 기준
## 정상 : 1 / 피싱 : -1
def tiny_dec(response: requests.Response):
    ## redirection 탐지
    for res in response.history:
        if res.status_code == 301 and res.status_code == 302:
            return -1
    else:
        return 1

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

'''
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
def domain_duration_dec(w: whois.WhoisEntry):
    try:
        ## 도메인 유효 기간 계산에 필요한 값
        expiration_date = w.expiration_date
        creation_date = w.creation_date

        ## 둘 이상의 값이 존재할 경우에 대한 처리
        if isinstance(expiration_date, list):
            expiration_date = expiration_date[-1]
        if isinstance(creation_date, list):
            creation_date = creation_date[0]

        ## 유효 기간이 1년(365일) 미만이면 피싱 사이트로 판별
        if (expiration_date - creation_date).days < 365:
            return -1
        else:
            return 1
    except:
        # 예외 발생 시 (예: 도메인 정보를 찾을 수 없는 경우) 의심 사이트로 판별
        return 0

## 1.10. favicon을 통한 판단 기준
def favicon_dec(url: str, soup: Optional[BeautifulSoup] = None, options: Optional[webdriver.ChromeOptions] = None) -> int:
    favicon_url = None

    try:
        ## BeautifulSoup 사용가능시
        if soup:
            favicon_link = soup.find('link', rel=lambda x: x and 'icon' in x)
            
            if favicon_link and 'href' in favicon_link.attrs:
                favicon_url = favicon_link['href']

        ## BeautifulSoup 사용 불가, Selenium 사용 가능시
        elif options:
            with webdriver.Chrome(options=options) as driver:
                driver.get(url)
                favicon_link_element = driver.find_element_by_xpath("//link[contains(@rel, 'icon')]")
                
                if favicon_link_element:
                    favicon_url = favicon_link_element.get_attribute('href')
        ## 모두 사용 불가시 판단 불가
        else:
            return 0

        ## favicon_url의 존재 여부 및 URL과 도메인 일치 판단
        if favicon_url:
            if favicon_url.startswith('http') or favicon_url.startswith('//'):
                favicon_domain = urlparse(favicon_url).netloc
                original_domain = urlparse(url).netloc

                ## favicon 도메인과 원본 도메인이 다르면 피싱 사이트로 판단
                if favicon_domain != original_domain:
                    return -1
            return 1
        ## favicon이 존재하면서 그 도메인이 존재하지 않는 경우 판단 불가
        else:
            return 0

    except Exception as e:
        print("An error occurred:", str(e))
        return 0  # 에러 발생 시 0 반환

## 1.11. 비표준 포트 사용 여부를 통한 판단 기준
##       HTTPS 표준 포트 연결 가능 여부 판단
##       HTTPS 표준 포트 연결 불가일 경우 예비 포트로 진입
## 정상 : 1 / 의심 : 0 / 피싱 : -1
def port_dec(url: str):
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

## 2.1. 사이트 내 외부 URL 비율을 통한 판단 기준
def url_ratio_dec(url: str, soup: Optional[BeautifulSoup] = None, options: Optional[webdriver.ChromeOptions] = None) -> int:
    try:
        ## bs4 사용 결과물을 받은 경우
        if soup
            pass
        ## bs4 사용이 불가능해서 selenium을 통해 소스코드를 받아와서 파싱
        elif options:
            driver = webdriver.Chrome(executable_path="chromedriver.exe", chrome_options=options)
            driver.get(url)
            page_source = driver.page_source
            driver.quit()
            soup = BeautifulSoup(page_source, "html.parser")
        ## 두 방법 모두 사용 불가능해서 판단이 불가능한 경우
        else:
            return 0

        base_domain = urlparse(url).netloc
        external_objects_count = 0
        total_objects_count = 0

        for tag in soup.find_all(['img', 'video', 'audio']):
            src = tag.get('src')
            if src:
                total_objects_count += 1
                if base_domain not in urljoin(url, src):
                    external_objects_count += 1
        ## 내부에 태그가 존재하지 않는 경우 판단 불가
        if total_objects_count == 0:
            return 0
        
        ratio = (external_objects_count / total_objects_count) * 100

        if ratio < 22:
            return 1
        elif ratio < 61:
            return 0
        else:
            return -1

    except Exception as e:
        print(f"Error: {e}")
        return 0


## 2.6.1. 웹사이트에서 mailto 허용 여부를 통한 판단 기준
def mailto_dec(response: requests.Response):
    try:
        ## mailto: 링크가 포함되어 있는지 확인
        if 'mailto:' in response.text:
            return 0
        else:
            return 1
    ## 요청에서 오류 발생
    except AttributeError as e:
        return -1

## 2.6.2. 웹사이트에서 mail 사용 여부를 통한 판단 기준
def mail_dec(response: requests.Response):
    try:
        if "mail(" in response.text:
            return -1  # mail() 사용
        else:
            return 1  # mail() 사용하지 않음

    except AttributeError as e:
        return 0

## 3.1. 웹사이트 포워딩을 통한 판단 기준
##      redirection 횟수를 기준으로 1번 이하이면 안전, 4번 이상이면 피싱
##      2번 이상 4번 미만일 경우 의심 사이트
def redir_dec(response: requests.Response):
    try:
        if len(response.history) < 2:
            return 1
        elif len(response.history) < 4:
            return 0
        else:
            return -1
    except AttributeError as e:
        return 0

## 3.3. 오른쪽 클릭 비활성화를 통한 판단 기준
def right_dec(url: str, soup: Optional[BeautifulSoup] = None, options: Optional[webdriver.ChromeOptions] = None):
    try:
        ## BeautifulSoup 사용
        if soup:
            if soup.find(lambda tag: tag.name.lower() in ["body", "html"] and 
                          tag.has_attr("oncontextmenu") and 
                          "return false" in tag.attrs["oncontextmenu"].lower()):
                return -1

            for script in soup.find_all("script"):
                if script.string and "event.button == 2" in script.string:
                    return -1
            return 1

        ## Selenium 사용
        elif options:
            with webdriver.Chrome(executable_path="chromedriver.exe", options=options) as driver:
                driver.get(url)  # Missing line: Visit the URL using the driver
                
                body_elements = driver.find_elements_by_xpath("//body[@oncontextmenu='return false']") + \
                                driver.find_elements_by_xpath("//html[@oncontextmenu='return false']")
                
                if body_elements:
                    return -1

                for script in driver.find_elements_by_tag_name("script"):
                    if "event.button == 2" in (script.get_attribute('innerHTML') or ''):
                        return -1

                return 1
        ## 둘 다 사용 불가한 경우 판단 불가
        else:
            return 0

    except Exception as e:
        print(f"Error in right_dec: {e}")
        return 0


    ## soup와 options 둘 다 None이라면 의심
    else:
        return 0

## 4.1. 도메인 수명을 통한 판단 기준
##      피싱사이트 수명이 짧은 것을 이용
def age_dec(w: whois.WhoisEntry):
    ## whois 사용 불가 사이트
    creation_date = w.creation_date
    if creation_date:
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
            
        current_date = datetime.datetime.now()
        domain_age = (current_date - creation_date).days

        ## 한 달을 30일로 해서 6개월 미만인지 판단
        if domain_age < 6 * 30:
            return -1
        else:
            return 1
    else:
        return 0

class URLFeature:
    def __init__(self, url: str):
        self.url = url
        self.origin = get_origin_url(url)
        if self.origin:
            self.response = requests.get(url)
            try:
                self.w = whois.whois(self.origin)
            except:
                self.w = None
                
            try:
                self.soup = BeautifulSoup(self.response.content, "html.parser")
            except:
                self.soup = None
                
            try:
                self.options = webdriver.ChromeOptions()
            except:
                self.options = None
            
            self.__data = [ip_dec(self.url),
                           len_dec(self.url),
                           tiny_dec(self.response),
                           at_sym_dec(self.url),
                           red_dec(self.url),
                           dash_dec(self.url),
                           subdo_dec(self.url),
                           domain_duration_dec(self.w),
                           favicon_dec(self.origin, self.soup, self.options)
                           port_dec(self.origin),
                           reque_dec(self.origin, self.soup, self.options),
                           mailto_dec(self.response),
                           mail_dec(self.response),
                           redir_dec(self.response),
                           right_dec(self.origin, self.soup, self.options),
                           age_dec(self.w)]
        else:
            self.__data = None

    @property
    def data(self):
        return self.__data

    def __getitem__(self, index):
        if self.__data:
            return self.__data[index]
        else:
            return None

    def __len__(self):
        if self.__data:
            return len(self.__data)
        else:
            return 0
        
    def __repr__(self):
        return repr(self.__data)
    

features_list = []

with open("verified_online.csv", 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        feature = URLFeature(row[1])

        if feature and feature.data:
            features_list.append(feature.data)

# 리스트를 numpy 배열로 변환
features_array = np.array(features_list)
    
# npy 파일로 저장
np.save("output_features.npy", features_array)



    
