# 政府戶政及家事法庭查詢作業ＡＰＩ
有鑒於政府尚未開放國民身分證領補換資料查詢作業，戶口名簿請領紀錄查詢，家事事件公告查詢之ＡＰＩ，所以分析了那些網站並用Flask架設API。
以下為原始網站：
[國民身分證領補換資料查詢作業](https://www.ris.gov.tw/apply-idCard/app/idcard/IDCardReissue/)
[戶口名簿請領紀錄查詢](https://www.ris.gov.tw/apply-registration/app/aw0720/main)
[家事事件公告查詢](http://domestic.judicial.gov.tw/abbs/wkw/WHD9HN01.jsp)

## Python version

```
3.6.7
```

## Installation

```
pip install -r requirements.txt
```

## Getting started

### develop

```
python manage.py runserver
```

### uwsgi
```
uwsgi --ini urus_uwsgi.ini
```

### Test

```
pytest --disable-warnings

```