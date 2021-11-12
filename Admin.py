#import libraries
import pandas as pd
import os
import numpy as np
import re
import datetime as dt
from datetime import datetime as dt2

#Says what's included in each kit based off the timepoint number
def kittype(x):
    out = []
    for i in range(len(x)):
        if x[i] == 1:
            out.append('faeces, urine, hair, mouth')
        elif x[i] == 2:
            out.append('faeces, skin')
        elif x[i] == 3:
            out.append('faeces, urine, hair, mouth, skin')
        elif x[i] == 4:
            out.append('faeces, urine, hair, skin')
        elif x[i] == 5:
            out.append('faeces, urine, hair, skin')
        elif x[i] == 6:
            out.append('faeces, urine, hair, skin')
        elif x[i] == 7:
            out.append('faeces, urine, hair')
    return out

#Creates bar code from dogid and timepoint number
def barcode(x, y):
    out = []
    for i in range(len(x)):
        out.append(str(x[i])+"-"+str(int(y[i])))
    return out

#Assigns numerical value to each sample based off permisions in master (0 for permision given)
def faeces(x):
    out = []
    for i in x:
        if i == 'Y':
            out.append(1)
        else:
            out.append(0)
    return out
def urine(x):
    out = []
    for i in x:
        if i == 'Y':
            out.append(2)
        else:
            out.append(0)
    return out
def hair(x):
    out = []
    for i in x:
        if i == 'Y':
            out.append(5)
        else:
            out.append(0)
    return out
def mouth(x):
    out = []
    for i in x:
        if i == 'Y':
            out.append(10)
        else:
            out.append(0)
    return out
def skin(x):
    out = []
    for i in x:
        if i == 'Y':
            out.append(20)
        else:
            out.append(0)
    return out

#Say whether a certain type of sample is required based on premisions from master
def faeces_inc(x):
    out = []
    for i in x:
        if i == 1:
            out.append('Yes')
        else:
            out.append('No')
    return out
def urine_inc(x):
    out = []
    for i in x:
        if i == 2:
            out.append('Yes')
        else:
            out.append('No')
    return out
def hair_inc(x):
    out = []
    for i in x:
        if i == 5:
            out.append('Yes')
        else:
            out.append('No')
    return out
def mouth_inc(x):
    out = []
    for i in x:
        if i == 10:
            out.append('Yes')
        else:
            out.append('No')
    return out
def skin_inc(x):
    out = []
    for i in x:
        if i == 20:
            out.append('Yes')
        else:
            out.append('No')
    return out

#Say which label to attach to kit based on samples included
def Normal_Label(x, y):
    out = []
    for i in range(len(x)):
        if x[i] + y[i] == 1:
            out.append(1)
        elif x[i] + y[i] == 2:
            out.append(1)
        elif x[i] + y[i] == 3:
            out.append(2)
        else:
            out.append(0)
    return out
def Freezer_Label(x):
    out = []
    for i in range(len(x)):
        if x[i] > 0:
            out.append(1)
        else:
            out.append(0)
    return out
def Biohazard_Label(x, y, z, a):
    out = []
    for i in range(len(x)):
        if x[i] + y[i] + z[i] + a[i] > 0:
            out.append(1)
        else:
            out.append(0)
    return out

#Creates a list of 1's the length of each df at a given time point.
# Compresension list used to turn this in to the timpoint number later on
def sample_point(x):
    out = []
    for i in range(len(x)):
        out.append(1)
    return out

#reates a list of 0's the length of each df at a given time point if a sample isn't sent at that timepoint
def no_sample_at_timepoint(x):
    out = []
    for i in range(len(x)):
        out.append(0)
    return out

#Check CIC returned samples sheet to see if a sample has been previously sent out
def prev_samp_sent_out(samp_to_send, sent_samp):
    prev_samp_out = []
    for i in samp_to_send:
        if i in sent_samp:
            prev_samp_out.append(i)
        else:
            prev_samp_out.append("")
    return prev_samp_out

