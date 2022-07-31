from re import T
from flask import Flask,render_template,request,session,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from datetime import datetime


app = Flask(__name__)
app.secret_key = 'super-secret-key'
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNEME='',
    MAIL_PASSWORD='')


mail=Mail(app)

app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:@localhost/coadingthuder'
  
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)
class Contacts(db.Model):
    name=db.Column(db.String(200),primary_key=True,nullable=False)
    email=db.Column(db.String(20),nullable=False)
    phone_num=db.Column(db.String(20),nullable=False,)
    mes=db.Column(db.String(200),nullable=False)

class Posts(db.Model):
    sno=db.Column(db.INTEGER,primary_key=True)
    title=db.Column(db.String(50),nullable=False)
    slug=db.Column(db.String(30),nullable=False)
    containt=db.Column(db.String(200),nullable=False)
    date=db.Column(db.String(12),nullable=False)
    img_file=db.Column(db.String(30),nullable=False)
    tagline=db.Column(db.String(100),nullable=False)


@app.route("/dashbord",methods=['GET','POST'])
def dashbord():
    if ('user' in session and session['user']=='sidd'):
         post=Posts.query.all()
         return render_template("dashbord.html",post=post)


    if request.method=="POST":
        username=request.form.get("uname")
        password=request.form.get("pass")
        if username=="sidd" and password=='123456':
            session['user']=username
            post=Posts.query.all()
            return render_template("dashbord.html",post=post)
    else:
        return render_template("login.html")
    
    

        
            


    
    
@app.route('/')
def home():
    post=Posts.query.filter_by().all()[0:5]
    return render_template("index.html",post=post)

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/edit/<string:sno>',methods=['GET','POST'])
def edit(sno):
    if ('user' in session and session['user']=='sidd'):
        if request.method=="POST":
            box_title=request.form.get("title")
            tline=request.form.get("tline")
            slug=request.form.get("slug")
            content=request.form.get("content")
            img_file=request.form.get("img_file")
            date=datetime.now()
            if sno=='0':
                post = Posts(title=box_title,tagline=tline,slug=slug,containt=content,img_file=img_file,date=date)
                db.session.add(post)
                db.session.commit()
                return render_template("edit.html",sno=sno,post=post)
            else:
                post=Posts.query.filter_by(sno=sno).first()
                post.title=box_title
                post.slug=slug
                post.tline=tline
                post.containt=content
                post.img_file=img_file
                post.date=date
                db.session.commit()
                return redirect("/edit/"+sno)
        post=Posts.query.filter_by(sno=sno).first()

        return render_template("edit.html",sno=sno,post=post)





@app.route('/contact',methods=['GET','POST'])
def contact():
    if request.method=='POST':
        name=request.form.get("name")
        email=request.form.get("email")
        Phno=request.form.get("Phno")
        mes=request.form.get("mes")
        entery=Contacts(name=name,email=email,phone_num=Phno,mes=mes)
        db.session.add(entery)
        db.session.commit()
        mail.send_message('New massage from'+name,sender=email,recipients=['parabsiddhesh60@gmail.com'],body= mes +"\n"+Phno)
    return render_template("contact.html")

@app.route('/post/<string:post_slug>',methods=['GET'])
def post(post_slug):
    post=Posts.query.filter_by(slug=post_slug).first()
    return render_template("post.html",post=post)
   

@app.route('/delete/<string:sno>',methods=['GET','POST'])
def delete(sno):
    if ('user' in session and session['user']=='sidd'):
        post=Posts.query.filter_by(sno=sno).first()
        db.session.delete(post)
        db.session.commit()
    return redirect("/dashbord")
@app.route('/logout')
def logout():
    session.pop('user')
    return redirect('/dashbord')

if __name__=="__main__":
    app.run(debug=True)