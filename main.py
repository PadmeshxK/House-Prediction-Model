from flask import Flask,render_template,request
import pandas as pd
import pickle
import numpy as np

app = Flask(__name__)
data = pd.read_csv("cleaned_data.csv")
pipe = pickle.load(open('pickle_model.pkl','rb'))


@app.route('/')
def index():
    locations = sorted(data['AREA'].unique())
    sale_conds = sorted(data['SALE_COND'].unique())
    park_facils = sorted(data['PARK_FACIL'].unique())
    build_types = sorted(data['BUILDTYPE'].unique())
    utility_avails = sorted(data['UTILITY_AVAIL'].unique())
    streets = sorted(data['STREET'].unique())
    return render_template('index.html', locations=locations,sale_conds = sale_conds,park_facils = park_facils,build_types = build_types,utility_avails = utility_avails,streets = streets)

@app.route('/predict',methods=['POST'])
def predict():
    sqft = request.form.get('int_sqft')
    dist_mainroad = request.form.get('dist_mainroad')
    n_bedroom = request.form.get('n_bedroom')
    n_bathroom = request.form.get('n_bathroom')
    n_room = request.form.get('n_room')
    age = request.form.get('age')
    area = request.form.get('area')
    sale_cond = request.form.get('sale_cond')
    park_facil = request.form.get('park_facil')
    build_type = request.form.get('build_type')
    utility_avail = request.form.get('utility_avail')
    street = request.form.get('street')

    unique_areas = sorted(data['AREA'].unique())
    unique_areas = column_generator(unique_areas,area)

    unique_sales = sorted(data['SALE_COND'].unique())
    unique_sales = column_generator(unique_sales,sale_cond)

    unique_park = sorted(data['PARK_FACIL'].unique())
    unique_park = column_generator(unique_park,park_facil)

    unique_build = sorted(data['BUILDTYPE'].unique())
    unique_build = column_generator(unique_build,build_type)

    unique_utility = sorted(data['UTILITY_AVAIL'].unique())
    unique_utility = column_generator(unique_utility,utility_avail)

    unique_street = sorted(data['STREET'].unique())
    unique_street = column_generator(unique_street,street)

    sqft,dist_mainroad,n_bedroom,n_bathroom,n_room,age = handle_empty([sqft,dist_mainroad,n_bedroom,n_bathroom,n_room,age])

    dummy_cols = unique_areas + unique_sales + unique_park + unique_build + unique_utility + unique_street
    dataframe_input = [sqft , dist_mainroad ,n_bedroom, n_bathroom , n_room , age ] + dummy_cols
    
    input_data = pd.DataFrame([dataframe_input],columns=['INT_SQFT','DIST_MAINROAD','N_BEDROOM','N_BATHROOM','N_ROOM','AGE','AREA_Adyar','AREA_Anna Nagar','AREA_Chrompet','AREA_KK Nagar','AREA_Karapakam','AREA_T Nagar','AREA_Velachery','SALE_COND_AbNormal','SALE_COND_Adj Land','SALE_COND_Family','SALE_COND_Normal Sale','SALE_COND_Partial','PARK_FACIL_No','PARK_FACIL_Yes','BUILDTYPE_Commercial','BUILDTYPE_House','BUILDTYPE_Others','UTILITY_AVAIL_All Pub','UTILITY_AVAIL_ELO','UTILITY_AVAIL_NoSeWa',"UTILITY_AVAIL_NoSewr ",'STREET_Gravel','STREET_No Access','STREET_Paved'])
    prediction = pipe.predict(input_data)[0]


    return str(np.round(prediction,2))

def column_generator(values,user_input):
    for i in range(len(values)):
        if values[i] != user_input:
            values[i] = 0
        else:
            values[i] = 1
    return values

def handle_empty(data_list):
    for i in range(len(data_list)):
        if data_list[i] == "":
            data_list[i] = 0
        else:
            data_list[i] = int(data_list[i])

    return data_list

if __name__ == "__main__":
    app.run(debug=True,port = 5001)