#Filters out any dogs from master that either don't require samples to be sent
def send_pack_check(df, col_name):
    idx = df.index
    drop_lst = []
    for i in range(len(df)):
        sent = df.iloc[i][col_name]
        if len(re.findall('emailed', str(sent))) > 0:
            drop_lst.append(idx[i])
        elif len(re.findall('no samples', str(sent))) > 0:
            drop_lst.append(idx[i])
        elif len(re.findall('No kit consent', str(sent))) > 0:
            drop_lst.append(idx[i])
        else:
            continue

    for j in drop_lst:
        df.drop(j, inplace=True)
    return df

#Remove any dogs where no samples need to be sent from sampling pakc sheet
def no_samples_drop_sp(df, a, b, c, d, e):
    idx = df.index
    drop_lst = []
    for i in range(len(idx)):
        if df.iloc[i][a] + df.iloc[i][b] + df.iloc[i][c] + df.iloc[i][d] + df.iloc[i][e] == 0:
            drop_lst.append(idx[i])

    for j in drop_lst:
        df.drop(j, inplace=True)
    return df

#Function to do early filtering
def col_drop(df, col_name, phrases):
    idx = df.index
    drop_lst = []
    for i in range((len(idx))):
        for phrase in phrases:
            try:
                if len(re.findall(phrase, (df_ad.iloc[i][col_name].lower())))>0:
                    drop_lst.append(i)
            except:
                continue
    for j in drop_lst:
        df.drop(j, inplace=True)
    return df.reset_index(drop=True)

#Functions to calculate the age of a dog in days
def age_days(df):
    dobs = (df["DoB"].tolist())
    today = dt2.today().strftime('%Y-%m-%d %H:%M:%S')
    today_obj = dt2.strptime(today, '%Y-%m-%d %H:%M:%S')
    age_days = []
    for date_str in dobs:
        if type(date_str) == str:
            dt_obj = dt2.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            age_days.append(int((today_obj - dt_obj).days))
        else:
            age_days.append(0)

    df['age in days today'] = age_days
    return df

#File Paths
Drive = 'C:\\'
admin = os.path.join(Drive, 'Python', 'Sampling Pack', 'Input', 'New Master v1077_trim uploaded by BR_copy.xlsx')
ret_samp = os.path.join(Drive, 'Python', 'Sampling Pack', 'Input', '27.10.21 RK GenPup Returned Samples Sheet for CIC 04NOV21 updated by SM.xlsx')
output_admin = os.path.join(Drive, 'Python', 'Sampling Pack', 'Output', 'Admin')
output_samp = os.path.join(Drive, 'Python', 'Sampling Pack', 'Output', 'Sampling Pack')
#date and time
now = dt2.now()
dt_string = now.strftime("%Y%m%d%H%M")

#Create dataframes ffrom admin and returned samples sheets
df_ad = pd.read_excel(admin)
df_rs = pd.read_excel(ret_samp)

#Specify drop conditions for ‘newPuppy’ column
col_A = ['handover', 'test', 'duplicate', 'error']

#Specify drop conditions for ‘Dog has left study’ column
col_H = ['archived']

#Specify drop conditions for ‘DogID’ column
col_C = ['anon1', 'anon2']

#Specify drop conditions for 'GenPup team notes' column
col_DR = ['republic of ireland']

#Update Ages in Days
df_ad = age_days(df_ad)

#Check age in days against permisons for sampling packs to check if a pack needs to be sent at this time point
df_ad.loc[(df_ad['age in days today'] >= 170) & (df_ad['age in days today'] < 188) & (df_ad['sample_faeces'] == 'N') & (df_ad['sample_skin'] == 'N') , """SIX MONTHS Sampling kit sent if required

(NO KIT CONSENT MARKED BUT PLEASE DOUBLE CHECK OWNER HAS NOT CHANGED THEIR CONSENT)"""] = 'no samples needed'

