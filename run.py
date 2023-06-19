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
gpt4_endpoint = "https://TODO.openai.azure.com/"            # Your endpoint will look something like  this: https://YOUR_AOAI_RESOURCE_NAME.openai.azure.com/
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
        template="{rag_from_manual} \n" +
                "## Question\n The above manual is for the ice cream machine at the restaurant. Write a quiz question for a new employee to test if they understand the above content. \n" +
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
        template="## Manual {excerpt} \n" +
                "## Quiz Question {quiz} \n" +
                "## User Answer {user_answer} \n" +
                "## Question\n Given the above chat history, is the employee's answer corrrect?  Write a short assessment of how they did. \n" +
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
    manual_text = "## Manual Winter Storage\n If the place of business is to be closed during the winter months, it is important to protect the freezer by following certain precautions, particularly if the building is subject to freezing conditions.  Important! On water-cooled freezers, disconnect the water supply. Relieve pressure on the spring in the water valve. Use air pressure on the outlet side to blow out any water remaining in the condenser. This is extremely important. Failure to follow this procedure may cause severe and costly damage to the refrigeration system. Your local Taylor distributor can perform this service for you.\n • Disconnect the freezer from the main power source to prevent possible electrical damage.\n • Wrap detachable parts of the freezer, such as the beater assembly and freezer door, and place them in a protected dry place. Rubber trim parts and gaskets can be protected by wrapping them with moisture-proof paper.\n • All parts should be thoroughly cleaned of dried mix or lubrication accumulations, which attract mice and other vermin."
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