import streamlit as st
from PIL import Image
from streamlit_option_menu import option_menu
import re
import base64
from fpdf import FPDF
from fastai.vision.all import *
import pathlib
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath
import mysql.connector

# Connect to the MySQL database
try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345678",
        database="alzheimers"
    )
    print("Database connection successful")
except mysql.connector.Error as err:
    print("Error connecting to database:", err)
    exit(1)
# Get a cursor object to execute SQL queries
mycursor = mydb.cursor()
#generating csv file
def generate_csv():
    # Execute SQL query to fetch data from the database
    mycursor.execute("SELECT * FROM predictions")

    # Fetch all rows from the result
    rows = mycursor.fetchall()

    # Define the CSV file path
    csv_file_path = "./data/patients_data.csv"

    # Write the data to the CSV file
    with open(csv_file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([i[0] for i in mycursor.description])  # Write header row
        writer.writerows(rows)  # Write data rows

    st.success("CSV file generated successfully!")


st.markdown("""
<style>
    button.step-up {display: none;}
    button.step-down {display: none;}
    div[data-baseweb] {border-radius: 4px;}
</style>""",
unsafe_allow_html=True)

def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-position: center;
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)
set_background('./images/bg3.png')

# load the trained model
# load the trained model
model_path = './models/my_model.h5'
learn_inf = load_learner(model_path)




# define a function to predict Alzheimer's disease
def predict_alzheimer(image):
    img = PILImage.create(image)
    prediction = learn_inf.predict(img)[0]
    return prediction


# Define the class labels
class_labels = ['Mild Demented', 'Moderate Demented',
                'Non Demented', 'Very Mild Demented']


def validate_phone_number(phone_number):
    """
    Validates that a phone number is a 10-digit number.
    """
    pattern = r'^\d{10}$'
    contact=re.match(pattern, str(phone_number))
    if not contact:
        st.error('Please enter a 10 digit number!')
        return False
    return True

def validate_name(name):
    if not all(char.isalpha() or char.isspace() for char in name):
        st.error("Name should not contain numbers or special character.")
        return False
    return True

def validate_input(name, age,contact,file):
    if not name:
        st.error('Please enter the patients name!')
        return False
    if not age:
        st.error('Please enter your age!')
        return False
    if not contact:
        st.error('Please enter your contact number!')
        return False
    if not file:
        st.error('Please upload the MRi Scan!')
        return False
    return True
#with st.sidebar:
selected = option_menu(
            menu_title=None,  # required
            options=["Home", "Alzhiemer Detection", "About US"],  # required
            icons=["house", "book", "envelope"],  # optional
            menu_icon="cast",  # optional
            default_index=0,  # optional
            orientation="horizontal",
        )