df_ad.loc[(df_ad['age in days today'] >= 355) & (df_ad['age in days today'] < 373) & (df_ad['sample_faeces'] == 'N') & (df_ad['sample_urine'] == 'N') & (df_ad['sample_hair'] == 'N') & (df_ad['sample_mouth'] == 'N') & (df_ad['sample_skin'] == 'N'), """12M Sampling kit SENT if required 

(NO KIT CONSENT MARKED BUT PLEASE DOUBLE CHECK OWNER HAS NOT CHANGED THEIR CONSENT)"""] = 'no samples needed'

df_ad.loc[(df_ad['age in days today'] >= 720) & (df_ad['age in days today'] < 738) & (df_ad['sample_faeces'] == 'N') & (df_ad['sample_urine'] == 'N') & (df_ad['sample_hair'] == 'N') & (df_ad['sample_skin'] == 'N'), """TWO YEAR Sampling kit sent if required

(NO KIT CONSENT MARKED BUT PLEASE DOUBLE CHECK OWNER HAS NOT CHANGED THEIR CONSENT)"""] = 'no samples needed'

df_ad.loc[(df_ad['age in days today'] >= 1085) & (df_ad['age in days today'] < 1103) & (df_ad['sample_faeces'] == 'N') & (df_ad['sample_urine'] == 'N') & (df_ad['sample_hair'] == 'N') & (df_ad['sample_skin'] == 'N'), """THREE YEAR Sampling kit sent if required

(NO KIT CONSENT MARKED BUT PLEASE DOUBLE CHECK OWNER HAS NOT CHANGED THEIR CONSENT)"""] = 'no samples needed'

df_ad.loc[(df_ad['age in days today'] >= 1450) & (df_ad['age in days today'] < 1468) & (df_ad['sample_faeces'] == 'N') & (df_ad['sample_urine'] == 'N') & (df_ad['sample_hair'] == 'N') & (df_ad['sample_skin'] == 'N'), """FOUR YEAR Sampling kit sent if required

(NO KIT CONSENT MARKED BUT PLEASE DOUBLE CHECK OWNER HAS NOT CHANGED THEIR CONSENT)"""] = 'no samples needed'

df_ad.loc[(df_ad['age in days today'] >= 1815) & (df_ad['age in days today'] < 1833) & (df_ad['sample_faeces'] == 'N') & (df_ad['sample_urine'] == 'N') & (df_ad['sample_hair'] == 'N'), """FIVE YEAR Sampling kit sent if required

(NO KIT CONSENT MARKED BUT PLEASE DOUBLE CHECK OWNER HAS NOT CHANGED THEIR CONSENT)"""] = 'no samples needed'

#Remove rows with values specified in DogID column
df_ad2 = col_drop(df_ad, 'DogId', col_C)
df_ad2.dropna(subset=['DogId'], inplace=True)

#Remove all rows with dog from Republic of Ireland
df_ad2 = col_drop(df_ad2, 'Country', col_DR)

#Remove rows with values specified in Dog has left study column
df_ad2 = col_drop(df_ad2, 'Dog has left study', col_H)

#Remove rows with values specified in newPuppy column
df_ad2 = col_drop(df_ad2, 'newPuppy', col_A)

#Filter for just puppies at the time point 12-16 weeks for puppies with # as the date the sample pack was sent
df_ad_12_16 = df_ad2[df_ad2['DATE SAMPLE PACK SENT PUPPY'].isin(['#'])]

#Check to see if kit is required at 6 month time point
df_ad_6M = df_ad2[df_ad2['SIX MONTHS sampling kit required (implemented 11/03/2019)'].isin([' send 6 MONTH kit now'])]

