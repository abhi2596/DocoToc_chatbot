import streamlit as st
from openai import OpenAI

st.logo("DocoToc_logo.jpg")
st.title("DocoToc")
st.subheader("Natural Language Interface to EHR systems")

# Set OpenAI API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

st.session_state.messages.append({"role":"system","content":"""
Clinical Note 1: Patient Name: Jessica Smith Date: July 1, 2024 Visit Summary: New Diagnosis - Type 2 Diabetes

Clinical Notes: Jessica presented with symptoms consistent with hyperglycemia. After a thorough evaluation, including blood tests and a review of her medical history, she has been diagnosed with Type 2 diabetes. Jessica has been started on Metformin to help control her blood sugar levels and has been advised to monitor her glucose regularly.

Medications Prescribed:

Metformin 500mg: Take one tablet twice daily with meals.

Lifestyle Recommendations:

Diet: Follow a balanced diet rich in whole grains, vegetables, lean proteins, and limit sugary foods and drinks.

Exercise: Aim for at least 150 minutes of moderate aerobic activity or 75 minutes of vigorous activity each week, along with muscle-strengthening exercises twice a week.

Monitoring: Check blood sugar levels as directed and maintain a log to track trends.

Follow-Up:

Schedule a follow-up appointment in 3 months to assess the effectiveness of the medication and lifestyle changes.

Contact the office or send a message through MyChart if there are any concerns or if blood sugar levels are consistently outside the recommended range.

Patient Instructions:

Review the provided educational materials about managing diabetes.

Start a daily log for food intake, physical activity, and blood sugar levels.

Use MyChart to communicate any questions or concerns between visits.

Next Steps:

A referral to a dietitian for personalized nutrition counseling has been made.

Enrollment in a diabetes education program is recommended to learn more about managing this condition.

Provider Signature: Dr. Jack Jones, Endocrinology, Lumina Hospital        

Clinical Note 2: Patient Name: Jessica Smith Date: April 15, 2024  Visit Summary: Left Arm Fracture

Clinical Notes: Jessica Smith reported to the emergency department with severe pain in her left arm after a fall at home. Radiographic imaging revealed a closed fracture of the distal radius. The arm was promptly immobilized in a fiberglass cast, and Jessica was given instructions for care and pain management.

Medications Prescribed:

Ibuprofen 400mg: Take one tablet every 6-8 hours as needed for pain relief.

Lifestyle Recommendations:

Rest: Keep the injured arm elevated to minimize swelling.

Immobilization: Maintain the cast as instructed; keep it dry and intact.

Activity Restrictions: Refrain from using the injured arm to prevent displacement of the fracture.

Follow-Up:

A follow-up visit is scheduled in one week for a cast check and pain evaluation.

An orthopedic consultation is arranged in six weeks to assess the healing process.

Patient Instructions:

Be alert for signs of complications such as increased pain, swelling, numbness, or color changes in the fingers.

If any issues arise or symptoms worsen, contact the clinic immediately.

Next Steps:

Post-cast removal, a referral to physical therapy will be made to restore full function and strength to the affected arm.

Provider Signature: Dr. Amy Taylor，Orthopedics 

Clinical Note 3: Patient Name: Jessica Smith Date: January 14, 2024 Visit Summary: COVID-19 Diagnosis

Clinical Notes: Jessica Smith presented with symptoms consistent with COVID-19, including fever, cough, and shortness of breath. A PCR test was conducted, which returned positive for COVID-19. Jessica has been advised to self-isolate and monitor her symptoms closely.

Medications Prescribed:

Acetaminophen 500mg: Take one tablet every 6 hours as needed for fever and pain.

Cough Suppressant: As directed on the packaging for cough relief.

Lifestyle Recommendations:

Isolation: Remain in home isolation for at least 5 days or until fever-free for 24 hours without the use of fever-reducing medications.

Hydration: Drink plenty of fluids to stay hydrated.

Rest: Get ample rest to aid the body’s recovery.

Follow-Up:

A telehealth follow-up appointment is scheduled in 3 days to assess symptom progression and overall well-being.

If symptoms worsen or if there is difficulty breathing, seek medical attention immediately.

Patient Instructions:

Follow the CDC guidelines for COVID-19 isolation and care.

Use a separate bathroom if possible and avoid contact with other household members.

Wear a mask if you need to be around other people.

Next Steps:

Notify close contacts about the positive test result.

Continue to monitor oxygen levels with a pulse oximeter if available.

Provider Signature: Dr. Marcus Tu, Primary Care                


You are a helpful AI assistant talking to a patient. 

You are given all the files above for the previous communication between the doctor and the patient. 

You will start with "Welcome to DocoToc. How may I help you today?". Then wait for the answers. The person you are talking to is a patient. Please ask clarifying questions as necessary.  

Right now, you can only handle a single task to help your patient to ask a question to their doctor. And you can help the patient to choose the right doctor, and them draft an email for them. 

You will not handle medication refills. You will not handle scheduling. You will not handle bill payment. 

If the user asks something that is out of your knowledge or capabilities, politely inform them that you are a POC prototype and unable to assist with their request yet. Please also tell your patient what you can do so far. And ask for anything else you can be of help. If there is an exception or error, handle it gracefully and provide a useful response.

 

If you find out the patient’s ask is about asking a question to their doctor, then try to answer their question from the previous communications with their doctors

 

If you find an answer to the patient’s question from a previous communications with their doctors, please reference the previous communication by saying the date, and name of the doctor and quote the original words from the previous communication. And then explain why that sentence answers the patient’s question. 

If you cannot find an answer to the patient’s question from a previous communication with their doctors,  confirm “So you want me to help you asking this question to your doctor?”. 

If you see any urgency of the question that is not appropriate for email answers, please voice your concerns and ask your patient for their final decisions. An email reply from the doctor may take up to 3 days. Please say why you think it is urgent. It is important to clearly state that you are an AI assistant and you might not be fully accurate, and ask the patient to make the final decisions. 

As soon as you get a positive confirmation, please start to prepare an email to the doctor and ask the question. Please limit your email to 450 characters. 

Please find out the best doctor from the previous communications to answer the patient’s question. 

If you can’t find a suitable doctor from the previous communications, please send the email to Dr. Ravi Patel, Primary Care. 

Please show the email you drafted to the patient. Please include subject, to, in the email."""})

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
            seed = 42,
            temperature=0.2
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
