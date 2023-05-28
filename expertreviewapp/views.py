from code import interact
from pyexpat import features
import re
from django.shortcuts import render
from django.http import HttpResponseRedirect
from datetime import date
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate
from django.contrib import messages
from .models import *
from datetime import datetime
from django.db.models import Q, Avg
# from torch import qr

#from sqlalchemy import engine_from_config
# Create your views here.

def mainhome(request):
   
    return render(request,"mainhome.html")

def login(request):
    msg=""
    if request.POST :
       
        uname=request.POST["t1"] 
        passw=request.POST["t2"] 
        user=authenticate(username=uname,password=passw)
        
        print(user)
        if user:
            userdata=CustomUser.objects.get(username=uname)
            if userdata.is_superuser == 1:
                    return redirect("/adminhome")
            elif userdata.usertype == "expert":
                    request.session["email"]=uname
                    r = Expert.objects.get(email=uname)
                    request.session["id"]=r.id
                    request.session["name"]=r.name
                    return redirect("/experthome")
            elif userdata.usertype == "customer":
                    request.session["email"]=uname
                    r = Registration.objects.get(email=uname)
                    request.session["id"]=r.id
                    request.session["name"]=r.name
                    return redirect("/cushome")
            else:
                    request.session["uname"]=uname
                    r = Company.objects.get(name=uname)
                    request.session["id"]=r.id
                    request.session["name"]=r.name
                    return redirect("/companyhome")

        
        else:
            messages.info(request,"User dosent exist")
       
            
    return render(request,"login.html",{"msg":msg})

def comviewvehicle(request):
    uid=request.session["id"]
    com=Company.objects.get(id=uid)
    data=Vehicle.objects.filter(cmp__id=uid)
    return render(request,"comvvehicle.html",{"data":data})

def companyhome(request):
    return render(request,"companyhome.html")


def cusreg(request):
    msg=""
    if request.POST :
        name=request.POST.get("t3")
       
        email=request.POST.get("t4")
        mob=request.POST.get("t5")
        
        passw=request.POST.get("t2")
        
        add=request.POST.get("house")
        user=Registration.objects.filter(email=email,psw=passw).exists()
        if user:
            messages.info(request,"User already exists")
        else:
            try:
                u=CustomUser.objects.create_user(username=email,email=email,password=passw,usertype="customer")
                u.save()
            except Exception as e:
                messages.info(request,e)
            else:
                try:
                    s=Registration.objects.create(name=name,con=mob,email=email,psw=passw,add=add,user=u)
                    s.save()
                except Exception as e:
                    messages.info(request,e)
                else:
                    messages.info(request,"Registered successfully")
    return render(request,"cusreg.html",{"msg":msg})

def expertreg(request):
    if request.POST :
        name=request.POST.get("t3")
        email=request.POST.get("t4")
        mob=request.POST.get("t5")
        exp=request.POST.get("t7")
        passw=request.POST.get("t2")
        user=Registration.objects.filter(email=email,psw=passw).exists()
        if user:
            messages.info(request,"User already exists")
        else:
            
            try:
                u=CustomUser.objects.create_user(username=email,email=email,password=passw,usertype="expert")
                u.save()
            except Exception as e:
                messages.info(request,e)
            else:
                try:
                    s=Expert.objects.create(name=name,con=mob,exp=exp,psw=passw,email=email,user=u)
                    s.save()
                except Exception as e:
                    messages.info(request,e)
                else:
                    messages.info(request,"Registered successfully")
    return render(request,"expertreg.html")


def addvehicle(request):
    
    data=Company.objects.all()
    dte=date.today()
    if request.POST :
        name=request.POST.get("t1")
        cid=request.POST.get("t2")
        cmp=Company.objects.get(id=cid)
        model=request.POST.get("t3")
        type=request.POST.get("t4")
        fuel=request.POST.get("t5")
        torque=request.POST.get("t6")
        hp=request.POST.get("t7")
        colors=request.POST.get("t8")
        price=request.POST.get("t9")
        ground=request.POST.get("t10")
        tyre=request.POST.get("t11")
        img=request.FILES.get("t12")
        # myfile=request.FILES.get("t12")
        user=Vehicle.objects.filter(name=name).exists()
        if user:
            messages.info(request,"Vehicle already exists")
        else:
            try:
                u=Vehicle.objects.create(name=name,cmp=cmp,model=model,type=type,fuel=fuel,torque=torque,hp=hp,colors=colors,price=price,groundcl=ground,tiresize=tyre,
                                         image=img,date=dte)
                u.save()
            except Exception as e:
                messages.info(request,e)
            else:
                messages.info(request,"Added Successfully")
    return render(request,"vehicle.html",{"data":data})

