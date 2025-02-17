from utils.common_util import *
from import_data.common import *



"""
An object containing information in a consumption trend
"""
class ConsumeInfoDict:

    def __init__(self, totals_cost, start_date, end_date, consume_res_list):
        self.totals_cost = totals_cost
        self.start_date = start_date
        self.end_date = end_date
        self.consume_res_list = consume_res_list


"""
Function that graphs consumption by category.
"""
def visualize_consume_res_by_category(category_labels, category_size_labels, start_dt, end_date, total_cost, file_name):
    
    draw_circle_graph(category_size_labels, category_labels, False, 140, start_dt, end_date, total_cost, file_name)



"""
Function that draws a circle graph
"""
def draw_circle_graph(category_size_labels, category_labels, shadow, startangle, start_dt, end_date, total_cost, save_fig):

    # Dynamic Color Array Generation
    colors = plt.cm.viridis(np.linspace(0, 1, len(category_size_labels)))   

    plt.figure(figsize=(8, 8))  # Specify graph size
    plt.pie(category_size_labels, labels=category_labels, colors=colors, autopct='%1.1f%%', shadow=shadow, startangle=startangle)
    plt.axis('equal')
    
    plt.suptitle("[" + start_dt + " ~ " + end_date + "]", fontsize=16)  # Main title
    plt.title("Total Cost: " + f'{int(total_cost):,}', fontsize=10, color='black', loc='center', pad=20)  # Subtitle with smaller font and gray color
    
    # Save Graphs
    plt.savefig(save_fig)
    plt.close()
    

"""
Formatter Function Definition
"""
def thousands_formatter(x, pos):
    return f'{int(x):,}'


"""
Function that draws a graph
"""
def draw_line_graph(plt, title, x_label, y_label, file_uuid):

    # y-axis label formatting
    formatter = FuncFormatter(thousands_formatter)
    plt.gca().yaxis.set_major_formatter(formatter)
    
    # Set the x-axis to display integers only (not floats)
    plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True))

    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)  

    plt.legend()
    plt.savefig(file_uuid)  
    plt.close()      


"""
Function that plots a graph of two consumption trends
"""
def draw_line_graph_dual(consume_info_1, consume_info_2, file_uuid):
    
    len_1 = len(consume_info_1.consume_res_list)
    len_2 = len(consume_info_2.consume_res_list)

    # Add default values if both are empty
    if len_1 == 0 and len_2 == 0:
        consume_info_1.consume_res_list.append(0)
        consume_info_2.consume_res_list.append(0)
    
    # If the lengths are different, expand the short list.
    elif len_1 != len_2:
        shorter, longer = (consume_info_1, consume_info_2) if len_1 < len_2 else (consume_info_2, consume_info_1)
        gap = len(longer.consume_res_list) - len(shorter.consume_res_list)
        last_element = shorter.consume_res_list[-1] if shorter.consume_res_list else 0
        shorter.consume_res_list.extend([last_element] * gap)
    
    longer_len = max(len_1, len_2, 1)
    
    # Set the x value according to the length of the list.
    x = list(range(1, longer_len + 1))
    
    # Add an element if the length is 1
    if longer_len == 1:
        consume_info_1.consume_res_list.append(consume_info_1.consume_res_list[-1])
        consume_info_2.consume_res_list.append(consume_info_2.consume_res_list[-1])
        x.append(2)
    
    
    # Create Graphs
    plt.figure(figsize=(10,7))
    plt.plot(x, consume_info_1.consume_res_list, color='red', label="[{} ~ {}]".format(consume_info_1.start_date, consume_info_1.end_date))
    plt.plot(x, consume_info_2.consume_res_list, color='black', label="[{} ~ {}]".format(consume_info_2.start_date, consume_info_2.end_date))
    
    draw_line_graph(plt, "[{} ~ {}] {:,} won".format(consume_info_1.start_date, consume_info_1.end_date, int(consume_info_1.totals_cost)), 'Date', 'Consume Cost', file_uuid)
   

"""
Function that plots a graph of a consumption trend
"""
def draw_line_graph_single(consume_info, file_uuid):
    
    consume_info_len = len(consume_info.consume_res_list)
    
    x = [i+1 for i in range(consume_info_len)]
    
    # Create Graphs
    plt.figure(figsize=(10,7))
    plt.plot(x, consume_info.consume_res_list, color='red', label="[{} ~ {}]".format(consume_info.start_date, consume_info.end_date))

    draw_line_graph(plt, "[{} ~ {}] {:,} won".format(consume_info.start_date, consume_info.end_date, int(consume_info.totals_cost)), 'Date', 'Consume Cost', file_uuid)