df_ad_6M = send_pack_check(df_ad_6M, """SIX MONTHS Sampling kit sent if required

(NO KIT CONSENT MARKED BUT PLEASE DOUBLE CHECK OWNER HAS NOT CHANGED THEIR CONSENT)""")

#Check to see if kit is required at 12 month time point
df_ad_12M = df_ad2[df_ad2['12-month sampling kit required'].isin(['send 12M kit now'])]

df_ad_12M = send_pack_check(df_ad_12M, """12M Sampling kit SENT if required 

(NO KIT CONSENT MARKED BUT PLEASE DOUBLE CHECK OWNER HAS NOT CHANGED THEIR CONSENT)""")

#Check to see if kit is required at 2 year time point
df_ad_2Y = df_ad2[df_ad2['TWO YEAR sampling kit required (implemented 11/03/2019)'].isin([' send 2YR kit now'])]

df_ad_2Y = send_pack_check(df_ad_2Y, """TWO YEAR Sampling kit sent if required

(NO KIT CONSENT MARKED BUT PLEASE DOUBLE CHECK OWNER HAS NOT CHANGED THEIR CONSENT)""")

#Check to see if kit is required at 3 year time point
df_ad_3Y = df_ad2[df_ad2['THREE YEAR sampling kit required (implemented 11/03/2019)'].isin([' send 3YR kit now'])]

df_ad_3Y = send_pack_check(df_ad_3Y, """THREE YEAR Sampling kit sent if required

(NO KIT CONSENT MARKED BUT PLEASE DOUBLE CHECK OWNER HAS NOT CHANGED THEIR CONSENT)""")

#Check to see if kit is required at 4 year time point
df_ad_4Y = df_ad2[df_ad2['FOUR YEAR sampling kit required (implemented …...)'].isin([' send 4YR kit now'])]

df_ad_4Y = send_pack_check(df_ad_4Y, """FOUR YEAR Sampling kit sent if required

(NO KIT CONSENT MARKED BUT PLEASE DOUBLE CHECK OWNER HAS NOT CHANGED THEIR CONSENT)""")

#Check to see if kit is required at 5 year time point
df_ad_5Y = df_ad2[df_ad2['FIVE YEAR sampling kit required (implemented …...)'].isin([' send 5YR kit now'])]

df_ad_5Y = send_pack_check(df_ad_5Y, """FIVE YEAR Sampling kit sent if required

(NO KIT CONSENT MARKED BUT PLEASE DOUBLE CHECK OWNER HAS NOT CHANGED THEIR CONSENT)""")

#Turn all values to go into sampling pack dataframe into columns
#12-16 Weeks
dogid_1216 = df_ad_12_16["DogId"].tolist()
userid_1216 = df_ad_12_16['userid'].tolist()
DogName_1216 = df_ad_12_16["Dog name"].tolist()
prefix_1216 = df_ad_12_16["prefix"].tolist()
firstName_1216 = df_ad_12_16["firstName"].tolist()
lastName_1216 = df_ad_12_16["lastName"].tolist()
email_1216 = df_ad_12_16["Email"].tolist()
samplingpoint_1216 = sample_point(dogid_1216)
FAECES_1216 = df_ad_12_16["sample_faeces"].tolist()
URINE_1216 = df_ad_12_16["sample_urine"].tolist()
HAIR_1216 = df_ad_12_16["sample_hair"].tolist()
MOUTH_1216 = df_ad_12_16["sample_mouth"].tolist()
SKIN_1216 = no_sample_at_timepoint(dogid_1216)
#6 Months
dogid_6M = df_ad_6M["DogId"].tolist()
userid_6M = df_ad_6M['userid'].tolist()
DogName_6M = df_ad_6M["Dog name"].tolist()
prefix_6M = df_ad_6M["prefix"].tolist()
firstName_6M = df_ad_6M["firstName"].tolist()
lastName_6M = df_ad_6M["lastName"].tolist()
email_6M = df_ad_6M["Email"].tolist()
samplingpoint_6M = [2 * x for x in sample_point(dogid_6M)]
FAECES_6M = df_ad_6M["sample_faeces"].tolist()
URINE_6M = no_sample_at_timepoint(dogid_6M)
HAIR_6M = no_sample_at_timepoint(dogid_6M)
MOUTH_6M = no_sample_at_timepoint(dogid_6M)
SKIN_6M = df_ad_6M["sample_skin"].tolist()
#12 Months
dogid_12M = df_ad_12M["DogId"].tolist()
userid_12M = df_ad_12M['userid'].tolist()
DogName_12M = df_ad_12M["Dog name"].tolist()
prefix_12M = df_ad_12M["prefix"].tolist()
firstName_12M = df_ad_12M["firstName"].tolist()
lastName_12M = df_ad_12M["lastName"].tolist()
email_12M = df_ad_12M["Email"].tolist()
samplingpoint_12M = [3 * x for x in sample_point(dogid_12M)]
FAECES_12M = df_ad_12M["sample_faeces"].tolist()
URINE_12M = df_ad_12M["sample_urine"].tolist()
HAIR_12M = df_ad_12M["sample_hair"].tolist()
MOUTH_12M = df_ad_12M["sample_mouth"].tolist()
SKIN_12M = df_ad_12M["sample_skin"].tolist()

