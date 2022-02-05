import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import os

def case_conditon(x):
    conditions = pd.read_csv("./data/scores.csv")
    conditions = conditions[conditions.number.str.startswith("condition")]

    print(conditions)
    conditions['Delta']= conditions.madrs2 - conditions.madrs1
    print("---------")
    print(conditions)
    print(conditions.shape)
    print("---------")
    txt_missing = 'missing'
    conditions.melanch = conditions.melanch.fillna(txt_missing)
    conditions.melanch = conditions.melanch.astype('category')
    conditions.melanch = conditions.melanch.cat.rename_categories({-1 : txt_missing,1.0 : '1',2.0 : '2'})

    conditions.inpatient = conditions.inpatient.fillna(txt_missing)
    conditions.inpatient = conditions.inpatient.astype('category')
    conditions.inpatient = conditions.inpatient.cat.rename_categories({-1 : txt_missing,1.0 : '1',2.0 : '2'})
    conditions.days = conditions.days.astype('category')
    conditions.age = conditions.age.astype('category')
    conditions.gender = conditions.gender.astype('category')
    conditions.afftype = conditions.afftype.astype('category')
    conditions.marriage = conditions.marriage.astype('category')
    conditions.work = conditions.work.astype('category')
    conditions.edu = conditions.edu.astype('category')
    conditions.edu = conditions.edu.cat.rename_categories({' ' : txt_missing})
    print(conditions)
    features_num = ['days','madrs1','madrs2','Delta']
    features_cat = ['age','gender','afftype','melanch','inpatient','edu','marriage','work']

    if x ==0:
        print(conditions[features_cat].describe())
        for f in features_cat:
            
            conditions[f].value_counts().sort_index().plot(kind='bar')
            fig1 = plt.gcf()
            plt.title(f)
            plt.grid()
            plt.show()

            fig1.savefig('./data/stat/condition/pure/'+f+'.jpg')
        temp_plot_paras = plt.rcParams['figure.figsize']
        plt.rcParams['figure.figsize'] = (14,4)
        conditions.plot(x='number', y=['madrs1','madrs2'], kind='bar')
        plt.title('MADRS Development')
        fig1 = plt.gcf()
        plt.grid()
        plt.show()
        plt.rcParams['figure.figsize'] = temp_plot_paras
        fig1.savefig('./data/stat/condition/pure/delta.jpg')

    elif x == 1:
        print("hey")
        return conditions
        
def case_control(x):
    control = pd.read_csv("./data/scores.csv")
    control = control[control.number.str.startswith("control")]
    txt_missing = '_MISSING_'
    print(control)
    control.days = control.days.astype('category')
    control.gender = control.gender.astype('category')
    control.age = control.age.astype('category')
    features_cat =['days','gender','age']
    print(control[features_cat].describe())
    if x ==0:
        for f in features_cat:
            control[f].value_counts().sort_index().plot(kind='bar')
            fig1 = plt.gcf()
            plt.title(f)
            plt.grid()
            plt.show()
            fig1.savefig('./data/stat/control/pure/'+f+'.jpg')
    if x ==1:
        return control

def case_data_condition():
    txt_missing = 'missing'
    sum_dict = {}
    for file in os.listdir("./data/condition/"):
        df = pd.read_csv("./data/condition/" + "/" + file)
        sum_dict[file.split(".")[0]] = df.activity.sum()
    sums = pd.DataFrame(pd.Series(sum_dict))
    sums.columns = ["Sum"]
    
    conditions = pd.read_csv("./data/scores.csv")
    conditions = conditions[conditions.number.str.startswith("condition")]
    conditions = conditions.set_index("number").join(sums).reset_index()
    conditions["Stress"] = conditions.Sum / conditions.days
    print(conditions)

    conditions.Sum = conditions.Sum.astype('category')
    conditions.Stress = conditions.Stress.astype('category')
    features_num = ['Sum','Stress']

    my_alpha=0.5
    fig, ax = plt.subplots(figsize=(18,6))
    ax.scatter(conditions.number, conditions.Sum , alpha=my_alpha)
    ax.xaxis.set_major_locator(plt.MaxNLocator(25)) # reduce number of x-axis labels
    plt.title("Sum")
    plt.xticks(rotation=90)
    plt.grid()
    ax.legend(loc='upper left')
    fig1 = plt.gcf()
    plt.show()
    fig1.savefig('./data/stat/condition/full/Sum.jpg')

    fig, ax = plt.subplots(figsize=(18,6))
    ax.scatter(conditions.number, conditions.Stress , alpha=my_alpha)
    ax.xaxis.set_major_locator(plt.MaxNLocator(25)) # reduce number of x-axis labels
    plt.title("Stress")
    plt.xticks(rotation=90)
    plt.grid()
    ax.legend(loc='upper left')
    fig5 = plt.gcf()
    plt.show()
    fig5.savefig('./data/stat/condition/full/Stress.jpg')

    features_cat = ['age','gender','afftype','melanch','inpatient','edu','marriage','work']
    for f in features_cat:
        plt.figure(figsize=(10,4))
        sns.violinplot(data=conditions, x=f, y='madrs2')
        plt.title('madrs2 vs ' + f)
        fig2 = plt.gcf()
        plt.grid()
        plt.show()
        fig2.savefig('./data/stat/condition/full/madrs2'+f+'.jpg')
    for f in features_cat:
        plt.figure(figsize=(10,4))
        sns.violinplot(data=conditions, x=f, y='madrs1')
        plt.title('madrs1 vs ' + f)
        fig2 = plt.gcf()
        plt.grid()
        plt.show()
        fig2.savefig('./data/stat/condition/full/madrs1'+f+'.jpg')
    for f in features_cat:
        plt.figure(figsize=(10,4))
        sns.violinplot(data=conditions, x=f, y='Delta')
        plt.title('delta vs ' + f)
        fig2 = plt.gcf()
        plt.grid()
        plt.show()
        fig2.savefig('./data/stat/condition/full/delta'+f+'.jpg')
    print(conditions)
    
