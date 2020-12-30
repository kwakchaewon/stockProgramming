import cx_Oracle
# import os
# os.chdir('D:\instantclient-basic-windows.x64-19.9.0.0.0dbru\instantclient_19_9')
# os.putenv('NLS_LANG','AMERICAN_AMERICAN.UTF8')

####
#
# cx_Oracle 라이브러리를 사용하여 오라클 - 장고 연동
#
####


# 파이썬에서 오라클과 DB연동을 할때 cx_Oracle 라이브러리는 SELECT 해오는 쿼리 결과가 tuple형태이다.
# rowfactory 라는 메소드를 오버라디잉하여 리턴받는 데이터의 형태를 바꿀 수 있다.
# cx_Oracle 로 가져온 데이터를 딕셔너리 형태로 반환
def makeDictFactory(cursor):
    columNames = [d[0] for d in cursor.description]

    def createRow(*args):
        return dict(zip(columNames, args))

    return createRow



## select STOCK_NAME from MY_STOCK
def bringmyStocks():
    MY_STOCKS = []

    db = cx_Oracle.connect('ksh03003', '1234', 'localhost:1521/orcl')

    print('{}'.format(db.version))

    cursor = db.cursor()
    cursor.execute("select stock_name from my_stock order by stock_name asc")
    cursor.rowfactory=makeDictFactory(cursor)
    rows = cursor.fetchall()

    for row in rows:
        MY_STOCKS.append(row["STOCK_NAME"])

    cursor.close()
    db.close()
    print(MY_STOCKS)
    return MY_STOCKS


## select COUNT(*) from my_stock where stock_name ='symbol';
def isThere(symbol):
    myBuffer = []

    db = cx_Oracle.connect('ksh03003', '1234', 'localhost:1521/orcl')

    print('{}'.format(db.version))

    cursor = db.cursor()
    
    
    # 문자열안에 따옴표 포함시키고싶을때 "\'": 백슬래쉬 따옴표
    cursor.execute("select COUNT(*) from my_stock where stock_name =" + '\'' + symbol + '\'')
    cursor.rowfactory = makeDictFactory(cursor)
    rows = cursor.fetchall()

    for row in rows:
        myBuffer.append(row["COUNT(*)"])

    cursor.close()
    db.close()
    return myBuffer



