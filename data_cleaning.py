
#%%
import pandas as pd
df = pd.read_csv("glassdoor_jobs.csv")
#df.head(3)



# - - - - - - - - - - - - 1. Salary parsing - - - - - - - - - - - -

# %%
#new Columns 'hourly' and 'employer_provided' with 1/0 values, 
# if its found or not in 'Salary Estimate 'column
df['hourly'] = df['Salary Estimate'].apply(lambda x: 1 if 'per hour' in x.lower() else 0)
df['employer_provided'] = df['Salary Estimate'].apply(lambda x: 1 if 'employer provided salary' in x.lower() else 0)

# %%
df = df[df['Salary Estimate']!='-1']
#print("dataset shape after removing the '-1' values: ",df.shape)

# %%
# Leave only the first part (salary range)
salary = df['Salary Estimate'].apply(lambda x: x.split('(')[0])
# %%
#Remove the 'k' and '$' from the dataframe 'salary'
minus_Kd = salary.apply(lambda x: x.replace('K','').replace('$',''))

# %%
#remove the words 'per hour' and 'employer provided salary:' from minus_Kd dataframe
min_hr = minus_Kd.apply(lambda x: x.lower().replace('per hour','').replace('employer provided salary:',''))
# %%
#Split the range e.g 40-50 by '-' in two parts
# so we'll finally have this split: 40 50 
#we take the left (40) split for min salary and right (50) for max salary
df['min_salary'] = min_hr.apply(lambda x: int(x.split('-')[0]))
df['max_salary'] = min_hr.apply(lambda x: int(x.split('-')[1]))
df['mean_salary'] = (df.min_salary+df.max_salary)/2
# %%
# - - - - - - - - - - - - 2. Company name text only - - - - - - - - - - - -
df['company_txt'] = df.apply(lambda x: x['Company Name'] if x['Rating']<0 else x['Company Name'][:-3], axis=1)
# %%
# - - - - - - - - - - - - 3. State location - - - - - - - - - - - -
df['job_state'] = df['Location'].apply(lambda x: x.split(',')[1])
df.job_state.value_counts()

df['same_state'] = df.apply(lambda x: 1 if x.Location == x.Headquarters else 0, axis=1)
# %%
# - - - - - - - - - - - - 4. Age of company  - - - - - - - - - - - -
df['age'] = df.Founded.apply(lambda x: x if x<1 else 2020 - x)

# %%
# - - - - - - - - - - - - 5. Parsing of job description (DS tools)  - - - - - - - - - - - -
# python
df['python_yn'] = df['Job Description'].apply(lambda x: 1 if 'python' in x.lower() else 0)
df.python_yn.value_counts()
# r
df['R_yn'] = df['Job Description'].apply(lambda x: 1 if 'r studio' in x.lower() or 'r-studio' in x.lower() else 0)
df.R_yn.value_counts()
# spark
df['Spark_yn'] = df['Job Description'].apply(lambda x: 1 if 'spark' in x.lower() else 0)
df.Spark_yn.value_counts()
# aws
df['AWS_yn'] = df['Job Description'].apply(lambda x: 1 if 'aws' in x.lower() else 0)
df.AWS_yn.value_counts()
# excel
df['Excel_yn'] = df['Job Description'].apply(lambda x: 1 if 'excel' in x.lower() else 0)
df.Excel_yn.value_counts()
# tableau
df['Tableau_yn'] = df['Job Description'].apply(lambda x: 1 if 'tableau' in x.lower() else 0)
df.Tableau_yn.value_counts()
# tensorflow
df['Tensorflow_yn'] = df['Job Description'].apply(lambda x: 1 if 'tensorflow' in x.lower() else 0)
df.Tensorflow_yn.value_counts()
# matlab
df['Matlab_yn'] = df['Job Description'].apply(lambda x: 1 if 'matlab' in x.lower() else 0)
df.Matlab_yn.value_counts()
# scikit-learn
df['Scikit_yn'] = df['Job Description'].apply(lambda x: 1 if 'scikit-learn' in x.lower() or 'scikit learn' in x.lower() else 0)
df.Scikit_yn.value_counts()
# sas
df['SAS_yn'] = df['Job Description'].apply(lambda x: 1 if 'sas' in x.lower() else 0)
df.SAS_yn.value_counts()
#

# %%
#Drop first column
df_out = df.drop(['Unnamed: 0'],axis=1)
df_out.to_csv('data_cleaned.csv',index=False)

