import sys
import pandas as pd 

initial_file = open(sys.argv[1], "rb")
df = pd.read_csv(initial_file)


def encode ( column ):
	df[column] = df[column].str.decode('unicode_escape')
	df[column] = df[column].str.encode('utf8', errors='strict') 

#convert FooDuration to floating point format
df['FooDuration'] = pd.to_timedelta(df['FooDuration'], unit='s')

#convert BarDuration to floating point format
df['BarDuration'] = pd.to_timedelta(df['BarDuration'], unit='s')

#TotalDuration should be sum of FooDuration and BarDuration
df['TotalDuration'] = df['FooDuration'] + df['BarDuration']

#capitalize names
df['FullName'] = map(lambda x: x.title(), df['FullName'])

#change zip codes
df['ZIP'] = df['ZIP'].astype(str).str.zfill(5)

#convert timestamp to ISO-8601 format
df['Timestamp'] = pd.to_datetime(df['Timestamp'],infer_datetime_format=True)

#convert timestamp from Pacific to Eastern
df['Timestamp']= df['Timestamp'].dt.tz_localize('US/Pacific')
df['Timestamp'] = df['Timestamp'].dt.tz_convert('US/Eastern')

#convert non-utf8 characters in Notes to Unicode characters.
encode('Notes')

#convert non-utf8 characters in Adddress to Unicode characters.
encode ('Address')

df.to_csv(open(sys.argv[2], "wb"), index=False)

