from flask import Flask, request, render_template
from datetime import datetime
import fileinput
import sqlite3
app = Flask(__name__)
@app.route('/shop')#店家主頁面
def shop():
    html = """
    <h1>店家頁面</h1>
    <form action='/edit_menu'><input type="submit" value="修改菜單"></form>
    <form action='/edit_history'><input type="submit" value="查看歷史紀錄"></form>
    <form action='/students'><input type="submit" value="進入學生點餐頁面"></form>
    """
    return html

@app.route('/edit_menu',methods=['GET','POST'])#編輯首頁
def edit_menu():
    fn = "menu.txt"
    infile = open(fn,"r",encoding="utf-8")
    menu_content=infile.readlines()
    infile.close()
    return render_template('edit_menu_template.html',menu=menu_content)

@app.route('/add_menu',methods=['GET','POST'])#加菜單
def add_menu():
    fn = "menu.txt"
    if request.method == 'GET':
        infile = open(fn,"r",encoding="utf-8")
        menu_content=infile.readlines()
        infile.close()
        return render_template('add_menu_template.html',menu=menu_content)
    else:
        infile=open(fn,"a",encoding="utf-8")
        print(request.values['item']+" "+request.values['price'], file=infile)
        infile = open(fn,"r",encoding="utf-8")
        menu_content=infile.readlines()
        infile.close()
        return render_template('edit_menu_template.html',menu=menu_content)#回編輯頁面

@app.route('/remove_menu',methods=['GET','POST'])#刪菜單
def remove_menu():
    fn = "menu.txt"
    infile = open(fn,"r",encoding="utf-8")
    menu_content=infile.readlines()
    if request.method == 'GET':
        infile.close()
        return render_template('remove_menu_template.html',menu=menu_content)
    else:
        selected_item=request.values['item']
        temp=[]
        for line in menu_content:
            item = line.split(" ")
            if item[0] != selected_item:
                temp.append(line)
        infile = open(fn,"w",encoding="utf-8")
        for line in temp: 
            print(line, end="",file=infile)
        infile = open(fn,"r",encoding="utf-8")
        menu_content=infile.readlines()  
        infile.close()
        return render_template('edit_menu_template.html',menu=menu_content)
    
@app.route('/edit_history',methods=['GET','POST'])#店家確認及更改紀錄
def edit_history():
    fn = "history.txt"
    infile = open(fn,"r",encoding="utf-8")
    history=infile.readlines()
    infile.close()
    sum=0
    if request.method == 'GET':#顯示菜單
        for line in history:
            item = line.split(" ")
            sum+=int(item[2])
            print(item[5])
        return render_template('edit_history_template.html',history=history,sum=sum)
    else:#顯示篩選菜單
        temp=history[:]
        if  request.values['name']!="":
            history=[]
            for line in temp:
                item = line.split(" ")
                if item[0] == request.values['name']:
                    history.append(line)
        temp=history[:]
        if request.values['date']!="":
            history=[]
            for line in temp:
                item = line.split(" ")
                if item[3] == request.values['date']:
                    history.append(line)
        temp=history[:]
        if request.values['payment']!="free":
            history=[]
            for line in temp:
                item = line.split(" ")
                if item[5] == request.values['payment']:
                    history.append(line)
        for line in history:
            item = line.split(" ")
            sum+=int(item[2])
        return render_template('edit_history_template.html',history=history,sum=sum)
    
