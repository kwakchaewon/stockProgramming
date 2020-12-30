import cx_Oracle
# import os
# os.chdir('D:\instantclient-basic-windows.x64-19.9.0.0.0dbru\instantclient_19_9')
# os.putenv('NLS_LANG','AMERICAN_AMERICAN.UTF8')


#조회
def select():
    #db= cx_Oracle.connect("user","password","localhost:port/sid")
    db = cx_Oracle.connect("ksh03003", "1234", "localhost:1521/orcl")

    #cursor 객체 가져오기
    cursor = db.cursor()

    #oracle DB의 테이블 검색(SELECT)
    #SQL문장 실행

    sql="SELECT * FROM MY_STOCK"
    cursor.execute(sql)

    print("오라클 연결완료")
    print(cursor.fetchone())
    cursor.close()
    db.close()


def select2():

    print("됐어1")
    db=cx_Oracle.connect('ksh03003','1234','localhost:1521/orcl')

    print('{}'.format(db.version))

    sql="select * from MY_STOCK"
    cursor=db.cursor()
    cursor.execute(sql)
    cursor.execute("select count(*) from MY_STOCK")

    for row in cursor:
        print(row)

    cursor.close()
    db.close()

