import random
import openpyxl

def create():
    list=['198','133','156','151','134','137','150','188','187','173','185']
    #获取手机号开头，列表里随机取一个
    title=random.choice(list)
    num='0123456789'
    #创建一个空字符串，用于接收手机号后8位
    list=''
    for i in range(8):
        #循环8次，每次在num里随机取一个数存放到list中生成手机号后8位
        last1=random.choice(num)
        list=list+last1
    #拼接手机号开头和后8位
    phone=title+list
    return phone

def write_excel():
    pwd='123456'
    #创建list空列表，用于存放单条手机号和密码
    list=[]
    #创建list_user空列表，用于存放所有手机号和密码
    list_user=[]
    for i in range(20000):
        #循环10次，生成10条数据
        #调用上方create()函数，生成单条手机号和密码
        list=[create(),pwd]
        #每次循环生成的单条手机号和密码放入lsit_user列表中
        list_user.append(list)
    wb=openpyxl.Workbook()
    sheet=wb.active
    #excel.sheet1中插入单元格开头
    a=['phone','paw']
    sheet.append(a)
    #在sheet中循环插入list_user中的每条数据
    for i in range(len(list_user)):
        sheet.append(list_user[i])
    wb.save(r'C:\Users\fyp\Desktop\test22.xlsx')



if __name__ == '__main__':
    write_excel()

