from flask import Flask, render_template, request, redirect, flash, session, url_for
import sqlite3, time, matplotlib, matplotlib.pyplot as plt
from werkzeug.security import generate_password_hash, check_password_hash
matplotlib.use('Agg')


app = Flask("__name__")
app.secret_key = "Shahzada"

con = sqlite3.connect("instance/A_Z_Household_Services.db")
cur = con.cursor()


def id(Category, Service, BasePrice):
    Id = ""
    count = 0
    for i in Category:
        if count <= 2:
            if i != " " and i != ".":
                Id += i
                count += 1
    count = 0
    for i in Service:
        if count <= 2:
            if i != " " and i != ".":
                Id += i
                count += 1
    Id = Id.upper()
    Id += BasePrice[2:]
    return Id.strip()



@app.route("/", methods = ["GET", "POST"])
def home():
    if request.method == "GET":
        con = sqlite3.connect("instance/A_Z_Household_Services.db")
        cur = con.cursor()
        query = "SELECT ServiceId, Category, Service, BasePrice, Description FROM Services"
        r = cur.execute(query)
        r = r.fetchall()
        return render_template("index.html", items = r)
    else:
        con = sqlite3.connect("instance/A_Z_Household_Services.db")
        cur = con.cursor()
        query = "SELECT Category, Service, BasePrice, Description FROM Services"
        r = cur.execute(query)
        r = r.fetchall()
        return render_template("index.html", items = r)

@app.route("/customer-signup", methods = ["GET", "POST"])
def CustomerSignup():
    if request.method == "GET":
        return render_template("CustomerSignUp.html")
    else:
        UserName = str(request.form["UserName"])
        UserType = "Customer"
        Email = str(request.form["Email"])
        Dob = str(request.form["Dob"])
        Address = str(request.form["Address"])
        Pincode = str(request.form["Pincode"])
        Password = str(request.form["Password"])
        VerifyPassword = str(request.form["VerifyPassword"])
        Date = time.ctime()

        if (Password == VerifyPassword):
            Password = generate_password_hash(Password)
            con = sqlite3.connect("instance/A_Z_Household_Services.db")
            cur = con.cursor()
            data1 = (Email, UserName, UserType, Dob, Password,)
            query1 = "INSERT INTO UserDetails VALUES(?, ?, ?, ?, ?)"
            cur.execute(query1, data1)
            data2 = (Email, UserName, Dob, Address, Pincode, Date, )
            query2 = "INSERT INTO ServiceUsers VALUES(?, ?, ?, ?, ?, ?)"
            cur.execute(query2, data2)

            con.commit()
            return render_template("CustomerSignUp.html", comment = "Congratulations ! Your account has been succesfuly created. Now login into your account.")

        else:
            return render_template("CustomerSignUp.html", Warning = "Warning : ", Comment = "The Password And Verify Password doesn't match.")

@app.route("/professional-signup", methods = ["GET", "POST"])
def ProfessionalSignup():
    if request.method == "GET":
        return render_template("ServiceProfessionalSignUp.html")
    else:
        UserName = str(request.form["UserName"])
        UserType = "Professional"
        Email = str(request.form["Email"])
        Dob = str(request.form["Dob"])
        Service = str(request.form["Service"])
        Experience = str(request.form["Experience"])
        Address = str(request.form["Address"])
        Pincode = str(request.form["Pincode"])
        Password = str(request.form["Password"])
        VerifyPassword = str(request.form["VerifyPassword"])
        Date = time.ctime()
        Status = "Not Approved"

        if (Password == VerifyPassword):
            Password = generate_password_hash(Password)
            con = sqlite3.connect("instance/A_Z_Household_Services.db")
            cur = con.cursor()
            data1 = (Email, UserName, UserType, Dob, Password,)
            query1 = "INSERT INTO UserDetails VALUES(?, ?, ?, ?, ?)"
            cur.execute(query1, data1)
            data2 = (Email, UserName, Dob, Service,Experience, Address, Pincode, Date, Status,)
            query2 = "INSERT INTO ServiceProviders VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)"
            cur.execute(query2, data2)
            con.commit()
            return render_template("ServiceProfessionalSignUp.html", comment = "Congratulations ! Your account has been succesfuly created. Now login into your account.")

        else:
            return render_template("ServiceProfessionalSignUp.html", Comment = "Warning : The Password And Verify Password doesn't match.")


