
import mysql.connector

class DatabaseManager:
    def __init__(self, host="localhost", user="root", password="", database="feedingfrenzy"):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor()

    def SelectAll(self):
        sql="Select * From lichsudau Order By score DESC "
        self.cursor.execute(sql)
        resutl=self.cursor.fetchall()
        return resutl
    def Insert(self,data):
        sql="Insert into lichsudau(name, level,score,time) Values (%s, %s, %s, %s)"
        self.cursor.execute(sql,data)
        self.connection.commit()
        print("Thên vào đc")
    def SelectTopScore(self):
        sql="Select MAX(score) From lichsudau"
        self.cursor.execute(sql)
        resutl=self.cursor.fetchone() # fetchone này là lấy 1 giá trị duy nhất
        return resutl[0]
    def close(self):
        self.cursor.close()
        self.connection.close()


# test=DatabaseManager()
# test.Insert(("Player",12,255,"11:33"))
# data=test.SelectAll()

# for x in data:
#     print(f"Name: {x[0]} | Level: {x[1]} | Score: {x[2]} | Time: {x[3]}")


# if connection.is_connected():
#     print("Thành công")
# else:
#     print("Thất bại")