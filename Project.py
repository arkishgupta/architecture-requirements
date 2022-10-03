import mysql.connector
import cv2
import numpy
import os
import datetime

def fingerprint():
    Name = input("Enter your name: ")
    #Assuming test_path to be input from fingerprint scanner
    test_path="C:\\Users\\ARKISH\\Documents\\12th Class\\Computer\\Project\\Test Fingerprint\\1.bmp"
    test = cv2.imread(test_path)
    test=cv2.resize(test,(0,0), fx=1, fy=1)
    cv2.imshow("Original", test)   
    cv2.waitKey(0) #waits for user to press a key(necessary to avoid shell from crashing)
    cv2.destroyAllWindows() #closing all open windows

    match_score=0
    filename=None
    image=None
    kp1,kp2,mp=None, None, None
    
    for file in [file for file in os.listdir("C:\\Users\\ARKISH\\Documents\\12th Class\\Computer\\Project\\Fingerprint")]:
        # Iterating through the fingerprint directory.
        fingerprint_image = cv2.imread("C:\\Users\\ARKISH\\Documents\\12th Class\\Computer\\Project\\Fingerprint\\"+file)
        #SIFT algorithm(Scale-Invariant Feature Transform) is an image descriptor for image-based matching. In this case, matching test fingerprint to one of database fingerprints. 
        sift = cv2.SIFT_create()
        keypoints_1, descriptors_1 = sift.detectAndCompute(test, None)
        keypoints_2, descriptors_2 = sift.detectAndCompute(fingerprint_image, None)
        #FlannBasedMatcher() method gives the no. of key matches.
        matches = cv2.FlannBasedMatcher(dict(algorithm=1, trees=10), dict()).knnMatch(descriptors_1, descriptors_2, k=2)
        match_points = []
        for p, q in matches:
            if p.distance < 0.1*q.distance:
                match_points.append(p)
        #To define key-point margins and display output by drawing matching key points. drawMatches() method has been used for this.       
        keypoint = 0
        if len(keypoints_1) < len(keypoints_2):
            keypoint = len(keypoints_1)            
        else:
            keypoint = len(keypoints_2)
            
        if (len(match_points) / keypoint * 100)> match_score:
            match_score = len(match_points)/keypoint * 100
            filename=file
            image=test
            kp1, kp2, mp= keypoints_1, keypoints_2, match_points
            result = cv2.drawMatches(test, kp1, fingerprint_image, kp2, mp, None)

    Best_Match= filename
    con=mysql.connector.connect(user="root", host="localhost", passwd="abcd")
    cur=con.cursor()
    cur.execute("use fingerprints")
    s="select Name from fingerprints where Filename=%s"
    cur.execute(s,(filename,))
    x=cur.fetchall() #Name is in form of a nested tuple
    x2=""
    for i in x:
        x2+=i[0]
    print("Match Score: " + str(match_score))
    if str(x2).upper()==Name.upper():
        print("User authorised")
        cv2.imshow("Result", result)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return "A"
    else:
        print("Access denied")

con=mysql.connector.connect(user="root", host="localhost", passwd="abcd")
if con.is_connected():
    print("Connected")
else:
    print("Not connected")
cur=con.cursor()

def remove_worker_status(): # To clear the status when expected arrival time meets current time.
    cur.execute("use architecture")
    cur.execute("select * from worker_status")
    x=cur.fetchall()
    s="delete from worker_status where Expected_arrival=%s"
    for i in x:
        date_object= datetime.datetime.strptime(str(i[5]), "%Y-%m-%d %H:%M:%S")
        if datetime.date.today() > date_object.date():
            cur.execute(s, (i[5],))
            con.commit()
            
remove_worker_status()

category=input("Enter W for worker, A for architect: ")