@app.route("/admin-dashboard", methods = ["GET", "POST"])
def AdminDashboard():
    if request.method == "GET" or request.method == "POST":
        if 'User' in session:
            con = sqlite3.connect("instance/A_Z_Household_Services.db")
            cur = con.cursor()

            query1 = "SELECT ServiceId, Category, Service, BasePrice, Description FROM Services"
            r1 = cur.execute(query1)
            r1 = r1.fetchall()

            query2 = "SELECT ProfessionalName, Experience, ProfessionalEmail , Category FROM ServiceProviders WHERE STATUS == ?"
            data2 = ('Not Approved', )
            r2 = cur.execute(query2, data2)
            r2 = r2.fetchall()

            query3 = "SELECT ProfessionalName, Experience, ProfessionalEmail , Category, Status, Date FROM ServiceProviders"
            r3 = cur.execute(query3)
            r3 = r3.fetchall()

            return render_template("AdminDashboard.html", User=session['User'], items1 = r1, items2 = r2, items3 = r3)


@app.route("/professional-dashboard", methods = ["GET", "POST"])
def ProfessionalDashboard():
    if 'User' in session:
        if request.method == "GET":
            return render_template("ProfessionalDashboard.html", User=session['User'])
        else:
            con = sqlite3.connect("instance/A_Z_Household_Services.db")
            cur = con.cursor()
            Date = time.ctime()

            query1 = "SELECT CustomerEmail, CustomerName, Service, ProfessionalName, ProfessionalEmail, BasePrice, Status, Date FROM UserServices WHERE ProfessionalEmail == ? AND Status == ?"
            data1 = (session['Email'], 'Requested',)
            r1 = cur.execute(query1, data1)
            r1 = r1.fetchall()
            for i in range(len(r1)):
                r1[i] = list(r1[i])
                query = "SELECT Address, Pincode FROM ServiceUsers WHERE CustomerEmail == ?"
                data = (r1[i][0], )
                r = cur.execute(query, data)
                r = r.fetchone()
                if r is not None:
                    r1[i].append(r[0] + " - " + str(r[1]))
            print(r1)

            query2 = "SELECT CustomerName, CustomerEmail, CustomerAddress, Service FROM ProfessionalServices WHERE ProfessionalEmail == ? AND Status == ?"
            data2 = (session['Email'],'Ongoing',)
            r2 = cur.execute(query2, data2)
            r2 = r2.fetchall()

            query3 = "SELECT CustomerName, CustomerEmail, CustomerAddress, Service, Ratings FROM ProfessionalServices WHERE ProfessionalEmail == ? AND Ratings <> ?"
            data3 = (session['Email'], '',)
            r3 = cur.execute(query3, data3)
            r3 = r3.fetchall()

            return render_template("ProfessionalDashboard.html", User=session['User'], items = r1, items2 = r2, items3 = r3)


@app.route("/dashboard", methods = ["GET", "POST"])
def Dashboard():
    if request.method == "POST" or request.method == "GET":
        if 'User' in session:
            con = sqlite3.connect("instance/A_Z_Household_Services.db")
            cur = con.cursor()
            query = "SELECT DISTINCT Category FROM Services"
            r = cur.execute(query)
            r = r.fetchall()

            query2 = "SELECT Service, ProfessionalName, ProfessionalEmail, Status FROM UserServices WHERE CustomerEmail == ? AND Status == ?"
            data2 = (session['Email'], 'Accepted',)
            r2 = cur.execute(query2, data2)
            r2 = r2.fetchall()

            return render_template("Dashboard.html", User=session['User'], Email = session['Email'], items=r, items2 = r2)

