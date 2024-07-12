from utils.common_util import *
from utils.matplot_util import *
from import_data import *
from config import global_logger


# Graph related font settings. - Globally set.
font_prop = font_manager.FontProperties(fname="./data/font/BMDOHYEON_ttf.ttf").get_name()
plt.rc('font', family=font_prop)

app = Flask(__name__)

@app.route('/api/category', methods=['POST'])
def run_app():
    
    data = request.get_json()
    
    category_labels = data["title_vec"]
    category_size_labels = data["cost_vec"]
    start_dt = data["start_dt"]
    end_dt = data["end_dt"]
    total_cost = data["total_cost"]
    
    file_uuid = '/Users/we/Documents/work_code/consume_alert_rust/consume_alert_rust/data/pngs' + str(uuid.uuid4()) + ".png"
    
    visualize_consume_res_by_category(category_labels, category_size_labels, start_dt, end_dt, total_cost, file_uuid)
    
    # jsonify
    return file_uuid, 200