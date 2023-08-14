from preprocessing import *
import csv

## csv파일 열기
with open("verified_online.csv", 'r', newline = '') as c:
    ## 각 판별값을 배열에 임시 저장하기 위한 설정
    m = [0, 0, 0, 0, 0, 0]
    cr = csv.reader(c)
    ## 헤더 부분 처리
    next(cr)

    ## 읽어 온 값의 URL 부분으로 각 값 판별 후 임시 저장
    for r in cr:
        turl = get_origin_url(r[1])
        if turl == None:
            continue
        m[0] = len_dec(turl)
        m[1] = at_sym_dec(turl)
        m[2] = red_dec(turl)
        m[3] = dash_dec(turl)
        m[4] = subdo_dec(turl)
        m[5] = non_std_port(turl)

        ## 결과값 확인을 위한 임시 출력
        print(f"{turl}\n{r[1]}\n{m}\n\n")

        ## 저장을 위한 txt 파일 열어서 추가
        with open("verified_online.txt", 'a') as txt:
            txt.write(f"{r[1]}, {m}\n")
        ## 각종 문제 상황 예외 처리 부분