@app.route("/customer-services/<Category>", methods = ["GET", "POST"])
def CustomerServices(Category):
    if 'User' in session and 'Email' in session:
        if request.method == "GET":
            con = sqlite3.connect("instance/A_Z_Household_Services.db")
            cur = con.cursor()
            query1 = "SELECT Service, BasePrice FROM Services WHERE Category == ?"
            data1 = (Category,)
            r1 = cur.execute(query1, data1)
            r1 = r1.fetchall()

            query2 = "SELECT ProfessionalName, ProfessionalEmail FROM ServiceProviders WHERE Category == ?"
            data2 = (Category,)
            r2 = cur.execute(query2, data2)
            r2 = r2.fetchall()
            items = []

            for i in r1:
                for j in r2:
                    items.append((i[0], j[0], j[1], i[1]))

            query3 = "SELECT Service, ProfessionalName, ProfessionalEmail, Status, CustomerEmail, Date FROM UserServices WHERE CustomerEmail == ? AND Category == ?"
            data3 = (session['Email'], Category,)
            r3 = cur.execute(query3, data3)
            r3 = r3.fetchall()

            for i in range(len(r3)):
                r3[i] = list(r3[i])
                link = "/customer-rating/" + r3[i][2] + "/" + r3[i][4] + "/" + r3[i][0] + "/" + r3[i][5]
                r3[i].append(link)
                if r3[i][3] == "Accepted":
                    query = "SELECT Ratings, CustomerName, customerEmail, CustomerAddress, Service FROM ProfessionalServices WHERE ProfessionalEmail == ? AND CustomerEmail == ? AND Service == ? AND Date == ?"
                    data = (r3[i][2], r3[i][4], r3[i][0], r3[i][5],)
                    r = cur.execute(query, data)
                    r = r.fetchone()
                    if r:
                        if r[0] != "":
                            img = "/static/Image/" + r[0] + '.png'
                            r3[i].append(img)

            return render_template("CustomerServices.html", Category=Category, User=session['User'], items=items,
                                   Email=session['Email'], items3=r3)

        else:
            con = sqlite3.connect("instance/A_Z_Household_Serices.db")
            cur = con.cursor()
            query = "SELECT Service FROM Services WHERE Category == ?"
            data = (Category,)
            r = cur.execute(query, data)
            r = r.fetchall()
            return render_template("CustomerServices.html", Category=Category, User=session['User'], items=r, Email=session['Email'])

    else:
        return redirect(url_for('Login'))



@app.route("/customer-rating/<ProfessionalEmail>/<CustomerEmail>/<Service>/<Date>/", methods = ["GET", "POST"])
def ServiceRating(ProfessionalEmail, CustomerEmail, Service, Date):
    if request.method == "GET":
        con = sqlite3.connect("instance/A_Z_Household_Services.db")
        cur = con.cursor()
        query1 = "SELECT Service, Category, BasePrice, ProfessionalName, ProfessionalEmail, Date FROM UserServices WHERE ProfessionalEmail = ? AND CustomerEmail = ? AND Service = ? AND Date = ?"
        data1 = (ProfessionalEmail, CustomerEmail, Service, Date,)
        r1 = cur.execute(query1, data1)
        r1 = r1.fetchone()
        RequestId = r1[0][:3] + r1[1][:3] + r1[4][:3] + r1[5][4:]
        RequestId = list(RequestId);  RequestId.remove(":"); RequestId.remove(":"); count = RequestId.count(" ");
        for i in range(count):
            RequestId.remove(" ")
        str = ""
        for i in RequestId :
            str += i
        RequestId = str

        return render_template("ServiceRating.html", ProfessionalEmail=ProfessionalEmail, CustomerEmail=CustomerEmail, Service=Service, Date=Date, items = r1, RequestId=RequestId)
    else:
        s1 = int(request.form.get("star01", '0'))
        s2 = int(request.form.get("star02", '0'))
        s3 = int(request.form.get("star03", '0'))
        s4 = int(request.form.get("star04", '0'))
        s5 = int(request.form.get("star05", '0'))
        d = str(request.form["description"])

        if s5 == 5:
            star = 5
        elif s4 == 4:
            star = 4
        elif s3 == 3:
            star = 3
        elif s2 == 2:
            star = 5
        elif s1 == 1:
            star = 1
        else:
            star = 5

        con = sqlite3.connect("instance/A_Z_Household_Services.db")
        cur = con.cursor()

        query = """UPDATE ProfessionalServices SET Ratings = ? WHERE ProfessionalEmail = ? AND CustomerEmail = ? AND Service = ? AND Date = ?"""
        data = (star, ProfessionalEmail, CustomerEmail, Service, Date)
        cur.execute(query, data)
        con.commit()
        con.close()
        return "Thankyou For Your Rating !"


