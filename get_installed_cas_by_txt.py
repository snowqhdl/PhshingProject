from cryptography import x509
from cryptography.hazmat.backends import default_backend
import subprocess
import os

## 윈도우에서 신뢰 가능한 CA 목록 받아 저장하는 함수
## 상시 실행 예정(크롤링 부분)
## txt 파일은 공유 부분에 할당 해야함
def get_installed_cas():
    CERT_FILE_PATH = "path_to_certificate.pem"
    OUTPUT_FILE_PATH = "installed_cas.txt"

    try:
        # 인증서 파일을 열고 데이터를 읽음
        with open(CERT_FILE_PATH, "rb") as cert_file:
            cert_data = cert_file.read()

            # 인증서 데이터 파싱
            cert = x509.load_pem_x509_certificate(cert_data, default_backend())

            # 발급자 정보에서 CN 정보를 찾음
            common_name = next(attr.value for attr in cert.issuer if attr.oid == x509.NameOID.COMMON_NAME)

            # 결과를 파일에 저장
            with open(OUTPUT_FILE_PATH, "w") as output_file:
                output_file.write(common_name)

    except FileNotFoundError:
        print(f"Error: Certificate file {CERT_FILE_PATH} not found.")
    except ValueError as e:
        print(f"Error parsing certificate: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


'''
## 리눅스에서 신뢰 가능한 CA 목록 받아 저장하는 함수
## 상시 실행 예정(크롤링 부분)
## txt 파일은 공유 부분에 할당
def get_installed_cas():
    try:
        # /etc/ssl/certs 내의 인증서 파일들을 나열
        certs_directory = "/etc/ssl/certs"
        cert_files = [os.path.join(certs_directory, f) for f in os.listdir(certs_directory) if os.path.isfile(os.path.join(certs_directory, f))]

        new_installed_cas = set()

        for cert_file in cert_files:
            # 인증서 파일에서 발급자 정보 추출
            process = subprocess.Popen(["openssl", "x509", "-in", cert_file, "-noout", "-issuer"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()
            
            if "issuer=" in stdout:
                issuer = stdout.split("CN=")[-1].strip()
                new_installed_cas.add(issuer)

        if os.path.exists("installed_cas.txt"):
            with open("installed_cas.txt", "r") as file:
                installed_cas = {line.strip() for line in file.readlines()}
        else:
            installed_cas = set()

        if new_installed_cas != installed_cas:
            with open("installed_cas.txt", "w") as file:
                file.write('\n'.join(new_installed_cas))

    except Exception as e:
        # 예외 발생 시 로그나 출력으로 오류 내용을 보여주는 것이 좋습니다.
        print(f"Error: {e}")


'''

get_installed_cas()