#2 Years
dogid_2Y = df_ad_2Y["DogId"].tolist()
userid_2Y = df_ad_2Y['userid'].tolist()
DogName_2Y = df_ad_2Y["Dog name"].tolist()
prefix_2Y = df_ad_2Y["prefix"].tolist()
firstName_2Y = df_ad_2Y["firstName"].tolist()
lastName_2Y = df_ad_2Y["lastName"].tolist()
email_2Y = df_ad_2Y["Email"].tolist()
samplingpoint_2Y = [4 * x for x in sample_point(dogid_2Y)]
FAECES_2Y = df_ad_2Y["sample_faeces"].tolist()
URINE_2Y = df_ad_2Y["sample_urine"].tolist()
HAIR_2Y = df_ad_2Y["sample_hair"].tolist()
MOUTH_2Y = no_sample_at_timepoint(dogid_2Y)
SKIN_2Y = df_ad_2Y["sample_skin"].tolist()
#3 Years
dogid_3Y = df_ad_3Y["DogId"].tolist()
userid_3Y = df_ad_3Y['userid'].tolist()
DogName_3Y = df_ad_3Y["Dog name"].tolist()
prefix_3Y = df_ad_3Y["prefix"].tolist()
firstName_3Y = df_ad_3Y["firstName"].tolist()
lastName_3Y = df_ad_3Y["lastName"].tolist()
email_3Y = df_ad_3Y["Email"].tolist()
samplingpoint_3Y = [5 * x for x in sample_point(dogid_3Y)]
FAECES_3Y = df_ad_3Y["sample_faeces"].tolist()
URINE_3Y = df_ad_3Y["sample_urine"].tolist()
HAIR_3Y = df_ad_3Y["sample_hair"].tolist()
MOUTH_3Y = no_sample_at_timepoint(dogid_3Y)
SKIN_3Y = df_ad_3Y["sample_skin"].tolist()
#4 Years
dogid_4Y = df_ad_4Y["DogId"].tolist()
userid_4Y = df_ad_4Y['userid'].tolist()
DogName_4Y = df_ad_4Y["Dog name"].tolist()
prefix_4Y = df_ad_4Y["prefix"].tolist()
firstName_4Y = df_ad_4Y["firstName"].tolist()
lastName_4Y = df_ad_4Y["lastName"].tolist()
email_4Y = df_ad_4Y["Email"].tolist()
samplingpoint_4Y = [6 * x for x in sample_point(dogid_4Y)]
FAECES_4Y = df_ad_4Y["sample_faeces"].tolist()
URINE_4Y = df_ad_4Y["sample_urine"].tolist()
HAIR_4Y = df_ad_4Y["sample_hair"].tolist()
MOUTH_4Y = no_sample_at_timepoint(dogid_4Y)
SKIN_4Y = df_ad_4Y["sample_skin"].tolist()
#5 Years
dogid_5Y = df_ad_5Y["DogId"].tolist()
userid_5Y = df_ad_5Y['userid'].tolist()
DogName_5Y = df_ad_5Y["Dog name"].tolist()
prefix_5Y = df_ad_5Y["prefix"].tolist()
firstName_5Y = df_ad_5Y["firstName"].tolist()
lastName_5Y = df_ad_5Y["lastName"].tolist()
email_5Y = df_ad_5Y["Email"].tolist()
samplingpoint_5Y = [7 * x for x in sample_point(dogid_5Y)]
FAECES_5Y = df_ad_5Y["sample_faeces"].tolist()
URINE_5Y = df_ad_5Y["sample_urine"].tolist()
HAIR_5Y = df_ad_5Y["sample_hair"].tolist()
MOUTH_5Y = no_sample_at_timepoint(dogid_5Y)
SKIN_5Y = no_sample_at_timepoint(dogid_5Y)