@app.route("/login", methods = ["GET", "POST"])
def Login():
    if request.method == "GET":
        return render_template("AdminLogin.html")
    else:
        Email = str(request.form["Email"])
        Password = str(request.form["Password"])

        con = sqlite3.connect("instance/A_Z_Household_Services.db")
        cur = con.cursor()
        query = "SELECT UserName,UserType, Password FROM UserDetails WHERE Email == ?"
        r = cur.execute(query, (Email,))
        r = r.fetchall()
        if check_password_hash(r[0][2], Password):
            User = r[0][0]
            session['User'] = User
            session['Email'] = Email
            if r[0][1] == "Admin":
                return AdminDashboard()
            elif r[0][1] == "Professional":
                return ProfessionalDashboard()
            else:
                return Dashboard()
        else:
            return render_template("AdminLogin.html", Comment = "Warning ! Username or Password is incorrect.")

@app.route("/AddService", methods = ["GET", "POST"])
def AddService():
    if request.method == "GET":
        return render_template("NewService.html")
    else:
        Category = str(request.form["Category"])
        ServiceName = str(request.form["ServiceName"])
        Description = str(request.form["Description"])
        BasePrice = str(request.form["BasePrice"]);
        if "₹ " not in BasePrice:
            BasePrice = "₹ " + BasePrice
        ServiceId = id(Category, ServiceName, BasePrice)

        con = sqlite3.connect("instance/A_Z_Household_Services.db")
        cur = con.cursor()
        query = "INSERT INTO Services VALUES(?,?,?,?,?,?)"
        data = (ServiceId, Category, ServiceName, BasePrice, time.ctime(), Description, )
        cur.execute(query, data)
        con.commit()
        Message = "The new service has been added."
        return render_template("NewService.html", message = Message)

@app.route("/delete/<Service_Id>/")
def delete(Service_Id):
    con = sqlite3.connect("instance/A_Z_Household_Services.db")
    cur = con.cursor()
    query = "DELETE FROM Services WHERE ServiceId == ?"
    data = (Service_Id,)
    cur.execute(query, data)
    con.commit()
    return AdminDashboard()

@app.route("/update/<Service>/<BasePrice>/<Description>/", methods = ["GET", "POST"])
def Update(Service, BasePrice, Description):
    if request.method == "POST":
        con = sqlite3.connect("instance/A_Z_Household_Services.db")
        cur = con.cursor()
        Category = str(request.form["Category"])
        service_name = str(request.form["ServiceName"])
        description = str(request.form["Description"])
        base_price = str(request.form["BasePrice"]);
        if "₹ " not in base_price:
            base_price = "₹ " + base_price
        BasePrice = "₹ " + BasePrice
        ServiceId = id(Category, Service, BasePrice)
        Date = time.ctime()

        query = """UPDATE Services 
        SET ServiceId = ?, Category = ?, Service = ?, BasePrice = ?, Date = ?, Description = ? 
        WHERE Service = ? AND BasePrice = ? AND Description = ?"""
        data = (ServiceId, Category, service_name, base_price, Date, description, Service, BasePrice, Description,)
        cur.execute(query, data)
        con.commit()
        con.close()
        return render_template("update.html", message = "Congratulations ! The service Data has been updated.")
    else:
        return render_template("update.html", ServiceName=Service, BasePrice=BasePrice[2:], Description=Description)

@app.route("/DeleteProfessional/<Email>/")
def DeleteProfessional(Email):
    con = sqlite3.connect("instance/A_Z_Household_Services.db")
    cur = con.cursor()
    query = "DELETE FROM ServiceProviders WHERE ProfessionalEmail == ?"
    data = (Email,)
    cur.execute(query, data)
    con.commit()
    return AdminDashboard()

@app.route("/ApproveProfessional/<Email>/")
def ApproveProfessional(Email):
    con = sqlite3.connect("instance/A_Z_Household_Services.db")
    cur = con.cursor()
    query = """UPDATE ServiceProviders SET Status = ? WHERE ProfessionalEmail == ?"""
    data = ('Approved', Email,)
    cur.execute(query, data)
    con.commit()
    return AdminDashboard()

@app.route("/RejectProfessional/<Email>/")
def RejectProfessional(Email):
    con = sqlite3.connect("instance/A_Z_Household_Services.db")
    cur = con.cursor()
    query = """UPDATE ServiceProviders SET Status = ? WHERE ProfessionalEmail == ?"""
    data = ('Rejected', Email,)
    cur.execute(query, data)
    con.commit()
    return AdminDashboard()


