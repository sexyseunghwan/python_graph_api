from utils.common_util import *
from utils.matplot_util import *
from import_data import *
from config import global_logger


# Graph related font settings. - Globally set.
font_prop = font_manager.FontProperties(fname="./data/font/BMDOHYEON_ttf.ttf").get_name()
plt.rc('font', family=font_prop)

app = Flask(__name__)

@app.route('/api/data', methods=['POST'])
def run_app():
    
    data = request.get_json()
    
    print(data)
    category_labels = data["title_vec"]
    category_size_labels = data["cost_vec"]

    visualize_consume_res_by_category(category_labels, category_size_labels)
    #print(data["title_vec"])
    #print(data[""])

    global_logger.info("Python Telegram Bot Stop")

    return jsonify(data), 200