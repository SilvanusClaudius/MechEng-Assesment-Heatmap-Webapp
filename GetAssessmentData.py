import requests
import time
import pandas as pd

def Get_Config_Data(config_url):
    try:
        config_content = requests.get(config_url, allow_redirects=True)
        f = open('config.csv', 'wb')
        f.write(config_content.content)
        f.close()

        config_df = pd.read_csv("config.csv")
        config_df = config_df[['Field', 'URL']]
        print("Configuration file has been read")
        print(config_df.head())

    except Exception as e:
        print('Error Occurred while reading from configuration file. Check filenames and URL, '
              'and GetAssessmentData.py - Jeny')
        print(e)

        return

    return config_df

def Get_Assessments_Data(db_url):
    try:
        start = time.time()
        db_content = requests.get(db_url, allow_redirects=True)
        f = open('testDB.csv', 'wb')
        f.write(db_content.content)
        f.close()

        df = pd.read_csv("testDB.csv")
        df = df[['Deadline Date', 'Module Code ', 'Assessment Weighting (%)', 'Module Title', 'Assessment Name',
                 'Assessment Type', 'Course', 'Year', 'Combined']]

        end =  time.time()
        time_elapsed = end - start
        print(f'Assessment Database read successfully in %2d seconds' %(time_elapsed))
        #print(df.shape())
        print(df.head())

    except Exception as e:
        print('Error Occurred while reading from Assessment Database file. Check filenames and URL, '
              'and GetAssessmentData.py - Jeny')
        print(e)
        return

    return df

def Get_Module_Data(mods_url):
    try:
        start = time.time()
        db_content = requests.get(mods_url, allow_redirects=True)
        f = open('modulesimported.csv', 'wb')
        f.write(db_content.content)
        f.close()

        df = pd.read_csv("modulesimported.csv")
        df = df.applymap(str) #converts integers to strings so they can be joined in the next step
        df['ProgramMods'] = df[['Module 1','Module 2','Module 3','Module 4','Module 5','Module 6',
                                'Module 7','Module 8','Module 9','Module 10']].agg(','.join, axis=1)
        #df['ProgramMods'] = df[['Module 1', 'Module 2', 'Module 3']].agg(','.join, axis=1)

        df = df[['Programme','Minor Name','Minor Code','ProgramMods', 'Module 8', 'Module 5', 'Module 6']]
        df.set_index(['Programme','Minor Code'], inplace=True) #Important to set the index to this multiindex for later
        print(f'Module Database read successfully')
        print(df.head())

    except:
        print('Error Occurred while reading from Module Database file. Check filenames and URL, '
              'and GetData.py - Jeny')
        raise
        return

    return df