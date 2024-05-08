import matplotlib.pyplot as plt
import pandas as pd

def read_xlsx_file(file_name):
    try:
        df = pd.read_excel(file_name)
        data = [(mrr, mop) for mrr, mop in zip(df['MRR'], df['MOP'])]
        return data
    except Exception as e:
        print(f"Error reading the file: {e}")
        return None

def scatter_plot(axs, i, data, color, title):
    x = [point[0] for point in data]
    y = [point[1] for point in data]
    axs[i].scatter(x, y, color=color)
    axs[i].set_xlabel('MRR')
    axs[i].set_ylabel('MOP')
    axs[i].set_title(title)


all_excel_path = [
    'grid_search_result.xlsx',
    'random_search_result.xlsx',
    'bayesian_search_result_05_05.xlsx',
    'bayesian_search_result_07_03.xlsx',
    'bayesian_search_result_03_07.xlsx',
    'nsga2_result.xlsx'
]

labels = [
    'Grid Search',
    'Random Search',
    'Bayesian-EQ',
    'Bayesian-MRR',
    'Bayesian-MOP',
    'NSGA-II'
]

colors = ['blue', 'green', 'red', 'orange', 'purple']

x_min = 0.0
x_max = 1.0
y_min = 0.0
y_max = 1.0


fig, axs = plt.subplots(2, 3, figsize=(12,8))
plt.rcParams.update({'font.size': 13})
line = 0
for i, excel_path in enumerate(all_excel_path[:3]):
    #plt.grid(True)
    metrics_points = read_xlsx_file(excel_path)
    scatter_plot(axs[line], i, metrics_points, 'purple', labels[i])
    axs[line, i].set_xlim(x_min, x_max)
    axs[line, i].set_ylim(y_min, y_max)

line = 1
for i, excel_path in enumerate(all_excel_path[3:]):
    #plt.grid(True)
    metrics_points = read_xlsx_file(excel_path)
    scatter_plot(axs[line], i, metrics_points, 'purple', labels[i+3])
    axs[line, i].set_xlim(x_min, x_max)
    axs[line, i].set_ylim(y_min, y_max)

# Scatter plot
plt.tight_layout()
plt.savefig("scatter_plot")
plt.savefig('scatter_plot.pdf', dpi=300)
#plt.show()
plt.close('all')