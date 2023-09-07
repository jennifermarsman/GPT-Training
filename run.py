import gradio as gr
from langchain.chat_models import AzureChatOpenAI
from langchain.prompts import (
    PromptTemplate,
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

# Constants for calling the Azure OpenAI service
openai_api_type = "azure"
gpt4_endpoint = "https://TODO.openai.azure.com/"            # Your endpoint will look something like this: https://YOUR_AOAI_RESOURCE_NAME.openai.azure.com/
gpt4_api_key = "TODO"                                       # Your key will look something like this: 00000000000000000000000000000000
gpt4_deployment_name="gpt-4"

# Create instance to call GPT-4
gpt4 = AzureChatOpenAI(
    openai_api_base=gpt4_endpoint,
    openai_api_version="2023-03-15-preview",
    deployment_name=gpt4_deployment_name,
    openai_api_key=gpt4_api_key,
    openai_api_type = openai_api_type,
)

def generate_quiz(rag_from_manual):
    system_template="Your role is a trainer to help new employees learn their job working at a restaurant.  You generate a multiple-choice quiz question to train an employee, when given information from the equipment manuals and employee guidebooks.\n"
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)

    user_prompt=PromptTemplate(
        template="## Manual \n {rag_from_manual} \n" +
                "## Question \n The above manual is for equipment used at the restaurant. Write a quiz question for a new employee to test if they understand the above content. The multiple choice question should have only one correct answer.\n" +
                "## Quiz Question \n",
        input_variables=["rag_from_manual"],
    )
    human_message_prompt = HumanMessagePromptTemplate(prompt=user_prompt)
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

    # Get formatted messages for the chat completion
    messages = chat_prompt.format_prompt(rag_from_manual={rag_from_manual}).to_messages()
    print("Messages")
    print(messages)

    # Call the model
    output = gpt4(messages)
    print("Output")
    print(output)
    return output.content

def evaluate_quiz(excerpt, quiz, user_answer):
    system_template="Your role is a quiz checker to help new employees learn their job working at a restaurant.  You evaluate a multiple-choice quiz question to train an employee and the employee's answer, and provide feedback.  You should compliment where they do something right and gently correct where they mess up.\n"
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)

    user_prompt=PromptTemplate(
        template="## Manual \n {excerpt} \n" +
                "## Quiz Question \n {quiz} \n" +
                "## User Answer \n {user_answer} \n" +
                "## Question \n Given the above chat history, is the employee's answer correct?  Write a short assessment of how they did. \n" +
                "## Assessment \n",
        input_variables=["excerpt", "quiz", "user_answer"],
    )
    human_message_prompt = HumanMessagePromptTemplate(prompt=user_prompt)
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

    # Get formatted messages for the chat completion
    messages = chat_prompt.format_prompt(excerpt={excerpt}, quiz={quiz}, user_answer={user_answer}).to_messages()
    print("Messages")
    print(messages)
    
    # Call the model
    output = gpt4(messages)
    print("Output")
    print(output)
    return output.content


with gr.Blocks(css=".gradio-label {color: red}") as demo:
    # Manual for a deep fryer: https://static-pt.com/modelManual/SOU-14-18_spm.pdf?v=1532002599167  (page 13)
    manual_text = "SOME DO’S AND DON’TS OF GOOD FRYING PRACTICES\n\nFRYING DO’S\n1. Make sure kettles are clean. \n2. Make sure thermostats are registering and functioning properly. \n3. Fill kettles only to proper frying level, which is 2% above the tubes when the frying fat is at frying temperature. A fry level line is stamped on the tank. \n4. Maintain proper level of frying fat in the kettle by occasional additions of fresh fat as the kettle fries down. \n5. Keep heating tubes covered at all times when heat is on. \n6. Fry at temperatures in the range of 325°F to 375°F. \n7. Turn heat in the kettles to 200”F, or preferable off between frying periods, or during any periods of time when this is practical. \n8. Fry foods in amounts only up to a full kettle load; a full kettle loading being the point where the temperature recovers to the dial setting and the thermostat turns off the burner before the food is completely fried or done. \n9. Remove food baskets from kettle as soon as food is done, allowing food to drain over kettle a minimum of 30 seconds. \n10. Keep fat as clean as possible at all times, removing immediately any floating burned particles. \n11. Make sure baskets are sound and don’t leak food into kettle. \n12. Drain kettle, filter fat and remove all residue from cold zone at least once daily. Boil out kettle and baskets with detergent at least once a week, scraping off any foreign materials not yielding to the treatment. Rinse kettle several times by filling with fresh water and bring to boil. Follow procedure under “MAINTENANCE” section. \n13. Keep kettles covered when not in use. \n\n FRYING DON’TS \n1. Don’t overfill the kettle; above line on rear of tank. \n2. Don’t allow fat in kettle to fry down to the point where there is insufficient fat in which to fry a full load. \n3. Don’t have heat on tubes when they are not entirely covered with frying fat. \n4. Don’t allow fat in kettle to be heated above 375°F and never turn thermostats to 400°F or over, even when bringing up to temperature. \n5. Don’t allow unnecessary moisture or breading material to get into frying kettle. \n6. Don’t allow fat in kettles to remain at frying temperature for long periods of time without frying taking place. \n7. Don’t overload frying kettle with food to be fried. \n8. Don’t pack the food too tightly in the baskets. \n9. Don’t add foreign fats to kettle such as bacon, beef drippings, or waste fat. \n10. Don’t fry bacon in deep frying kettle. \n11. Don’t salt foods over or near the frying kettle. \n12. Don’t allow visible burned particles to remain floating in fry kettle. \n13. Don’t allow exhaust stack accumulations to drip back into the kettle."

    with gr.Row():
        with gr.Column(scale=1):
            gr.Image(value="logo.png", show_label=False, interactive=False)
        with gr.Column(scale=9):
            gr.Markdown(value = "## Dynamic Training")
            gr.Markdown(value = "Training of new employees can be a costly endeavor.  This demonstration uses GPT-4 to generate a quiz question for a new employee, given a manual excerpt.  The employee can then answer the quiz question, and the AI will evaluate the answer and provide feedback.  This can be used to train new employees on the job, and to evaluate their understanding of the material.\n\nNote that the manual excerpt is shown here for demonstration purposes, but in a real-world application, the manual excerpt would be hidden from the employee.  You are also not limited to one short excerpt; code can iterate over a manual or group of documents and generate many questions on the material.")
    with gr.Row():
        with gr.Column():
            excerpt = gr.Textbox(label = "Excerpt from manual", value=manual_text, lines=20)
            btn_Quiz = gr.Button("Generate Quiz Question")
        with gr.Column():
            quiz = gr.Textbox(label = "AI-generated quiz question", lines=5)
            user_answer = gr.Textbox(label = "Your answer", lines=1)
            btn_Check = gr.Button("Check Answer")
            assessment = gr.Textbox(label = "AI-generated assessment", lines=5)
    
    btn_Quiz.click(fn=generate_quiz, inputs=excerpt, outputs=quiz)
    btn_Check.click(fn=evaluate_quiz, inputs=[excerpt, quiz, user_answer], outputs=assessment)

demo.launch()