@app.route("/BookService/<Email>/<Customer>/<ServiceName>/<ProfessionalName>/<ProfessionalEmail>/<BasePrice>/<Category>/")
def BookService(Email, Customer, ServiceName, ProfessionalName, ProfessionalEmail, BasePrice, Category):

    con = sqlite3.connect("instance/A_Z_Household_Services.db")
    cur = con.cursor()
    Date = time.ctime()

    query1 = "SELECT CustomerEmail, CustomerName, Service, ProfessionalName, ProfessionalEmail, BasePrice, Status FROM UserServices WHERE CustomerEmail == ? AND CustomerName == ? AND Service == ? AND ProfessionalName == ? AND ProfessionalEmail == ? AND BasePrice == ? AND Status == ?"
    data1 = (Email, Customer, ServiceName, ProfessionalName, ProfessionalEmail, BasePrice, 'Requested',)
    r1 = cur.execute(query1, data1)
    r1 = r1.fetchone()

    if r1:
        return("Warning ! Service Already Booked.")

    else:
        query2 = "INSERT INTO UserServices VALUES(?,?,?,?,?,?,?,?)"
        data2 = (Email, Customer, ServiceName, Category, ProfessionalName, ProfessionalEmail, BasePrice, 'Requested', Date,)
        cur.execute(query2, data2)
        con.commit()
        return CustomerServices(Category)


@app.route("/AcceptService/<Service>/<CustomerName>/<CustomerEmail>/<CustomerAddress>/<BasePrice>/<Date>/")
def AcceptService(CustomerName,CustomerEmail,CustomerAddress,Service,BasePrice,Date):
    con = sqlite3.connect("instance/A_Z_Household_Services.db")
    cur = con.cursor()

    query1 = "SELECT * FROM ProfessionalServices WHERE ProfessionalEmail == ? AND ProfessionalName == ? AND CustomerName == ? AND CustomerEmail == ? AND CustomerAddress == ? AND Service == ? AND BasePrice == ? AND Date == ?"
    data1 = (session['Email'], session['User'], CustomerName, CustomerEmail, CustomerAddress, Service, BasePrice, Date,)
    r1 = cur.execute(query1, data1)
    r1 = r1.fetchone()

    print(Service, CustomerName, CustomerEmail, CustomerAddress, BasePrice, Date)

    if not r1:
        query = "INSERT INTO ProfessionalServices VALUES(?,?,?,?,?,?,?,?,?,?)"
        data = (session['Email'], session['User'], Service, CustomerName, CustomerEmail, CustomerAddress, BasePrice, Date, 'Ongoing',"",)
        cur.execute(query, data)

        query = """UPDATE UserServices SET Status = ? WHERE CustomerEmail == ? AND ProfessionalEmail == ? AND Date == ?"""
        data = ('Accepted', CustomerEmail, session['Email'], Date)
        cur.execute(query, data)
        con.commit()
        return redirect(url_for("ProfessionalDashboard"))

    else:
        return ("Request Already Accepted !")


@app.route("/ServiceRejected/<Email>/<Date>/")
def ServiceRejected(Email, Date):
    con = sqlite3.connect("instance/A_Z_Household_Services.db")
    cur = con.cursor()
    query = """UPDATE UserServices SET Status = ? WHERE CustomerEmail == ? AND ProfessionalEmail == ? AND Date == ?"""
    data = ('Rejected', Email, session['Email'], Date)
    cur.execute(query, data)
    con.commit()
    return "The service request has been rejected."


@app.route("/Payment/<Email>/<Customer>/<ServiceName>/<ProfessionalName>/<ProfessionalEmail>/<BasePrice>/<Category>/", methods = ["GET", "POST"])
def Payment(Email, Customer, ServiceName, ProfessionalName, ProfessionalEmail, BasePrice, Category):
    if request.method == "GET":
        return render_template("Payment.html", Email=Email, Customer=Customer, ServiceName=ServiceName, ProfessionalName=ProfessionalName, ProfessionalEmail=ProfessionalEmail, BasePrice=BasePrice, Category=Category)
    else:
        Name = str(request.form["Name"])
        Email = str(request.form["Email"])
        Address = str(request.form["Address"])
        City = str(request.form["City"])
        State = str(request.form["State"])
        Pincode = str(request.form["Pincode"])
        CardHolderName = str(request.form["CardHolderName"])
        CreditCardNumber = str(request.form["CreditCardNumber"])
        Month = str(request.form["Month"])
        ExpiryYear = str(request.form["ExpiryYear"])
        Cvv = str(request.form["Cvv"])
        Date = time.ctime()

        con = sqlite3.connect("instance/A_Z_Household_Services.db")
        cur = con.cursor()
        Date = time.ctime()

        query1 = "INSERT INTO UserServices VALUES(?,?,?,?,?,?,?,?,?)"
        data1 = (Email, Customer, ServiceName, Category, ProfessionalName, ProfessionalEmail, BasePrice, 'Requested', Date,)
        cur.execute(query1, data1)

        query2 = "INSERT INTO Payments VALUES(?,?,?,?,?,?,?)"
        data2 = (Customer, Email, ProfessionalName, ProfessionalEmail, ServiceName, BasePrice, Date,)
        cur.execute(query2, data2)
        con.commit()
        return "The payment has done successfully. Now login into your account again."