def case_data_control():
    txt_missing = 'missing'
    sum_dict = {}
    for file in os.listdir("./data/control/"):
        df = pd.read_csv("./data/control/" + "/" + file)
        sum_dict[file.split(".")[0]] = df.activity.sum()
    sums = pd.DataFrame(pd.Series(sum_dict))
    sums.columns = ["Sum"]

    control = pd.read_csv("./data/scores.csv")
    control = control[control.number.str.startswith("control")]
    control = control.set_index("number").join(sums).reset_index()
    control["Stress"] = control.Sum / control.days
    control.Sum = control.Sum.astype('category')
    control.Stress = control.Stress.astype('category')
    features_num = ['Sum','Stress']

    my_alpha=0.5
    fig, ax = plt.subplots(figsize=(18,6))
    ax.scatter(control.number, control.Sum , alpha=my_alpha)
    ax.xaxis.set_major_locator(plt.MaxNLocator(40)) # reduce number of x-axis labels
    plt.title("Sum")
    plt.xticks(rotation=90)
    plt.grid()
    ax.legend(loc='upper left')
    fig1 = plt.gcf()
    plt.show()
    fig1.savefig('./data/stat/control/full/Sum.jpg')
    control.Sum = control.Sum.astype('category')
    features_num = ['Sum']
    
    fig, ax = plt.subplots(figsize=(18,6))
    ax.scatter(control.number, control.Stress , alpha=my_alpha)
    ax.xaxis.set_major_locator(plt.MaxNLocator(25)) # reduce number of x-axis labels
    plt.title("Stress")
    plt.xticks(rotation=90)
    plt.grid()
    ax.legend(loc='upper left')
    fig5 = plt.gcf()
    plt.show()
    fig5.savefig('./data/stat/control/full/Stress.jpg')

def case_data_condition_activity():
    for file in os.listdir("./data/condition/"):
        df = pd.read_csv("./data/condition/" + "/" + file)
        
        plt.figure(figsize=(10,4))
        df.activity.plot(kind='hist', bins=100)
        plt.title(file+'Activity - Histogram')
        plt.grid()
        fig1 = plt.gcf()
        plt.show()
        fig1.savefig('./data/stat/activity_condtion/activity_per_condition/'+file+'_activity.jpg')
        
        my_alpha=0.25
        fig, ax = plt.subplots(figsize=(18,6))
        ax.scatter(df.timestamp, df.activity , alpha=my_alpha)
        ax.xaxis.set_major_locator(plt.MaxNLocator(30)) # reduce number of x-axis labels
        plt.title(file+"time -activity ")
        plt.xticks(rotation=90)
        plt.grid()
        ax.legend(loc='upper left')
        fig2 = plt.gcf()
        plt.show()
        fig2.savefig('./data/stat/activity_condtion/activity_per_condition/'+file+'_time_per_acitivity.jpg')

def case_data_control_activity():
    for file in os.listdir("./data/control/"):
        df = pd.read_csv("./data/control/" + "/" + file)
        
        plt.figure(figsize=(10,4))
        df.activity.plot(kind='hist', bins=100)
        plt.title(file+'Activity - Histogram')
        plt.grid()
        fig1 = plt.gcf()
        plt.show()
        fig1.savefig('./data/stat/activity_control/activity_per_control/'+file+'_activity.jpg')
        
        my_alpha=0.25
        fig, ax = plt.subplots(figsize=(18,6))
        ax.scatter(df.timestamp, df.activity , alpha=my_alpha)
        ax.xaxis.set_major_locator(plt.MaxNLocator(30)) # reduce number of x-axis labels
        plt.title(file+"time -activity ")
        plt.xticks(rotation=90)
        plt.grid()
        ax.legend(loc='upper left')
        fig2 = plt.gcf()
        plt.show()
        fig2.savefig('./data/stat/activity_control/activity_per_control/'+file+'_time_per_acitivity.jpg')

def main():
    x = int(input("enter case (1 for conditon,2 for control,3 for data_condition,4 for data_control,5 for condition_activity, 6 for control_activity, 9 for quit) : "))
    if x == 1:
        case_conditon(0)
        main()
    elif x == 2:
        case_control(0)
        main()
    elif x == 3:
        case_data_condition()
        main()
    elif x == 4:
        case_data_control()
        main()
    elif x == 5:
        case_data_condition_activity()
        main()
    elif x == 6:
        case_data_control_activity()
        main()
    elif x==9:
        print("bye")
    else:
        print("1 for conditon,2 for control,3 for data_condition,4 for data_control,5 for conditon_activity,6 for control_activity, 9 for quit")
        main()
    
if __name__ == '__main__':
    main()
        