if category.upper()=="W":
    while True:
        id0=int(input("Enter Wid (Enter 0 if not known): "))
        cur.execute("use architecture")
        cur.execute("select * from Wid")
        x1=cur.fetchall()
        list_wid=[]
        for i in x1:
            list_wid.append(i[1])
        if id0 not in list_wid and id0!=0:
            print("\nCheck Wid")
            break
        if id0==0:
            a2=input("\nEnter your name: ")
            for i in x1:
                if i[0].lower()==a2.lower():
                    print("Wid:", i[1])
            break
        print("\nEnter 1 to input requirements\nEnter 2 to retrieve status\nEnter 3 to view Wid")
        choice=int(input(": "))
        if choice==1:
                cur.execute("use architecture")
                a1=id0
                b1=input("Enter material: ")
                c1=input("Enter amount: ")
                d1=input("Enter reason: ")
                s01="insert into worker_input values(%s, %s, %s, %s, now())"
                cur.execute(s01,(a1,b1,c1,d1))
                con.commit()
                s02="insert into architect_input(Wid, Material, Amount, Reason) values (%s, %s, %s, %s)"
                cur.execute(s02,(a1,b1,c1,d1))
                con.commit()
                print("\nSent requirements")
                
        elif choice==2:
            cur.execute("use architecture")
            s11="select * from worker_status where Wid=%s"
            cur.execute(s11, (id0,))
            x2=cur.fetchall()
            if len(x2)==0:
                print("No pending status")
            else:
                for i in x2:
                    print(i)

        elif choice==3:
            a3=input("\nEnter your name: ")
            for i in x1:
                if i[0].lower()==a3.lower():
                    print("Wid:", i[1])
        else:
            print("\nEnter again")         
                     
elif category.upper()=="A":
    a=fingerprint() # fingerprint() function returns “A” if user is authorized.
    if a=="A":
        while True:
            print("\nEnter 1 to retrieve requirements\nEnter 2 to update requirements\nEnter 3 to retrieve requirements log\nEnter 4 to add or remove worker\nEnter 5 to retrieve workers")
            choice=int(input(": "))
            if choice==1:
                cur.execute("use architecture")
                cur.execute("select * from worker_input")
                x1=cur.fetchall()
                for i in x1:
                    print(i)
                if len(x1)==0:
                    print("None")
            elif choice==2:
                cur.execute("use architecture")
                cur.execute("select * from worker_input")
                x2=cur.fetchall()
                s01="update architect_input set AcceptorRejectorRemarks=%s, Date_of_view=now(), Expected_arrival=%s where Wid=%s and Material=%s and Amount=%s"
                s02="insert into worker_status values(%s, %s, %s, %s, now(), %s)"
                s03="delete from worker_input where wid=%s and material=%s and amount=%s" 
                if len(x2)==0:
                    print("No requirement to update")
                else:
                    for i in x2:
                        print(i)
                        a1=input("\nEnter accept or reject or remarks: ")
                        a2=input("Enter expected_arrival in YYYY-MM-DD format: ")
                        y,m,d=map(int, a2.split("-"))
                        a3=datetime.date(y,m,d)
                        cur.execute(s01, (a1, a3, i[0], i[1], i[2]))
                        con.commit()
                        cur.execute(s02, (i[0], i[1], i[2], a1, a3))
                        con.commit()
                        cur.execute(s03, (i[0], i[1], i[2]))
                        con.commit()
                    print("Requirements have been updated")
            elif choice==3:
                cur.execute("select * from architect_input")
                x3=cur.fetchall()
                for i in x3:
                    print(i)
                if len(x3)==0:
                    print("None")
                print("\nEnd of logs")
            elif choice==4:
                print("\nEnter 1 to add worker\nEnter 2 to remove worker")
                a4=int(input(": "))
                cur.execute("use architecture")
                s11="insert into Wid values(%s,%s)"
                s12="delete from Wid where Wid=%s"
                n2=int(input("Enter no. of workers: "))
                if a4==1:
                    for i in range(1, n2+1):
                        cur.execute("select * from wid")
                        x4=cur.fetchall()
                        list_wid=[]
                        for j in x4:
                            list_wid.append(j[1])
                        list_wid.sort()
                        Wid=int(list_wid[-1])+1
                        name=input("Enter name "+ str(i)+ ": ")
                        cur.execute(s11,(name,Wid))
                        con.commit()
                    print("\nWorkers have been added")
                elif a4==2:
                    for i in range(1, n2+1):
                        Wid=input("Enter Wid "+ str(i)+ ": ")
                        cur.execute(s12, (Wid,))
                        con.commit()
                    print("\nWorkers have been removed")
                            
                else:
                    print("\nEnter again")
                    
            elif choice==5:
                cur.execute("select * from Wid")
                x5=cur.fetchall()
                for i in x5:
                    print(i)
                print("\nEnd of data")

            else:
                print("\nEnter again")