@app.route("/Search", methods = ["GET", "POST"])
def Search():
    if 'User' in session and 'Email' in session:
        if request.method == "GET":
            return render_template("Search.html")
        else:
            data = str(request.form["data"])
            con = sqlite3.connect("instance/A_Z_Household_Services.db")
            cur = con.cursor()
            Date = time.ctime()

            query1 = "SELECT ProfessionalName, ProfessionalEmail, Category, Pincode FROM ServiceProviders WHERE ProfessionalName == ?"
            data1 = (data,)
            r1 = cur.execute(query1, data1).fetchall()

            if r1:
                for i in range(len(r1)):
                    r1[i] = list(r1[i])
                    query2 = "SELECT Service FROM UserServices WHERE ProfessionalName == ?"
                    data2 = (r1[i][0],)
                    r2 = cur.execute(query2, data2).fetchone()
                    if r2:
                        r1[i].append(r2[0])
                    else:
                        r1[i].append("Not Available")
                return render_template("Search.html", items1 = r1)
            else:
                query1 = "SELECT ProfessionalName, ProfessionalEmail, Category, Pincode FROM ServiceProviders WHERE ProfessionalEmail == ?"
                data1 = (data,)
                r1 = cur.execute(query1, data1).fetchall()
                if r1:
                    for i in range(len(r1)):
                        r1[i] = list(r1[i])
                        query2 = "SELECT Service FROM UserServices WHERE ProfessionalName == ?"
                        data2 = (r1[i][0],)
                        r2 = cur.execute(query2, data2).fetchone()
                        if r2:
                            r1[i].append(r2[0])
                        else:
                            r1[i].append("Not Available")
                    return render_template("Search.html", items1=r1)
                else:
                    query1 = "SELECT ProfessionalName, ProfessionalEmail, Category, Pincode FROM ServiceProviders WHERE Category == ?"
                    data1 = (data,)
                    r1 = cur.execute(query1, data1).fetchall()
                    if r1:
                        for i in range(len(r1)):
                            r1[i] = list(r1[i])
                            query2 = "SELECT Service FROM UserServices WHERE ProfessionalName == ?"
                            data2 = (r1[i][0],)
                            r2 = cur.execute(query2, data2).fetchone()
                            if r2:
                                r1[i].append(r2[0])
                            else:
                                r1[i].append("Not Available")
                        return render_template("Search.html", items1=r1)
                    else:
                        query1 = "SELECT ProfessionalName, ProfessionalEmail, Category, Pincode FROM ServiceProviders WHERE Pincode == ?"
                        data1 = (data,)
                        r1 = cur.execute(query1, data1).fetchall()
                        if r1:
                            for i in range(len(r1)):
                                r1[i] = list(r1[i])
                                query2 = "SELECT Service FROM UserServices WHERE ProfessionalName == ?"
                                data2 = (r1[i][0],)
                                r2 = cur.execute(query2, data2).fetchone()
                                if r2:
                                    r1[i].append(r2[0])
                                else:
                                    r1[i].append("Not Available")
                            return render_template("Search.html", items1=r1)
                        else:
                            flash("Data Not Found !")
                            return render_template("Search.html")

    else:
        return redirect(url_for('Login'))