if selected =='Home':
    def app():
        st.markdown('<p class="my-font1"><h2>Alzheimer\'s Disease</h2></p>', unsafe_allow_html=True)
        st.markdown('<p class="my-font2">&nbsp Alzheimer disease is the most common type of dementia. It is a progressive disease beginning with mild memory loss and possibly leading to loss of the ability to carry on a conversation and respond to the environment. Alzheimer disease involves parts of the brain that control thought, memory, and language.</p>', unsafe_allow_html=True)
        st.markdown('<p class="my-font2">&nbsp Using this website, you can find out that does your MRI scan have Alzheimer\'s disease. It is classified according to four different stages of Alzheimer\'s disease.</p>', unsafe_allow_html=True)
        st.markdown('<p class="my-font2">1. Mild Demented<br> 2. Very Mild Demented<br> 3. Moderate Demented<br> 4. Non Demented</p>', unsafe_allow_html=True)
    
        st.markdown('<p class="my-font1"><h2>Treatment for Mild to Moderate Alzheimer’s</h2></p>', unsafe_allow_html=True)
        st.markdown('<p class="my-font2">&nbsp Treating the symptoms of Alzheimer’s can provide people with comfort, dignity, and independence for a longer period of time and can encourage and assist their caregivers as well. Galantamine, rivastigmine, and donepezil are cholinesterase inhibitors that are prescribed for mild to moderate Alzheimer’s symptoms. These drugs may help reduce or control some cognitive and behavioral symptoms.</p>', unsafe_allow_html=True)
        st.markdown('<p class="my-font2">&nbsp Scientists do not yet fully understand how cholinesterase inhibitors work to treat Alzheimer’s disease, but research indicates that they prevent the breakdown of acetylcholine, a brain chemical believed to be important for memory and thinking. As Alzheimer’s progresses, the brain produces less and less acetylcholine, so these medicines may eventually lose their effect. Because cholinesterase inhibitors work in a similar way, switching from one to another may not produce significantly different results, but a person living with Alzheimer’s may respond better to one drug versus another.</p>', unsafe_allow_html=True)
        st.markdown('<p class="my-font2">&nbsp Medications that target the underlying causes of a disease are called disease-modifying drugs or therapies. Aducanumab is the only disease-modifying medication currently approved to treat Alzheimer’s. This medication is a human antibody, or immunotherapy, that targets the protein beta-amyloid and helps to reduce amyloid plaques, which are brain lesions associated with Alzheimer’s. Clinical studies to determine the effectiveness of aducanumab were conducted only in people with early-stage Alzheimer’s or mild cognitive impairment. Researchers are continuing to study whether this medication works to affect a person’s rate of cognitive decline over time.</p>', unsafe_allow_html=True)
        st.markdown('<p class="my-font2">&nbsp Before prescribing aducanumab, doctors may require PET scans or an analysis of cerebrospinal fluid to evaluate whether amyloid deposits are present in the brain. This can help doctors make an accurate diagnosis of Alzheimer’s before prescribing the medication. Once a person is on aducanumab, their doctor or specialist may require routine MRIs to monitor for side effects such as brain swelling or bleeding in the brain.</p>', unsafe_allow_html=True)
        
        st.markdown('<p class="my-font1"><h2>Treatment for Moderate to Severe Alzheimer’s</h2></p>', unsafe_allow_html=True)
        st.markdown('<p class="my-font2">&nbsp A medication known as memantine, an N-methyl D-aspartate (NMDA) antagonist, is prescribed to treat moderate to severe Alzheimer’s disease. This drug’s main effect is to decrease symptoms, which could enable some people to maintain certain daily functions a little longer than they would without the medication. For example, memantine may help a person in the later stages of the disease maintain his or her ability to use the bathroom independently for several more months, a benefit for both the person with Alzheimer\'s and caregivers.</p>', unsafe_allow_html=True)
        st.markdown('<p class="my-font2">&nbsp Memantine is believed to work by regulating glutamate, an important brain chemical. When produced in excessive amounts, glutamate may lead to brain cell death. Because NMDA antagonists work differently from cholinesterase inhibitors, the two types of drugs can be prescribed in combination.</p>', unsafe_allow_html=True)
        st.markdown('<p class="my-font2">&nbsp The FDA has also approved donepezil, the rivastigmine patch, and a combination medication of memantine and donepezil for the treatment of moderate to severe Alzheimer’s.</p>', unsafe_allow_html=True)
        
    
        st.markdown('<p class="my-font1"><h2>Generate CSV from MySQL Database</h2></p>', unsafe_allow_html=True)
        # Adding CSS styles for the button
        st.markdown("""
            <style>
            .stButton>button {
                background-color: #FF0000;
                color: white;
                transition: background-color 0.3s;
            }

            .stButton>button:hover {
                background-color: #00FA9A;
            }
            </style>
        """, unsafe_allow_html=True)

        # Adding a button
        if st.button("Generate CSV"):
            generate_csv()