#Concatenate all the columns for each value
dogid = dogid_1216 + dogid_6M + dogid_12M + dogid_2Y + dogid_3Y + dogid_4Y + dogid_5Y
userid = userid_1216 + userid_6M + userid_12M + userid_2Y + userid_3Y + userid_4Y + userid_5Y
DogName = DogName_1216 + DogName_6M + DogName_12M + DogName_2Y + DogName_3Y + DogName_4Y + DogName_5Y
prefix = prefix_1216 + prefix_6M + prefix_12M + prefix_2Y + prefix_3Y + prefix_4Y + prefix_5Y
firstName = firstName_1216 + firstName_6M + firstName_12M + firstName_2Y + firstName_3Y + firstName_4Y + firstName_5Y
lastName = lastName_1216 + lastName_6M + lastName_12M + lastName_2Y + lastName_3Y + lastName_4Y + lastName_5Y
email = email_1216 + email_6M + email_12M + email_2Y + email_3Y + email_4Y + email_5Y
samplingpoint = samplingpoint_1216 + samplingpoint_6M + samplingpoint_12M + samplingpoint_2Y + samplingpoint_3Y + samplingpoint_4Y + samplingpoint_5Y
FAECES = faeces(FAECES_1216) + faeces(FAECES_6M) + faeces(FAECES_12M) + faeces(FAECES_2Y) + faeces(FAECES_3Y) + faeces(FAECES_4Y) + faeces(FAECES_5Y)
URINE = urine(URINE_1216) + urine(URINE_6M) + urine(URINE_12M) + urine(URINE_2Y) + urine(URINE_3Y) + urine(URINE_4Y) + urine(URINE_5Y)
HAIR = hair(HAIR_1216) + hair(HAIR_6M) + hair(HAIR_12M) + hair(HAIR_2Y) + hair(HAIR_3Y) + hair(HAIR_4Y) + hair(HAIR_5Y)
MOUTH = mouth(MOUTH_1216) + mouth(MOUTH_6M) + mouth(MOUTH_12M) + mouth(MOUTH_2Y) + mouth(MOUTH_3Y) + mouth(MOUTH_4Y) + mouth(MOUTH_5Y)
SKIN = skin(SKIN_1216) + skin(SKIN_6M) + skin(SKIN_12M) + skin(SKIN_2Y) + skin(SKIN_3Y) + skin(SKIN_4Y) + skin(SKIN_5Y)

#Sent Sampling Packs
sp_out = df_rs["Sampling pack out"].tolist()

