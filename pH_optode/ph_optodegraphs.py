#%% PLOTTING
#%% plotting the regression with seaborn
for file in file_list:
    fig, ax = plt.subplots()
    sns.regplot(data[file].sec, data[file].pH, fit_reg=True, x_ci="sd")
    
#%% scatter each plot individually
for file in file_list:
    data[file].plot.scatter("sec", "pH")

#%% plot line each file on same plot
fig, ax = plt.subplots()
for file in file_list:
    data[file].plot("sec", "pH", ax=ax)
    
#%% jointplot of averages distribution
fig, ax = plt.subplots()
sns.despine(left=True)
d = avg.average_pH
#sns.distplot(d, kde=False, color="b", ax=ax)
sns.jointplot(d,d, kind="hex", color="#4CB391")