def company(request):
    msg=""
    if request.POST :
        name=request.POST.get("t1")
        con=request.POST["con"]
        myfile=request.FILES.get("file")

        user=Company.objects.filter(name=name).exists()
        if user:
            messages.info(request,"Company already exists")
        else:
            try:
                c=CustomUser.objects.create_user(username=name,password=con,usertype="company")
                c.save()
                
            except Exception as e:
                messages.info(request,e)
            else:
                try:
                    u=Company.objects.create(name=name,con=con,logo=myfile)
                    u.save()
                except Exception as e:
                    messages.info(request,e)
                else:

                    messages.info(request,"Added succesfully")
    data=Company.objects.all()
    return render(request,"company.html",{"msg":msg,"data":data})


def adminviewcus(request):
   
    data=Registration.objects.all()
    return render(request,"adminviewcus.html",{"data":data})


def adminviewexpert(request):
    
    data=Expert.objects.all()
    return render(request,"adminviewexpert.html",{"data":data})

def adminviewvehicle(request):
   
    data=Vehicle.objects.all()
    return render(request,"adminviewvehicle.html",{"data":data})




def adminreview(request):
    
    data=ExpertReview.objects.all()
    return render(request,"adminreview.html",{"data":data})


def adminreviewmore(request):
    rid=request.GET.get('id')
    
    data=ReviewChild.objects.filter(rid__id=rid)
    return render(request,"adminreviewmore.html",{"data":data,"rid":rid})

def adminupdatereview(request):
    rid=request.GET.get('id')
    e=ExpertReview.objects.get(id=rid)
    e.status="Approved"
    e.save()
    return redirect("/adminreview")

def adminhome(request):
    return render(request,"adminhome.html")

def deletevehicle(request):
    id=request.GET.get("id")
    v=Vehicle.objects.get(id=id).delete()
    return redirect("/adminviewvehicle")

def expertviewvehicle(request):
    
    data=Vehicle.objects.all()
    return render(request,"expertviewvehicle.html",{"data":data})

def expcardetails(request):
    cid=request.GET.get("id")
    
    car=Vehicle.objects.get(id=cid)
    return render(request,"expcardetails.html",{"d":car})

def expertreview(request):
    msg=""
    dte=date.today()
    datas=Question.objects.all()
    vid=request.GET.get("id")
    v=Vehicle.objects.get(id=vid)
    
    uid=request.session["id"]
    e=Expert.objects.get(id=uid)
    rev=ExpertReview.objects.filter(Q(exp=e) & Q(vid__id=vid))
    for r in rev:
        print(r.review)
    if rev is None:
        msg="Review already added"
    else:
        
        datas=Question.objects.all()

        if request.POST :
            buy=request.POST.get("txtBuy")
            avoid=request.POST.get("txtAvoid")
            review=request.POST.get("txtOverall")
            rating=request.POST.get("rating")


            r=ExpertReview.objects.create(review=review,rating=rating,whybuy=buy,whyavoid=avoid,status="Submitted",date=dte,vid=v,exp=e)
            r.save()
            for d in datas:
                ans = request.POST[f'ans{d.id}']
                rating = request.POST[f'point{d.id}']
                rc=ReviewChild.objects.create(rid=r,q=d,a=ans,rating=rating)
                rc.save()
           
            msg="Review added"

    return render(request,"expertreview.html",{"msg":msg,"datas":datas})



def experthome(request):
    return render(request,"experthome.html")

def expertviewreviews(request):
    uname=request.session["id"]
    
    data=ExpertReview.objects.filter(exp__id=uname)
    return render(request,"expertviewreviews.html",{"data":data})

def custviewvehicle(request):
   
    data=Vehicle.objects.all()
    return render(request,"custviewvehicle.html",{"data":data})
    


def cusviewreviews(request):
    
    qry="select ev.reviewid,ev.review,ev.rating,ex.name,ex.mob,ex.email,vh.id,vh.name from expertreview ev join expert ex on(ev.exp_id=ex.id) join vehicle vh on(vh.id=ev.vid) where ev.status='Approved'"

    # c.execute(qry)
    # data=c.fetchall()
    return render(request,"cusviewviewreviews.html")

def cushome(request):
    return render(request,"cushome.html")

