import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import plotly.graph_objects as go


gbr = joblib.load('totalcomp_undersampled_gbr_tuned.joblib')
locations = ['US', 'United Kingdom', 'India', 'Canada', 'San Francisco, CA', 'Seattle, WA', 'Sunnyvale, CA', 'Mountain View, CA', 'Redmond, WA', 'Menlo Park, CA', 'Cupertino, CA', 'New York, NY', 'San Jose, CA', 'Palo Alto, CA', 'Austin, TX', 'Boston, MA', 'Santa Clara, CA']
companies = ['oracle', 'ebay', 'amazon', 'apple', 'microsoft', 'salesforce', 'facebook', 'uber', 'google', 'netflix', 'pinterest', 'linkedin', 'adobe', 'intel', 'lyft', 'yelp', 'airbnb', 'sap', 'vmware', 'twitter', 'cisco', 'dropbox', 'ibm', 'walmart_labs', 'twilio', 'qualcomm', 'tesla', 'expedia', 'yahoo', 'intuit', 'bloomberg', 'yandex', 'capital_one', 'workday', 'splunk', 'samsung', 'autodesk', 'dell_technologies', 'box', 'booking.com', 'paypal', 'atlassian', 'indeed', 'shopify', 'accenture', 'nvidia', 'snap', 'square', 'nutanix', 'spotify', 'zillow', 'godaddy', 't-mobile', 'goldman_sachs', 'cruise', 'qualtrics', 'northrop_grumman', 'deloitte', 'jpmorgan_chase', 'wayfair', 'boeing', 'ernst_and_young', 'comcast', 'american_express', 'broadcom', 'general_motors', 'stripe', 'servicenow', 'visa', 'walmart', 'epam_systems', 'morgan_stanley', 'amd', 'doordash', 'instacart', 'lockheed_martin', 'pwc', 'bytedance']
titles = ['Product Manager', 'Software Engineer', 'Software Engineering Manager', 'Data Scientist', 'Solution Architect', 'Technical Program Manager', 'Hardware Engineer', 'Mechanical Engineer']
degrees = ["Unknown_degree", "Highschool", "Some College", "Bachelor's Degree", "Master's Degree", "PhD"]


# Create title and sidebar
st.title("STEM Salary Predictor")
company = st.sidebar.selectbox('Company:', companies)
title = st.sidebar.selectbox('Title:', titles)
year = st.sidebar.slider('Year of Experience:', 0, 10, 0)
degree = st.sidebar.selectbox('Degree:', degrees)
location = st.sidebar.selectbox('Location', locations)

def predict(company, role, year, yearsAtCompany, location, education):
    loc_lst = []
    for loc in locations:
        if loc == location:
            loc_lst.append(1)
        else:
            loc_lst.append(0)

    comp_lst = []
    for comp in companies:
        if comp == company:
            comp_lst.append(1)
        else:
            comp_lst.append(0)

    role_lst = []
    for rol in titles:
        if role == rol:
            role_lst.append(1)
        else:
            role_lst.append(0)

    degree = degrees.index(education)
    
    input = []
    input.append(year)
    input.append(yearsAtCompany) #years at company
    input.append(degree)
    input.extend(loc_lst)
    input.extend(role_lst)
    input.extend(comp_lst)

    df = pd.DataFrame([input])
    return gbr.predict(df)

if st.button("Click Here to Predict"):
    all = []
    x = [0,1,2,3,4]
    compare = ['facebook', 'amazon', 'google', 'microsoft']
    if company not in compare:
        compare.append(company)

    for j in compare:
        y = []
        yearsAtCompany = 0
        for i in x:
            y.extend(predict(j, title, int(year) + i, 0, location, degree))
        print(y)
        all.append(y)

    result = predict(company, title, year, 0, location, degree)

    group_labels = compare

    fig = go.Figure()
    for arr in all:
        
        fig.add_trace(go.Scatter(x=x, y=arr,
                            mode='lines',
                            name=compare[all.index(arr)]))

    st.header('Your predicted total package is $' + str("{:,}".format(int(result[0]))) + ' per year!')
    st.write('See how your salary will grow and how much you can earn from other companies:')
    # Plot!
    st.plotly_chart(fig, use_container_width=True)