@app.route('/edit_data',methods=['GET','POST'])#確認更改消費紀錄頁面與刪除數據
def edit_data():
    if request.method == "GET":#更改消費紀錄
        fn = "history.txt"
        infile = open(fn,"r",encoding="utf-8")
        history=infile.readlines()
        #更改history.txt紀錄
        temp=[]
        for line in history:
            item = line.split(" ")
            print("*",line)
            id=item[0]+" "+item[3]+" "+item[4]
            if request.values.get(id) is not None:#避免篩選過後的資料不完整
                item[5]=request.values[id]
            else:
                item[5]=item[5].strip()
            temp.append(" ".join(item))
        infile = open(fn,"w",encoding="utf-8")
        for line in temp: 
            #print(line)
            print(line,file=infile)
        #顯示繳費過的紀錄
        fn = "history.txt"
        infile = open(fn,"r",encoding="utf-8")
        history=infile.readlines()
        infile.close()
        paid_history=[]
        for line in history:
            item = line.split(" ")
            if item[5].strip() == "paid":
                paid_history.append(line)
        return render_template('edit_data_template.html',history=paid_history)
    else:
        fn = "history.txt"
        infile = open(fn, "r", encoding="utf-8")
        history = infile.readlines()
        # 只留下未繳費紀錄
        temp = []
        for line in history:
            item = line.split(" ")
            if item[5].strip() == "unpaid":
                temp.append(line)
        infile = open(fn, "w", encoding="utf-8")
        for line in temp:
            print(line)
            print(line, end="", file=infile)
        infile.close()
        html = '''
        <h2>已刪除繳費過的資料</h2>
        <form action='/edit_history'><input type="submit" value="繼續查看歷史紀錄"></form>
        <form action='/edit_menu'><input type="submit" value="更改菜單"></form>
        '''
        return html

@app.route('/students',methods=['GET','POST'])#學生點餐頁面
def students():
    if request.method == "GET":
        fn = "menu.txt"
        infile = open(fn,"r",encoding="utf-8")
        menu_content=infile.readlines()
        infile.close()
        return render_template('students_template.html',menu=menu_content)
    else: # POST
        #記錄到表單中
        # current_datetime = datetime.now()
        # formatted_datetime = current_datetime.strftime('%Y-%m-%d %H:%M')
        # d1 = datetime.strptime(formatted_datetime, '%Y-%m-%d %H:%M') 
        d1=str(datetime.now())
        f = open("history.txt", "a",encoding="utf-8")
        choice=request.values['lunch'].split("$")
        print(request.values['name']+" "+choice[0]+request.values['detail']+" "+choice[1].strip()+" "+str(d1)+" unpaid", file=f)
        #將資料加入database
        db_filename = 'history.db'
        conn = sqlite3.connect(db_filename)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO history(name,item,price,date,payment) VALUES ({},"{}","{}","{}","unpaid");'.format(request.values['name'],choice[0]+request.values['detail'],choice[1].strip(),str(d1)))
        conn.commit()
        conn.close()
        f.close()
        #顯示頁面
        html='<h3>{}成功送出{}{}的訂單</h3>'.format(request.values['name'],request.values['lunch'],request.values['detail'])
        html+='''
        <form action=/students method="get">
            <button type="submit">
            繼續點餐</button>
        </form>
        <form action="/view_history" method="get">
            <button type="submit">查看點餐紀錄</button>
        </form>
        '''
    return html

@app.route('/view_history',methods=['GET','POST'])#學生確認紀錄
def view_history():
    #從history.txt中取得
    sum=0
    fn = "history.txt"
    infile = open(fn,"r",encoding="utf-8",errors='ignore')
    history=infile.readlines()
    infile.close()
    if request.method == 'GET':
        for line in history:
            item = line.split(" ")
            sum+=int(item[2])
        return render_template('view_history_template.html',history=history,sum=sum)
    else:
        sum=0
        temp=history[:]
        if  request.values['name']!="":
            history=[]
            for line in temp:
                item = line.split(" ")
                if item[0] == request.values['name']:
                    history.append(line)
        temp=history[:]
        if request.values['date']!="":
            history=[]
            for line in temp:
                item = line.split(" ")
                if item[3] == request.values['date']:
                    history.append(line)
        temp=history[:]
        if request.values['payment']!="free":
            print("++++++++++++++++")
            history=[]
            for line in temp:
                item = line.split(" ")
                if item[5].strip() == request.values['payment'].strip():
                    history.append(line)
        for line in history:
            item = line.split(" ")
            sum+=int(item[2])
        return render_template('view_history_template.html',history=history,sum=sum)