if selected =='About US':
    def app():
        st.markdown('<p class="my-font1"><h2>ALZHEIMER’S AND DEMENTIA DISEASE DETECTION FROM BRAIN MRI DATA</h2></p>', unsafe_allow_html=True)
        st.markdown('<p class="my-font2">&nbsp Welcome to our platform dedicated to Alzheimer\'s and Dementia Disease Detection from Brain MRI Data. We understand the importance of early detection and accurate diagnosis when it comes to these neurodegenerative diseases. Our mission is to provide advanced tools and techniques that aid in the early identification of Alzheimer\'s and Dementia by analyzing brain MRI data.</p>', unsafe_allow_html=True)

        st.markdown('<p class="my-font2">&nbsp At our core, we are a team of dedicated researchers, data scientists, and medical professionals who are passionate about making a positive impact in the field of neurology. We believe that through the power of advanced imaging technology and data analysis, we can improve the accuracy and efficiency of Alzheimer\'s and Dementia diagnosis.</p>', unsafe_allow_html=True)

        st.markdown('<p class="my-font2">&nbsp Our platform utilizes state-of-the-art machine learning algorithms and image processing techniques to analyze brain MRI scans. By leveraging the vast amount of data available and applying cutting-edge methodologies, we aim to develop reliable and robust models for early detection and classification of Alzheimer\'s and Dementia.</p>', unsafe_allow_html=True)

        st.markdown('<p class="my-font2">&nbsp We are committed to transparency and collaboration. We work closely with medical professionals, researchers, and institutions to validate our findings and ensure the highest level of accuracy and credibility in our results. Our platform also provides a user-friendly interface, making it accessible to healthcare professionals and researchers alike.</p>', unsafe_allow_html=True)

        st.markdown('<p class="my-font2">&nbsp Through our efforts, we hope to contribute to the early identification of Alzheimer\'s and Dementia, enabling timely interventions and personalized treatment plans. By detecting these diseases at their earliest stages, we strive to improve patient outcomes and enhance the quality of life for individuals and their families affected by Alzheimer\'s and Dementia.</p>', unsafe_allow_html=True)

        st.markdown('<p class="my-font2">&nbsp Thank you for joining us on this important journey as we continue to push the boundaries of medical research and technology to make a meaningful difference in the fight against Alzheimer\'s and Dementia.</p>', unsafe_allow_html=True)