def custcardetails(request):
    engine1=""
    ride1=""
    interior1=""
    feature1=""
    cid=request.GET.get("id")
    car=Vehicle.objects.get(id=cid)
    uname=request.session["email"]
    

   
    count=ExpertReview.objects.filter(vid__id=cid).count()
    d=ExpertReview.objects.filter(vid__id=cid)
    rev=ReviewChild.objects.filter(rid__vid__id=cid)
    score=0
    engine=""
    ride=""
    interior=""
    feature=""
    if count > 0:
        score=generate_data(cid)
        print("Score **************(*&(*&(*&)))")
        print(score)

        # engine=ReviewChild.objects.filter()


    # qry="select count(*)  from reviewchild where reviewid in(select reviewid from expertreview where vid='"+str(cid)+"')"
    # c.execute(qry)
    # d=c.fetchone()
    # count= ReviewChild.objects.filter(rid__vid__id=cid).count()
    # score=0
    # engine=""
    # ride=""
    # interior=""
    # feature=""
    # if d:
    #     score=generate_data(cid)
    #     print(score)

        

        engine=ReviewChild.objects.filter(q__q='Engine and Performance',rid__vid__id=cid).aggregate(Avg('rating'))

        ride=ReviewChild.objects.filter(q__q='Ride and handling',rid__vid__id=cid).aggregate(Avg('rating'))

        interior=ReviewChild.objects.filter(q__q='Interior space and comfort',rid__vid__id=cid).aggregate(Avg('rating'))

        feature=ReviewChild.objects.filter(q__q='Features and equipment',rid__vid__id=cid).aggregate(Avg('rating'))
        print("*******************")
        
        # print(ride['rating__avg'])
        # print(interior['rating__avg'])
        # print(feature['rating__avg'])
        ride1=ride['rating__avg']
        engine1=engine['rating__avg']
        interior1=interior['rating__avg']
        feature1=feature['rating__avg']
        print("*************SCORE**************")
        print(score[2])
        a=score[0]
        b=score[1]

    return render(request,"custcardetails.html",{"d":car,"count":count,"rev":rev, "data":d,"engine":engine1,"ride":ride1,"interior":interior1,"feature":feature1,"score":score,"a":a,"b":b})

def generate_data(vid):
    import pymysql
    import csv
    import sys

   

    # sql = "SELECT review from expertreview where vid='"+str(vid)+"' and status='Approved' UNION SELECT answer from reviewchild where reviewid in (SELECT reviewid from expertreview where vid='"+str(vid)+"')"
    sql=ExpertReview.objects.filter(vid__id=vid)

    csv_file_path = 'expertreviewapp/static/data/dataset.csv'

    try:
        # cur.execute(sql)
        rows = ExpertReview.objects.filter(vid__id=vid)
    except:
        pass
