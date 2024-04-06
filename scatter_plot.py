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

def scatter_plot(ax, data, color, title):
    x = [point[0] for point in data]
    y = [point[1] for point in data]
    ax.scatter(x, y, color=color)
    ax.set_xlabel('MRR')
    ax.set_ylabel('MOP')
    ax.set_title(title)


all_excel_path = [
#'output.xlsx',
#'grid_search_2024-04-01.xlsx',
#'random_search_result.xlsx',
'bayesian_search_result_05_05.xlsx',
#'bayesian_search_result_07_03.xlsx',
#'bayesian_search_result_03_07.xlsx',
'nsga2_result.xlsx'
]

labels = [
    #'Grid Search',
    #'Random Search',
    'Bayesian Search (05,05)',
    #'Bayesian Search (07,03)',
    #'Bayesian Search (03,07)',
    'NSGA-II'
]

colors = ['blue', 'green', 'red', 'orange', 'purple']

x_min = 0.0
x_max = 1.0
y_min = 0.0
y_max = 1.0

fig, axs = plt.subplots(1, 2, figsize=(12, 4))
for i, excel_path in enumerate(all_excel_path):
    #plt.grid(True)
    metrics_points = read_xlsx_file(excel_path)
    scatter_plot(axs[i], metrics_points, 'purple', labels[i])
    axs[i].set_xlim(x_min, x_max)
    axs[i].set_ylim(y_min, y_max)

# Scatter plot
plt.tight_layout()
plt.savefig("scatter_plot")
plt.show()
plt.close('all')