from utils.common_util import *
from utils.matplot_util import *
from import_data import *
from config import global_logger


# An object containing information in a consumption trend
class ConsumeInfoDict:

    def __init__(self, totals_cost, start_date, end_date, consume_res_list):
        self.totals_cost = totals_cost
        self.start_date = start_date
        self.end_date = end_date
        self.consume_res_list = consume_res_list

# Graph related font settings. - Globally set.
font_prop = font_manager.FontProperties(fname="./data/font/BMDOHYEON_ttf.ttf").get_name()
plt.rc('font', family=font_prop)

app = Flask(__name__)

@app.route('/api/category', methods=['POST'])
def category_app():
    
    data = request.get_json()
    
    category_labels = data["title_vec"]
    category_size_labels = data["cost_vec"]
    start_dt = data["start_dt"]
    end_dt = data["end_dt"]
    total_cost = data["total_cost"]
    
    #file_uuid = '/Users/we/Documents/work_code/consume_alert_rust/consume_alert_rust/data/' + str(uuid.uuid4()) + ".png"
    file_uuid = '/Users/sinseunghwan/Documents/work_code/python_graph_api/data/' + str(uuid.uuid4()) + ".png"
    #print(file_uuid)

    visualize_consume_res_by_category(category_labels, category_size_labels, start_dt, end_dt, total_cost, file_uuid)
    
    # jsonify
    return file_uuid, 200


@app.route('/api/consume_detail_double', methods=['POST'])
def consume_detail_double_app():
    
    data = request.get_json()
    
    cur_consume_info = None
    pre_consume_info = None
    
    for elem in data:
        
        line_type = elem['line_type']
        start_dt = elem['start_dt']
        end_dt = elem['end_dt']
        total_cost = elem['total_cost']
        consume_accumulate_list = elem['consume_accumulate_list']

        print(line_type)
        print(start_dt)
        print(end_dt)
        print(total_cost)
        print(consume_accumulate_list)

        # consume_info_dict = ConsumeInfoDict(line_type, total_cost, start_dt, end_dt, consume_accumulate_list)

        # if line_type == "cur":
        #     cur_consume_info = consume_info_dict
        # else:
        #     pre_consume_info = consume_info_dict

    # print(cur_consume_info.totals_cost)

    # print(pre_consume_info.totals_cost)

    #draw_line_graph_dual(cur_consume_info, pre_consume_info)

    # print(data)
    # category_labels = data["title_vec"]
    # category_size_labels = data["cost_vec"]
    # start_dt = data["start_dt"]
    # end_dt = data["end_dt"]
    # total_cost = data["total_cost"]
    
    #file_uuid = '/Users/we/Documents/work_code/consume_alert_rust/consume_alert_rust/data/' + str(uuid.uuid4()) + ".png"
    file_uuid = '/Users/sinseunghwan/Documents/work_code/python_graph_api/data/' + str(uuid.uuid4()) + ".png"
    #print(file_uuid)

    #visualize_consume_res_by_category(category_labels, category_size_labels, start_dt, end_dt, total_cost, file_uuid)
    
    # jsonify
    return file_uuid, 200


@app.route('/api/consume_detail_single', methods=['POST'])
def consume_detail_single_app():
    
    data = request.get_json()
    
    category_labels = data["title_vec"]
    category_size_labels = data["cost_vec"]
    start_dt = data["start_dt"]
    end_dt = data["end_dt"]
    total_cost = data["total_cost"]
    
    #file_uuid = '/Users/we/Documents/work_code/consume_alert_rust/consume_alert_rust/data/' + str(uuid.uuid4()) + ".png"
    file_uuid = '/Users/sinseunghwan/Documents/work_code/python_graph_api/data/' + str(uuid.uuid4()) + ".png"
    #print(file_uuid)

    #visualize_consume_res_by_category(category_labels, category_size_labels, start_dt, end_dt, total_cost, file_uuid)
    
    # jsonify
    return file_uuid, 200