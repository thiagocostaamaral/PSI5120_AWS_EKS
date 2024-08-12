import pandas as pd
import matplotlib.pyplot as plt
import os 

base_folder = '../Stress_Files/'
Stressfiles = os.listdir(base_folder)

#Grabbing all results
results = []
results_dict = {}
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
    df['time'] = df.index*2.5
    results.append(
        {'Workers':workers, 'timeRequests':timeRequests,'data':df.copy(deep=True),'NormalizedLoad':base_unit/timeRequests}
    )
    results_dict[StressFile] =  {'Workers':workers, 'timeRequests':timeRequests,'data':df.copy(deep=True),'NormalizedLoad':base_unit/timeRequests}

#%%
#Plotting 2 workers
fig =plt.figure(figsize=[12,10])
plt.title('Stress with 2 Workers')
for result in results:
    #if result['Workers']!=2:
    #    continue
    stress_df = result['data']
    plt.plot(stress_df['time'],stress_df['CPU usage'],label='%d Load / Replicas %d '%(result['NormalizedLoad'],stress_df['REPLICAS'].max()))
plt.legend()
plt.grid()
plt.show()

#%%
#Plotting all info
plt.figure(figsize=(10, 12))
i=1
for key in ['StressLog1_5.log', 'StressLog2_5.log','StressLog1_1.log','StressLog2_1.log', 'StressLog1_01.log', 'StressLog2_01.log']:
    result = results_dict[key]
    plt.subplot(3, 2, i)
    plt.title('Workers: '+str(result['Workers'])+ ' - Load:'+str(result['NormalizedLoad']) )
    stress_df = result['data']
    ax1 = plt.gca()  # Get current axis
    color = 'tab:blue'
    ax1.plot(stress_df['time'],stress_df['CPU usage'],label='CPU Usage',color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.set_ylim([0,250])
    if i%2==1:
        ax1.set_ylabel('CPU', color=color)
    if i>4:
        ax1.set_xlabel('Time (s)')
    ax2 = ax1.twinx() 
    color = 'tab:red'
    ax2.plot(stress_df['time'],stress_df['REPLICAS'],label='Replicas',color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.set_ylim([1,8])
    if i%2==0:
        ax2.set_ylabel('Replicas', color=color)
    i += 1
plt.savefig('../Figures/WorkersSimulation.jpeg')
# %%

#%%
stable_results = []
for key in ['StressLog1_5.log', 'StressLog2_5.log','StressLog1_1.log','StressLog2_1.log', 'StressLog1_01.log', 'StressLog2_01.log']:
    workers = results_dict[key]['Workers']
    load = results_dict[key]['NormalizedLoad']
    df = results_dict[key]['data']
    df = df.loc[(df['time']>100) & (df['time']<200)]
    mean_use = df['CPU usage'].mean()
    stable_results.append([workers,load,df['REPLICAS'].max(),mean_use])
    
stable_df = pd.DataFrame(stable_results,columns=['Workers','Load','Replicas','CPU Use'])
display(stable_df)
# %%