@app.route("/AdminSummary", methods = ["GET", "POST"])
def AdminSummary():
    if request.method == "GET":
        con = sqlite3.connect("instance/A_Z_Household_Services.db")
        cur = con.cursor()
        query1 = "SELECT Ratings FROM ProfessionalServices"
        r1 = cur.execute(query1)
        r1 = r1.fetchall()
        z = []
        d1 = {}
        for i in r1:
            if i[0] == "5":
                d1["5-Star"] = 0
                z.append("5-Star")
            elif i[0] == "4":
                d1["4-Star"] = 0
                z.append("4-Star")
            elif i[0] == "3":
                d1["3-Star"] = 0
                z.append("3-Star")
            elif i[0] == "2":
                d1["2-Star"] = 0
                z.append("2-Star")
            elif i[0] == "1":
                d1["1-Star"] = 0
                z.append("1-Star")

        for i in d1:
            d1[i] = z.count(i)
        plt.clf()
        p = plt.bar(list(d1.keys()),list(d1.values()))
        plt.savefig("/Users/shahzadamoon/Documents/A-Z Household Project/static/Image/AdminSummary-1.jpg")

        plt.clf()
        p = plt.pie(list(d1.values()), labels = list(d1.keys()))
        plt.savefig("/Users/shahzadamoon/Documents/A-Z Household Project/static/Image/AdminSummary-2.jpg")

        query2 = "SELECT Status FROM ServiceProviders"
        r2 = cur.execute(query2)
        r2 = r2.fetchall()
        z2 = []
        d2 = {}
        for i in r2:
            d2[i[0]] = 0
            z2.append(i[0])
        for i in d2:
            d2[i] = z2.count(i)

        plt.clf()
        p = plt.bar(list(d2.keys()), list(d2.values()))
        plt.savefig("/Users/shahzadamoon/Documents/A-Z Household Project/static/Image/AdminSummary-3.jpg")
        plt.clf()
        p = plt.pie(list(d2.values()), labels = list(d2.keys()))
        plt.savefig("/Users/shahzadamoon/Documents/A-Z Household Project/static/Image/AdminSummary-4.jpg")

        return render_template('AdminSummary.html' , User = session['User'])


@app.route("/ProfessionalSummary", methods = ["GET", "POST"])
def ProfessionalSummary():
    if request.method == "GET":
        con = sqlite3.connect("instance/A_Z_Household_Services.db")
        cur = con.cursor()
        query1 = "SELECT Ratings FROM ProfessionalServices WHERE ProfessionalEmail == ?"
        data1 = (session['Email'],)
        r1 = cur.execute(query1, data1)
        r1 = r1.fetchall()
        z = []
        d1 = {}
        for i in r1:
            if i[0] == "5":
                d1["5-Star"] = 0
                z.append("5-Star")
            elif i[0] == "4":
                d1["4-Star"] = 0
                z.append("4-Star")
            elif i[0] == "3":
                d1["3-Star"] = 0
                z.append("3-Star")
            elif i[0] == "2":
                d1["2-Star"] = 0
                z.append("2-Star")
            elif i[0] == "1":
                d1["1-Star"] = 0
                z.append("1-Star")

        for i in d1:
            d1[i] = z.count(i)
        plt.clf()
        p = plt.bar(list(d1.keys()),list(d1.values()))
        plt.savefig("/Users/shahzadamoon/Documents/A-Z Household Project/static/Image/ProfessionalSummary-1.jpg")

        plt.clf()
        p = plt.pie(list(d1.values()), labels = list(d1.keys()))
        plt.savefig("/Users/shahzadamoon/Documents/A-Z Household Project/static/Image/ProfessionalSummary-2.jpg")

        query2 = "SELECT Status FROM UserServices WHERE ProfessionalEmail == ?"
        data2 = (session['Email'],)
        r2 = cur.execute(query2, data2)
        r2 = r2.fetchall()
        z2 = []
        d2 = {}
        for i in r2:
            if i[0] == "Requested":
                d2["Pending Requests"] = 0
                z2.append("Pending Requests")
            elif i[0] == "Accepted":
                d2["Accepted Requests"] = 0
                z2.append("Accepted Requests")
            else:
                d2["Rejected Requests"] = 0
                z2.append("Rejected Requests")
        for i in d2:
            d2[i] = z2.count(i)


        plt.clf()
        p = plt.bar(list(d2.keys()), list(d2.values()))
        plt.savefig("/Users/shahzadamoon/Documents/A-Z Household Project/static/Image/ProfessionalSummary-3.jpg")
        plt.clf()
        p = plt.pie(list(d2.values()), labels = list(d2.keys()))
        plt.savefig("/Users/shahzadamoon/Documents/A-Z Household Project/static/Image/ProfessionalSummary-4.jpg")

        return render_template('ProfessionalSummary.html' , User = session['User'])

