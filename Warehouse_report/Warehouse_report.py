import pandas as pd
import datetime
import smtplib

df=pd.read_excel("C:\\Users\\ariel\\OneDrive\\Área de Trabalho\\Sublime Files\\Projeto\\Warehouse_results.xlsx")

def get_assignments15min(df):

    assignments={}
    assignments_15min={}
       
    #create the users in assignments dictionary
    for user in df['Name']:
        if user not in assignments:
            assignments[user]={}
            assignments_15min[user]=[]
            #inserts the loads as a new dictionary inside each user
            for load in df.loc[df['Name']==user]['Load']:
                if load not in assignments[user]:
                    assignments[user][load]=[]
                    #insert the times fr pick and drop of each load in the dictionary
                    for date_time in df.loc[df['Load']==load]['Date_Time']:
                        assignments[user][load].append(date_time)
                    assignments[user][load].append(assignments[user][load][1]-assignments[user][load][0])
                    #assignments has user's names as key, loads as key to nested dict, [0] pick, [1] drop, [2] delta
                    if assignments[user][load][2]>datetime.timedelta(minutes=15):
                        for location in df.loc[(df['Load']==load) & (df['Date_Time']==assignments[user][load][0])]['Location']:
                            assignments_15min[user].append(str(assignments[user][load][0])+f' at Location: {location}')
    return assignments_15min
   
    #print(assignments)
    #print('Assignments>15min:','\n',assignments_15min,'\n')
 
def get_palput_palpick(df,stage,storage,prep):
    
    stage_positions=[]
    storage_positions=[]
    prep_positions=[]
    palpick={}
    palput={}
    
    #Defining the locations for each wh area
    for i in range(1,stage):
        stage_positions.append(i)
    
    for i in range(stage,storage):
        storage_positions.append(i)
        
    for i in range(storage,prep):
        prep_positions.append(i)
    
    #finding the total palpick and palput for each user
    for user in df['Name']:
        if user not in palpick:
            palpick[user]=[]
            palput[user]=[]
            for load in df.loc[(df['Name']==user) & (df['Movement_type']=='Drop') & (df['Location'].isin(storage_positions))]['Load']:
                palput[user].append(load)
            for load2 in df.loc[(df['Name']==user) & (df['Movement_type']=='Drop') & (df['Location'].isin(prep_positions))]['Load']:
                palpick[user].append(load2)
    return palput,palpick
    #ajustar unpacking da tuple return

#print('Palput','\n',palput,'\n')
#print('Palpick','\n',palpick,'\n')


def email():
    
    emails={'a.prado':'arielfprado96@gmail.com','t.quadros':'taise.squadros@gmail.com','p.pereira':'arielfprado96@gmail.com','h.galvao':'arielfprado96@gmail.com','c.henrique':'arielfprado96@gmail.com','v.oliveira':'vh_silverio@hotmail.com','m.vidal':'arielfprado96@gmail.com','b.silva':'arielfprado96@gmail.com','e.souza':'arielfprado96@gmail.com','b.miranda':'brunofelippemm@gmail.com'}
    #configuring the email
    
    x=datetime.datetime.now()
    yesterday=x-datetime.timedelta(days=1)
    yest_day=yesterday.strftime('%d')
    yest_month=yesterday.strftime('%m')
    yest_year=yesterday.strftime('%y')
    
    smtp_object=smtplib.SMTP('smtp.gmail.com',587)
    smtp_object.connect("smtp.gmail.com",587)
    smtp_object.ehlo()
    smtp_object.starttls()
    
    email=input("Email: ")
    password=input('Password: ')
    smtp_object.login(email,password)
    
    for person in emails:
        from_address=email
        to_address=emails[person]
        subject=f'Productivity result - {yest_day}/{yest_month}/{yest_year}'
        message=f"Results of {yest_day}/{yest_month}/{yest_year} from {person} are:\n\nAssignments>15min: {len(assignments_15min[person])}\n{assignments_15min[person]}\n\nPalput: {len(palput[person])}\n\nPalpick: {len(palpick[person])}"
        msg=f"Subject: {subject}\n\n{message}"
        
        smtp_object.sendmail(from_address,to_address,msg)
        #smtp_object.close()
        
def email_me():
    
    x=datetime.datetime.now()
    yesterday=x-datetime.timedelta(days=1)
    yest_day=yesterday.strftime('%d')
    yest_month=yesterday.strftime('%m')
    yest_year=yesterday.strftime('%y')
    
    smtp_object=smtplib.SMTP('smtp.gmail.com',587)
    smtp_object.connect("smtp.gmail.com",587)
    smtp_object.ehlo()
    smtp_object.starttls()
    
    email=input("Email: ")
    password=input('Password: ')
    smtp_object.login(email,password)
    
    from_address=email
    to_address=email
    subject=f'Productivity result - {yest_day}/{yest_month}/{yest_year}'
    message=f"Results of {yest_day}/{yest_month}/{yest_year} from a.prado are:\n\nAssignments>15min: {len(assignments_15min['a.prado'])}\n{assignments_15min['a.prado']}\n\nPalput: {len(palput['a.prado'])}\n\nPalpick: {len(palpick['a.prado'])}"
    msg=f"Subject: {subject}\n\n{message}"
    
    smtp_object.sendmail(from_address,to_address,msg)

assignments_15min=get_assignments15min(df)
palput,palpick=get_palput_palpick(df, 101, 301, 401)
email()