# Continue only if there are rows returned.
    if rows:
    # New empty list called 'result'. This will be written to a file.
        result = list()
       
        print("rows *****************")
        print(rows)

    # The row name is the first entry for each entity in the description tuple.
        column_names = list()
       
        for i in rows:
            column_names.append(i.review)

        result.append(column_names)
        print("columns **********************")
        print(column_names)
        print("result *****************")
        print(result)
        for row in rows:
            result.append(row.rating)
        print("result *****************")
        print(result)
        res=result
        print(res)

    # Write result to file.
        with open(csv_file_path, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for row in result:
                csvwriter.writerow(row)
    else:
        sys.exit("No rows found for query: {}".format(sql))
    score=analyse(res)
    return score

def analyse(res):
    import csv
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    import pandas as pd
    import re
    analyser = SentimentIntensityAnalyzer()
    # print(analyser)
    def print_sentiment_scores():
        lst=[]
        dataset = pd.read_csv('expertreviewapp/static/data/dataset.csv', delimiter = ',')
        f=open('expertreviewapp/static/data/dataset.csv')
        reader=csv.reader(f)
        lines=len(list(reader))
        print(lines)
        corpus = []
        corpusn = []
        print("dataset")
        
    
        cnt=0
        cntn=0
        print("kkkkkkkkkkkkkkkkkkkkkkkkkkkk")
        pos=0
        neg=0
        neu=0
        review=''
        for i in res[0]:  
            # review = re.sub('[^a-zA-Z0-1]', ' ', dataset['review'][i])
            review=i
            cor=0
           
            vadersenti = analyser.polarity_scores(review)
            if vadersenti["compound"] >= 0.5:
                    pos=pos+1
            elif vadersenti["compound"] <= -0.5:
                    neg=neg+1
            else:
                    neu=neu+1
            
            print(i)
            print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
            print(vadersenti)
            cnt=cnt+vadersenti['pos']
            cntn=cntn+vadersenti['neg']
            corpus.append(cnt)
            corpusn.append(cntn)
        score=[]
        score.append(pos)
        score.append(neg)
        score.append(neu)

        print("Scores")
        print("************************")
        print("Pos=",pos)
        print("Neg=",neg)
        print("Neu=",neu)
        print("************************")
        corpus.append(cnt)
        corpusn.append(cntn)

        lst.append(corpus)
        lst.append(corpusn)
        print(score)
        return(score)

        
    
    score=print_sentiment_scores()
    return score


def req(request):
    id=request.GET.get("id")
    uid=request.session["id"]
    ex=Expert.objects.get(id=id)
    user=Registration.objects.get(id=uid)
    status="Requested"
    r=Request.objects.create(user=user,exp=ex,status=status)
    r.save()
    return redirect("/cushome")


def expapp(request):
    id=request.GET.get("id")
    data=Request.objects.get(id=id)
    data.status="Approved"
    data.save()
    return redirect("/expertvreq")

def exprem(request):
    id=request.GET.get("id")
    data=Request.objects.get(id=id).delete()
    return redirect("/expertvreq")

def expertvreq(request):
    eid=request.session["id"]
    data=Request.objects.filter(exp__id=eid)
    return render(request,"expertvreq.html",{"data":data})

def expertprofile(request):
    uid=request.session["id"]
    data=Expert.objects.get(id=uid)
    if request.POST :
        name=request.POST.get("t3")
        email=request.POST.get("t4")
        mob=request.POST.get("t5")
        # exp=request.POST.get("t6")
        area=request.POST.get("t7")
        data.name=name
        data.email=email
        data.con=mob
        data.exp=area
        data.save()
        messages.info(request,"Updated")
        
    
    return render(request,"expertprofile.html",{"d":data})


def cusprofile(request):
    uid=request.session["id"]
    msg=""
    data=Registration.objects.get(id=uid)
    
    if request.POST :
        name=request.POST.get("t3")
        
        email=request.POST.get("t4")
        mob=request.POST.get("t5")
       
     
        add=request.POST.get("pin")
        data.name=name
        data.email=email
        data.con=mob
        data.add=add
        data.save()
        messages.info(request,"Updated")

     
   
    return render(request,"cusprofile.html",{"msg":msg,"d":data})



def cusvreq(request):
    eid=request.session["id"]
    data=Request.objects.filter(user__id=eid)
    return render(request,"cusvreq.html",{"data":data})



def inchat(request):
    sender = request.session['email']
    # receiver = request.GET.get("email")
    receiver=request.GET.get("email")
    print(receiver)
    print(sender)
    dates=date.today()
    if request.POST:
        msg=request.POST["msg"]
        c=Chat.objects.create(sender=sender,receiver=receiver,date=dates,message=msg)
        c.save()
    #     msg = request.POST['msg']
    #     qry = f"INSERT INTO `chat` (`sender`,`receiver`,`message`,`date`) VALUES('{sender}','{receiver}','{msg}',(select sysdate()))"
    #     c.execute(qry)
    #     db.commit()
    # qryChat = f"SELECT * FROM chat WHERE sender='{sender}' AND receiver='{receiver}' UNION SELECT * FROM chat WHERE receiver='{sender}' AND sender='{receiver}' ORDER BY `chatid`"
    # c.execute(qryChat)
    # messages = c.fetchall()  
    r=Chat.objects.all()
    return render(request,"inchat.html",{"messages":r,"sender":sender, "receiver": receiver}  )



def sfChatPer(request):
    sender = request.session['email']
    receiver = request.GET['email']
    dates=date.today()
    if request.POST:
        msg=request.POST["msg"]
        c=Chat.objects.create(sender=sender,receiver=receiver,date=dates,message=msg)
        c.save()
    #     msg = request.POST['msg']
    #     qry = f"INSERT INTO `chat` (`sender`,`receiver`,`message`,`date`) VALUES('{sender}','{receiver}','{msg}',(select sysdate()))"
    #     c.execute(qry)
    #     db.commit()
    # qryChat = f"SELECT * FROM chat WHERE sender='{sender}' AND receiver='{receiver}' UNION SELECT * FROM chat WHERE receiver='{sender}' AND sender='{receiver}' ORDER BY `chatid`"
    # c.execute(qryChat)
    # messages = c.fetchall()
    r=Chat.objects.all()
    # for i in  r:

    return render(request, "sfChatPer.html", {"messages":r,"sender":sender, "receiver": receiver})  



