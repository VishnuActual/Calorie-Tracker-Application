import io
import csv
import os 
import pandas as pd 
import matplotlib.pyplot as plt 

def generate_csv(logs):
    csv_data = io.StringIO()
    writer = csv.writer(csv_data)

    # Write header row
    writer.writerow(["Date", "Breakfast", "Lunch", "Dinner", "Snacks", "Total"])

    # Write data rows
    for log in logs:
        writer.writerow([
            log.date_posted.strftime('%Y-%m-%d'),
            log.breakfast,
            log.lunch,
            log.dinner,
            log.snacks,
            log.breakfast + log.lunch + log.dinner + log.snacks
        ])

    csv_data.seek(0)
    return csv_data



def weekly_csv(logs):
    dir_path = os.path.dirname(__file__)

    dir_path = dir_path.split('\calories')[0]
    file_path = os.path.join(dir_path, 'data/temp_weekly_data.csv')

    open(file_path, 'w').close()
    if len(logs)==0:
        fig, ax = plt.subplots()
        image_path= os.path.join(dir_path,'static/pie_charts/daywise.png')
        plt.savefig(image_path, dpi=300, bbox_inches='tight')
        image_path= os.path.join(dir_path,'static/pie_charts/mealwise.png')
        plt.savefig(image_path, dpi=300, bbox_inches='tight')
        return 

    with open(file_path, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Write header row
        writer.writerow(["Date", "Breakfast", "Lunch", "Dinner", "Snacks", "Total"])

        # Write data rows
        for log in logs:
            writer.writerow([
                log.date_posted.strftime('%Y-%m-%d'),
                log.breakfast,
                log.lunch,
                log.dinner,
                log.snacks,
                log.breakfast + log.lunch + log.dinner + log.snacks
            ])

    data = pd.read_csv("flaskblog/data/temp_weekly_data.csv", sep=',') 

    #making the daywise piechart for a week 
    fig, ax = plt.subplots()
    ax.pie(data.Total, labels=data.Date, autopct='%1.1f%%')
    ax.set_title('Daywaise analysis per week')
    ax.axis('equal')
    image_path= os.path.join(dir_path,'static/pie_charts/daywise.png')
    plt.savefig(image_path, dpi=300, bbox_inches='tight')


    #making the mealwise 
    labels = data.columns[1:-1]
    # print('--------------------------------------')
    # print(labels)
    # print("----------------------------------------")
    values = [] 
    for label in labels:
        print(label) 
        x = sum(data[label]) 
        values.append(x) 


    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct='%1.1f%%')
    ax.set_title('Mealwise analysis per week')
    ax.axis('equal')
    image_path2= os.path.join(dir_path,'static/pie_charts/mealwise.png')
    plt.savefig(image_path2, dpi=300, bbox_inches='tight')
    

    