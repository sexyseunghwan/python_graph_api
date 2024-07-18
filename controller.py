from utils.common_util import *
from utils.matplot_util import *
from import_data import *
from config import global_logger


# Graph related font settings. - Globally set.
font_prop = font_manager.FontProperties(fname="./data/font/BMDOHYEON_ttf.ttf").get_name()
plt.rc('font', family=font_prop)

app = Flask(__name__)

# 
@app.route('/api/category', methods=['POST'])
def category_app():
    
    try:
        data = request.get_json()
        
        category_labels = data["title_vec"]
        category_size_labels = data["cost_vec"]
        start_dt = data["start_dt"]
        end_dt = data["end_dt"]
        total_cost = data["total_cost"]
        
        #file_uuid = '/Users/we/Documents/work_code/consume_alert_rust/consume_alert_rust/data/pngs/' + str(uuid.uuid4()) + ".png"
        file_uuid = '/Users/sinseunghwan/Documents/work_code/consume_alert_rust/consume_alert_rust/data/images/' + str(uuid.uuid4()) + ".png"

        visualize_consume_res_by_category(category_labels, category_size_labels, start_dt, end_dt, total_cost, file_uuid)
        
        # jsonify
        return file_uuid, 200
    
    except Exception as e:
        global_logger.error(str(e), exc_info=True)
        return jsonify({'error': 'An error occurred: {}'.format(str(e))}), 500
    
# 
@app.route('/api/consume_detail', methods=['POST'])
def consume_detail_double_app():
    
    try:
        data = request.get_json()
        
        cur_consume_info = None
        pre_consume_info = None
        
        for elem in data:
            
            line_type = elem['line_type']
            consume_info_dict = ConsumeInfoDict(elem['total_cost'], elem['start_dt'], elem['end_dt'], elem['consume_accumulate_list'])
            
            if line_type == "cur":
                cur_consume_info = consume_info_dict
            else:
                pre_consume_info = consume_info_dict

        #file_uuid = '/Users/we/Documents/work_code/consume_alert_rust/consume_alert_rust/data/pngs/' + str(uuid.uuid4()) + ".png"
        file_uuid = '/Users/sinseunghwan/Documents/work_code/consume_alert_rust/consume_alert_rust/data/images/' + str(uuid.uuid4()) + ".png"

        if pre_consume_info == None:
            draw_line_graph_single(cur_consume_info, file_uuid)
        else:
            draw_line_graph_dual(cur_consume_info, pre_consume_info, file_uuid)

        # jsonify
        return file_uuid, 200
    
    except Exception as e:
        global_logger.error(str(e), exc_info=True)
        return jsonify({'error': 'An error occurred: {}'.format(str(e))}), 500