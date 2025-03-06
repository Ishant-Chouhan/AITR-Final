import google.generativeai as genai

genai.configure(api_key="AIzaSyC3pCAiP_jYxMrYO8C6alZzCYTrP11EE8A")

context=""" i am giving you a complent that is "there was a bus driver driving rushly" give priority for the department to perform execution on it  like is it an emergency, moderate or less priority, give in one word """
def chat(context):
    response = genai.GenerativeModel("gemini-1.5-flash").generate_content(context)
    ans=response.text
    return ans