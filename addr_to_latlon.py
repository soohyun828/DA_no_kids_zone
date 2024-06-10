import pandas as pd
import requests
import json
import os

def getLatLng(addr):
    url = 'https://dapi.kakao.com/v2/local/search/address.json?query=' + addr
    headers = {
        "Authorization": "KakaoAK 794e600cd25dbe707dccdf154dde8021"}
    # get 방식으로 주소를 포함한 링크를 헤더와 넘기면 result에 json형식의 주소와 위도경도가 출력된다.
    result = json.loads(str(requests.get(url, headers=headers).text))
    # status_code = requests.get(url, headers=headers).status_code
    # if(status_code != 200):
    #     print(
    #         f"ERROR: Unable to call rest api, http_status_coe: {status_code}")
    #     return 0

    try:
        match_first = result['documents'][0]['address']
        lon = match_first['x']
        lat = match_first['y']

        return float(lat), float(lon)
    except IndexError:  # match값이 없을때
        return 0, 0
    except TypeError:  # match값이 2개이상일때
        return 2, 2

def processing_csv(file_path):
    
    df = pd.read_csv(file_path, encoding='utf-8-sig')

    latitudes = []
    longitudes = []

    for address in df['Address']: 
        lat, lon = getLatLng(address)
        latitudes.append(lat)
        longitudes.append(lon)

    df['latitude'] = latitudes
    df['longitude'] = longitudes

    df.to_csv(file_path, index=False, encoding='utf-8-sig')
    print(f'{file_path} complete processing.')

def main():
    for file_path in ['nokidsZone.csv','Elementary_school.csv','kindergarten.csv']:
        processing_csv(file_path)


if __name__ == '__main__':
    main()