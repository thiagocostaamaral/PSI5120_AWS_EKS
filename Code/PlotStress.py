import pandas as pd
import matplotlib.pyplot as plt
import os 

base_folder = '../Stress_Files/'
Stressfiles = os.listdir(base_folder)

#Grabbing all results
results = []
base_unit = 0.5
for StressFile in Stressfiles:
    print(StressFile)
    info = open(base_folder+StressFile, "r").read()
    #Getting time information
    workers = int(StressFile.split('StressLog')[1][0])
    timeRequests = float('0.'+StressFile.split('_')[1].split('.')[0])
    #Process log file to have datafrmae
    info = info.replace('cpu: ','')
    info = info.split()
    lines = []
    line = []
    for i in range(len(info)):
        if i%7==0:
            lines.append(line)
            line = []
        line.append(info[i])
    lines = lines[1:]
    df = pd.DataFrame(lines[1:], columns=lines[0])
    df['CPU usage'] = df['TARGETS'].apply(lambda x: int(x.split('%')[0]))
    df['REPLICAS'] = df['REPLICAS'].apply(lambda x: int(x))
    df['time'] = df.index*2
    results.append(
        {'Workers':workers, 'timeRequests':timeRequests,'data':df.copy(deep=True),'NormalizedLoad':base_unit/timeRequests}
    )

#Plotting 2 workers
fig =plt.figure(figsize=[12,10])
plt.title('Stress with 2 Workers')
for result in results:
    if result['Workers']!=2:
        continue
    stress_df = result['data']
    plt.plot(stress_df['time'],stress_df['CPU usage'],label='%d Load / Replicas %d '%(result['NormalizedLoad'],stress_df['REPLICAS'].max()))
plt.legend()
plt.grid()
plt.show()

#%%
#Plotting all info
plt.figure(figsize=(12, 8))
i=1
for result in results:
    plt.subplot(2, 3, i)
    plt.title('Workers: '+str(result['Workers'])+ ' - Load:'+str(result['NormalizedLoad']) )
    stress_df = result['data']
    ax1 = plt.gca()  # Get current axis
    color = 'tab:blue'
    ax1.plot(stress_df['time'],stress_df['CPU usage'],label='CPU Usage',color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx() 
    color = 'tab:red'
    ax2.plot(stress_df['time'],stress_df['REPLICAS'],label='Replicas',color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.set_ylim([1,8])
    i += 1
# %%
