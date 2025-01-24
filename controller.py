from utils.common_util import *
from utils.matplot_util import *
from import_data import *
from config import global_logger


""" 
Graph related font settings. - Globally set.
"""
font_prop = font_manager.FontProperties(fname="./data/font/BMDOHYEON_ttf.ttf").get_name()
plt.rc('font', family=font_prop)


"""
Flask settings
"""
app = Flask(__name__)


"""
TEST API
"""
@app.route('/api/test', methods=['GET'])
def test_app():

    try:
        
        data = request.get_json()
        test = data["test"]

        global_logger.info("test")
        print(test)
        

        return "test", 200

    except Exception as e:
        global_logger.error(str(e), exc_info=True)
        return jsonify({'error': 'An error occurred: {}'.format(str(e))}), 500


"""
Functions to draw consumption history category graphs
"""
@app.route('/api/category', methods=['POST'])
def category_app():
    
    try:
        data = request.get_json()
        
        category_labels = data["prodt_type_vec"]
        category_size_labels = data["prodt_type_cost_per_vec"]
        start_dt = data["start_dt"]
        end_dt = data["end_dt"]
        total_cost = data["total_cost"]
        
        file_path = os.getenv('FILE_PATH')
        file_uuid = file_path + str(uuid.uuid4()) + ".png"
        visualize_consume_res_by_category(category_labels, category_size_labels, start_dt, end_dt, total_cost, file_uuid)
        
        # jsonify
        return file_uuid, 200
        
    except Exception as e:
        global_logger.error(str(e), exc_info=True)
        return jsonify({'error': 'An error occurred: {}'.format(str(e))}), 500

"""
Function to draw consumption details graph
"""
@app.route('/api/consume_detail', methods=['POST'])
def consume_detail_double_app():
    
    try:
        data = request.get_json()
        
        cur_consume_info = None
        pre_consume_info = None
        
        # If the size of the vector data passed to the post exceeds 2
        if len(data) > 2:
            error_msg = "The size of the vector cannot exceed two."
            global_logger.error(str(error_msg), exc_info=True)
            return jsonify({'error': 'An error occurred: {}'.format(str(error_msg))}), 500
        

        for elem in data:
            
            line_type = elem['line_type']
            consume_info_dict = ConsumeInfoDict(elem['total_cost'], elem['start_dt'], elem['end_dt'], elem['consume_accumulate_list'])
            
            if line_type == "cur":
                cur_consume_info = consume_info_dict
            else:
                pre_consume_info = consume_info_dict

        file_path = os.getenv('FILE_PATH')
        file_uuid = file_path + str(uuid.uuid4()) + ".png"
        
        if pre_consume_info == None:
            draw_line_graph_single(cur_consume_info, file_uuid)
        else:
            draw_line_graph_dual(cur_consume_info, pre_consume_info, file_uuid)

        # jsonify
        return file_uuid, 200
    
    except Exception as e:
        global_logger.error(str(e), exc_info=True)
        return jsonify({'error': 'An error occurred: {}'.format(str(e))}), 500