# create a Streamlit web application
if selected=='Alzhiemer Detection':
    def app():
        st.markdown('<p class="my-font1"><h2>Alzheimer\'s Disease Detection</h2></p>', unsafe_allow_html=True)
        st.markdown('<p class="my-font2">Upload an MRI scan of the brain to predict Alzheimer\'s disease</p>', unsafe_allow_html=True)



        with st.form(key='myform', clear_on_submit=True):
            name = st.text_input('Name')
            age = st.number_input('Age', min_value=1, max_value=150, value=40)
            gender = st.radio('Gender', ('Male', 'Female','Other'))
            contact = st.text_input('Contact Number', value='', key='contact')
            file_upload = st.file_uploader("Upload an image", type=['jpg', 'jpeg', 'png'])
            submit=st.form_submit_button("Submit")

        def insert_data(name, age, gender, contact, prediction):
            try:
                sql = "INSERT INTO predictions (Patient_Name, Age, Gender, Contact, Prediction) VALUES (%s, %s, %s, %s, %s)"
                val = (name, age, gender, contact, prediction)
                mycursor.execute(sql, val)
                mydb.commit()
                print(mycursor.rowcount, "record inserted")
            except mysql.connector.Error as err:
                print("Error inserting record:", err) 


        if file_upload is not None and validate_input(name, age,contact,file_upload) and validate_phone_number(contact) and validate_name(name):
            st.success('Your personal information has been recorded.', icon="✅")
            image = Image.open(file_upload)
            

            png_image = image.convert('RGBA')
            st.image(image, caption='Uploaded MRI scan', use_column_width=True)
            st.write('Name:', name)
            st.write('Age:', age) 
            st.write('Gender:', gender)
            st.write('Contact:', contact)

            #image = preprocess_image(image)
            prediction = predict_alzheimer(image)
           # prediction = np.argmax(prediction, axis=1)           
            #st.write(predictions)
            st.success('The predicted class is: '+ prediction)
            result_str = 'Name: {}\nAge: {}\nGender: {}\nContact: {}\nPrediction for Alzheimer: {}'.format(
                name, age, gender, contact, prediction)
            insert_data(name, age, gender, contact, prediction)
            export_as_pdf = st.button("Export Report")

            def create_download_link(val, filename):
                b64 = base64.b64encode(val)  # val looks like b'...'
                return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}.pdf">Download file</a>'

            if export_as_pdf:
                pdf = FPDF()
                pdf.add_page()
                # set the border style
                pdf.set_draw_color(0, 0, 0)
                pdf.set_line_width(1)

                # add a border to the entire page
                pdf.rect(5.0, 5.0, 200.0, 287.0, 'D')

                # Set font for title
                pdf.set_font('Times', 'B', 24)
                pdf.cell(200, 20, 'Alzheimer Detection Report', 0, 1, 'C')

                # Set font for section headers
                pdf.set_font('Arial', 'B', 16)
                pdf.cell(200, 10, 'Patient Details', 0, 1)

                # Set font for regular text
                pdf.set_font('Arial', '', 12)
                pdf.cell(200, 10, f'Name: {name}', 0, 1)
                pdf.cell(200, 10, f'Age: {age}', 0, 1)
                pdf.cell(200, 10, f'Gender: {gender}', 0, 1)
                pdf.cell(200, 10, f'Contact: {contact}', 0, 1)
                pdf.ln(0.15)
                pdf.ln(0.15)



                # Add the image to the PDF object's images dictionary
                png_file = "image.png"
                png_image.save(png_file, "PNG")
                pdf.cell(200, 10, 'MRI scan:', 0, 1)
                pdf.image(png_file, x=40, y=80, w=50,h=50)
                pdf.ln(0.15)
                pdf.ln(10.0)
                pdf.ln(10.0)
                pdf.ln(10.15)
                pdf.ln(10.15)
                pdf.ln(1.15)
                pdf.ln(1.15)
                pdf.ln(1.15)

                # Set font for prediction text
                pdf.set_font('Arial', 'B', 16)
                pdf.cell(200, 10, f'Prediction for Alzheimer: {prediction}', 0, 1)
                pdf.ln(2.0)
                pdf.set_font('Arial', 'B', 12)
                if (prediction!='NonDemented'):
                    pdf.set_text_color(255, 0, 0)
                    pdf.cell(200,10,'Demetia detected in your MRI, kindly consult a nearby neurologist immediately!',0,1)
                    pdf.set_text_color(0, 0, 255)
                    pdf.set_font('Arial', 'B', 10)
                    pdf.cell(200, 10, 'Here are some precautions you can take:', 0, 1, 'C')
                    pdf.ln(2)

                    precautions = [
                    '1. Stay mentally active: Engage in mentally stimulating activities such as reading, writing, puzzles, and games to keep your brain active.',
                    '2. Stay physically active: Exercise regularly to improve blood flow to the brain and help prevent cognitive decline.',
                    '3. Eat a healthy diet: Eat a balanced diet that is rich in fruits, vegetables, whole grains, and lean protein to help maintain brain health.',
                    '4. Stay socially active: Engage in social activities and maintain social connections to help prevent social isolation and depression.',
                    '5. Get enough sleep: Aim for 7-8 hours of sleep per night to help improve brain function and prevent cognitive decline.'                ]

                    pdf.set_font('Arial', '', 12)

                    for precaution in precautions:
                        pdf.multi_cell(190, 10, precaution, 0, 1, 'L')
                        pdf.ln(1)

                else:
                    pdf.set_text_color(0, 255, 0)
                    pdf.cell(200,10,'Congratulations! There is no sign of demetia in your MRI.',0,1)

                # Create and display the download link
                html = create_download_link(pdf.output(dest="S").encode("latin-1"), "test")
                st.markdown(html, unsafe_allow_html=True)





if __name__ == '__main__':
    st.markdown(
    """
        <style>
        .my-font1 {
            font-family: Verdana;
            font-size: 16px;
            font-weight: bold;
            color: #333333;
            /* Add any other desired CSS properties for font style */
        }
        .my-font2 {
            font-family: Times New Roman;
            font-size: 16px;
            font-weight: null;
            color: #333333;
            /* Add any other desired CSS properties for font style */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    app()