#Create sampling packs dataframe
df_sp = pd.DataFrame({"Kit Type (no blank rows)":kittype(samplingpoint), "VALUE OF BARCODE FOR VLOOKUP": barcode(dogid, samplingpoint),
                      'dogid':dogid, 'userid':userid, 'Dog Name':DogName,  "Sampling point (1=12-16w, 2=6m, 3=12m, 4=2y, 5=3y)": samplingpoint,
                      'FAECES':FAECES, 'URINE':URINE, 'HAIR':HAIR, 'MOUTH':MOUTH, 'SKIN':SKIN,
                      "NORMAL LABEL": Normal_Label(FAECES, URINE), "Freezer LABEL": Freezer_Label(SKIN),
                      "Biohazard LABEL": Biohazard_Label(FAECES, URINE, MOUTH, SKIN),
                     'prefix':prefix, 'firstName':firstName, 'lastName':lastName, 'email': email,
                      'faeces_included':faeces_inc(FAECES), 'urine_included':urine_inc(URINE), 'hair_included':hair_inc(HAIR),
                      'mouth_included':mouth_inc(MOUTH), 'skin_included':skin_inc(SKIN),
                      'prev sample sent out':prev_samp_sent_out(barcode(dogid, samplingpoint), sp_out)})

#Drop all rows where sum of all permisons is 0
df_sp = no_samples_drop_sp(df_sp, 'FAECES', 'URINE', 'HAIR', 'MOUTH', 'SKIN')

#Update Master To Say When Packs Have been Emailed Out
today = dt.date.today()
if 1 - today.weekday() == 0:
    next_tues = today + dt.timedelta(7)
else:
    next_tues = today + dt.timedelta( (1 - today.weekday()) % 7 )

#Add email date to admin page
message = 'emailed {}'.format(next_tues)
#6 Month
df_ad.loc[(df_ad['age in days today'] >= 170) & (df_ad['age in days today'] < 188), """SIX MONTHS Sampling kit sent if required

(NO KIT CONSENT MARKED BUT PLEASE DOUBLE CHECK OWNER HAS NOT CHANGED THEIR CONSENT)"""] = message

#12 Month
df_ad.loc[(df_ad['age in days today'] >= 355) & (df_ad['age in days today'] < 373), """12M Sampling kit SENT if required 

(NO KIT CONSENT MARKED BUT PLEASE DOUBLE CHECK OWNER HAS NOT CHANGED THEIR CONSENT)"""] = message

#Two Year
df_ad.loc[(df_ad['age in days today'] >= 720) & (df_ad['age in days today'] < 738), """TWO YEAR Sampling kit sent if required

(NO KIT CONSENT MARKED BUT PLEASE DOUBLE CHECK OWNER HAS NOT CHANGED THEIR CONSENT)"""] = message

#Three Year
df_ad.loc[(df_ad['age in days today'] >= 1085) & (df_ad['age in days today'] < 1103), """THREE YEAR Sampling kit sent if required

(NO KIT CONSENT MARKED BUT PLEASE DOUBLE CHECK OWNER HAS NOT CHANGED THEIR CONSENT)"""] = message

#Four Year
df_ad.loc[(df_ad['age in days today'] >= 1450) & (df_ad['age in days today'] < 1468), """FOUR YEAR Sampling kit sent if required

(NO KIT CONSENT MARKED BUT PLEASE DOUBLE CHECK OWNER HAS NOT CHANGED THEIR CONSENT)"""] = message

#Five Year
df_ad.loc[(df_ad['age in days today'] >= 1815) & (df_ad['age in days today'] < 1833), """FIVE YEAR Sampling kit sent if required

(NO KIT CONSENT MARKED BUT PLEASE DOUBLE CHECK OWNER HAS NOT CHANGED THEIR CONSENT)"""] = message

#Output sampling packs and new admin sheet
df_sp.to_excel(output_samp + '\sampling_packs_{}.xlsx'.format(dt_string), index=False)
df_ad.to_excel(output_admin + '\Admin_{}.xlsx'.format(dt_string), index=False)