@app.route("/CustomerSummary", methods = ["GET", "POST"])
def CustomerSummary():
    if 'Email' in session:
        if request.method == "GET":
            con = sqlite3.connect("instance/A_Z_Household_Services.db")
            cur = con.cursor()
            query = "SELECT Status FROM UserServices WHERE CustomerEmail == ?"
            data = (session['Email'],)
            r = cur.execute(query, data)
            r = r.fetchall()
            z = []
            d = {}
            for i in r:
                if i[0] == "Requested":
                    d["Pending Requests"] = 0
                    z.append("Pending Requests")
                elif i[0] == "Accepted":
                    d["Accepted Requests"] = 0
                    z.append("Accepted Requests")
                else:
                    d["Rejected Requests"] = 0
                    z.append("Rejected Requests")
            for i in d:
                d[i] = z.count(i)
            plt.clf()
            p = plt.bar(list(d.keys()),list(d.values()))
            plt.savefig("/Users/shahzadamoon/Documents/A-Z Household Project/static/Image/CustomerSummary-1.jpg")

            plt.clf()
            p = plt.pie(list(d.values()), labels = list(d.keys()))
            plt.savefig("/Users/shahzadamoon/Documents/A-Z Household Project/static/Image/CustomerSummary-2.jpg")

            return render_template('CustomerSummary.html', User = session['User'], Email=session['Email'])
        else:
            return redirect(url_for('Login'))

@app.route("/CustomerProfile/<Email>/", methods = ["GET", "POST"])
def CustomerProfile(Email):
    if request.method == "GET":
        con = sqlite3.connect("instance/A_Z_Household_Services.db")
        cur = con.cursor()
        query = "SELECT CustomerEmail, CustomerName, Dob, Address, Pincode FROM ServiceUsers WHERE CustomerEmail == ?"
        data = (Email,)
        Email = session['Email']
        r = cur.execute(query, data)
        r = r.fetchone()
        return render_template("CustomerProfile.html", r = r, Email = Email)
    else:
        UserName = str(request.form["UserName"])
        Email = str(request.form["Email"])
        Dob = str(request.form["Dob"])
        Address = str(request.form["Address"])
        Pincode = str(request.form["Pincode"])

        con = sqlite3.connect("instance/A_Z_Household_Services.db")
        cur = con.cursor()
        data1 = (UserName, Dob, Address, Pincode, Email,)
        query1 = """UPDATE  ServiceUsers SET CustomerName = ?, Dob = ?, Address = ?, Pincode = ? WHERE CustomerEmail == ?"""
        cur.execute(query1, data1)
        con.commit()
        flash("Congratulations ! Your Profile has been updated successfully.")

        return redirect(url_for("CustomerProfile", Email=session['Email']))

@app.route("/ProfessionalProfile/", methods = ["GET", "POST"])
def ProfessionalProfile():
    if request.method == "GET":
        con = sqlite3.connect("instance/A_Z_Household_Services.db")
        cur = con.cursor()
        query = "SELECT ProfessionalEmail, ProfessionalName, Dob, Category, Experience, Address, Pincode FROM ServiceProviders WHERE ProfessionalEmail == ?"
        Email = session['Email']
        data = (Email,)
        r = cur.execute(query, data)
        r = r.fetchone()
        return render_template("ProfessionalProfile.html", r = r)
    else:
        UserName = str(request.form["UserName"])
        Email = str(request.form["Email"])
        Dob = str(request.form["Dob"])
        Category = str(request.form["Category"])
        Experience = str(request.form["Experience"])
        Address = str(request.form["Address"])
        Pincode = str(request.form["Pincode"])

        con = sqlite3.connect("instance/A_Z_Household_Services.db")
        cur = con.cursor()
        data1 = (UserName, Dob, Category, Experience, Address, Pincode, Email,)
        query1 = """UPDATE  ServiceProviders SET ProfessionalName = ?, Dob = ?, Category = ?, Experience = ?, Address = ?, Pincode = ? WHERE ProfessionalEmail == ?"""
        cur.execute(query1, data1)
        con.commit()
        flash("Congratulations ! Your Profile has been updated successfully.")
        return redirect(url_for("ProfessionalProfile"))


@app.route("/Logout")
def Logout():
    session.pop('Email', None)
    return render_template('AdminLogin.html')

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=5000)