import autogen
import panel as pn
from autogen import Agent, ConversableAgent
from autogen.coding import LocalCommandLineCodeExecutor

llm_config = {
    "cache_seed": 42,
    "temperature": 0,
    "config_list": [
        {
            "model": "gpt-4o-mini",
            "api_key": "yourapikey",
        }
    ],
    "timeout": 120,
}


system_message_admin = """
    As an AI assistant and the admin of a group chat, you relay the context
    received from the user without adding anything to the message.
    """

admin = ConversableAgent(
    name="Admin",
    human_input_mode="NEVER",
    code_execution_config=False,
    default_auto_reply="",
    llm_config=llm_config,
    system_message=system_message_admin,
)

system_message_translator = """
    As an AI assistant, you are equipped with a knowledge base of sample
    questions and answers.

    Your task is to interpret the user's message, understand the parameter
    they wish to modify, and respond with the appropriate Python dictionary.

    Please avoid including any reasoning in your output. Your response should
    solely consist of the Python dictionary.

    For instance, if a user inquires about the implications of changing the
    cost of 'my_band_1' to $1300, your response should be:
    new_costs_dict = {'my_band_1': 1300}.

    Similarly, if a user asks about the effects of changing the value of
    'my_band_2' to 3600, your response should be:
    new_values_dict = {'my_band_2': 3600}.

    If a user questions what would occur if the total budget is adjusted to
    10000, your response should be: new_budget_dict = {'budget': 10000}.

    If a user asks what happens if 'band1' and 'band2' are not incompatible,
    your response should be: new_incompatible = [('band1','band2')].

    In cases where the user poses multiple questions simultaneously,
    provide each dictionary as separate responses.
    """


translator = ConversableAgent(
    name="Translator",
    human_input_mode="NEVER",
    code_execution_config=False,
    default_auto_reply="",
    llm_config=llm_config,
    system_message=system_message_translator,
)

# Define a system message for the engineer role

system_message_engineer = """
    As a helpful AI Assistant, your task is to read the definitions of
    new_costs_dict, new_values_dict, new_budget_dict, and new_incompatible
    from the context you receive.

    You are to replace the corresponding lines in the code snippet below
    with the definitions from the context.

    Specifically, replace the new_costs_dict definition in the code with
    the new_costs_dict definition from the context. If the context you
    receive donot include new_costs_dict, then don't update the code.

    Specifically, replace the new_values_dict definition in the code with
    the new_values_dict definition from the context. If the context you
    receive donot include new_values_dict, then don't update the code.

    Specifically, replace the new_budget_dict_dict definition in the
    code with the new_budget_dict_dict definition from the context. If
    the context you receive donot include new_budget_dict_dict, then
    don't update the code.

    Specifically, replace the new_incompatible definition in the code
    with the new_incompatible definition from the context. If the context
    you receive donot include new_incompatible, then don't update the code.

    Please ensure that you only modify these specific lines in the code
    and leave the rest of the code unchanged.

    The following message includes a code block. Please refer to the
    code block below:


    ```python
    import pandas as pd
    import pulp
    from pulp import PULP_CBC_CMD


    def read_excel_data(filename):
        # Read the Excel file for bands and costs/values
        bands_df = pd.read_excel(filename, sheet_name="Inputs")
        incompatibilities_df = pd.read_excel(filename, sheet_name="Incompatibilities")
        budget_df = pd.read_excel(filename, sheet_name="Budget")

        # Extract the band names, costs, and values into lists
        bands = bands_df["Band"].tolist()
        costs = bands_df.set_index("Band")["Cost"].to_dict()
        values = bands_df.set_index("Band")["Value"].to_dict()
        budget = budget_df.iloc[0, 0]  # Assuming the budget is in the first cell

        # Extract the incompatibilities into a list of tuples where the 'Compatible' column is 'No'
        incompatibilities = [
            (row["Band1"], row["Band2"])
            for _, row in incompatibilities_df.iterrows()
            if row["Compatible"].strip().lower() == "no"
        ]

        return bands, costs, values, budget, incompatibilities


    def create_optimization_model(bands, costs, values, budget, incompatibilities):
        # Create a new LP problem
        festival_problem = pulp.LpProblem("MusicFestivalScheduling", pulp.LpMaximize)

        # Create variables: x[band] == 1 if the band is hired for the festival
        x = pulp.LpVariable.dicts("x", bands, cat="Binary")

        # Objective function: maximize the total expected audience draw
        festival_problem += pulp.lpSum([values[band] * x[band] for band in bands])

        # Constraint: the total cost of hiring bands must not exceed the festival's budget
        festival_problem += pulp.lpSum([costs[band] * x[band] for band in bands]) <= budget

        # Band incompatibility constraints: incompatible bands cannot both be hired
        for band1, band2 in incompatibilities:
            festival_problem += (
                x[band1] + x[band2] <= 1,
                f"Incompatibility_constraint_{band1}_{band2}",
            )

        return festival_problem, x


    def solve_optimization_problem(festival_problem, x, status='Original'):
        # Solve the problem
        festival_problem.solve(PULP_CBC_CMD(msg=False))


        # Print the solution

        if status=='Original':
            summary_head = 'Solution summary with original inputs'
        elif status=='Updated':
            summary_head = 'Solution summary with updated user inputs'

        print()
        print(summary_head,':')
        print()

        if pulp.LpStatus[festival_problem.status] == "Optimal":

            print(
                f"Maximum expected audience draw: {pulp.value(festival_problem.objective)}"
            )
            available_bands = bands
            hired_bands = [band for band in x if x[band].varValue > 0]

            total_cost = 0
            for current_hired_band in hired_bands:
                total_cost = total_cost + costs[current_hired_band]


            print("Available bands for the festival:", available_bands)
            print("Cost of bands used for this scenario",costs)
            print("Values of bands used for this scenario",values)
            print("Incompatible band pairs:", incompatibilities)
            print("Budget available for this scenario",budget)
            print("Total money used from budget for this scenario",total_cost)
            print("Bands hired for the festival:", hired_bands)

        else:
            print("No solution found")


    # Read data from Excel file
    filename = "festival_planning.xlsx"
    bands, costs, values, budget, incompatibilities = read_excel_data(filename)

    festival_problem, x = create_optimization_model(
        bands, costs, values, budget, incompatibilities
    )
    solve_optimization_problem(festival_problem, x, status='Original')


    new_costs_dict = dict()
    new_values_dict = dict()
    new_budget_dict = dict()
    new_incompatible = []

    # Update the costs and values with the new data

    if len(new_costs_dict) > 0:
        for band, cost in new_costs_dict.items():
            if band in costs:
                costs[band] = cost


    if len(new_values_dict) > 0:
        for band, value in new_values_dict.items():
            if band in values:
                values[band] = value

    if len(new_budget_dict) > 0:
    budget = new_budget_dict['budget']


    if len(new_incompatible) > 0:
        incompatibilities.extend(new_incompatible)


    festival_problem, x = create_optimization_model(
        bands, costs, values, budget, incompatibilities
    )
    solve_optimization_problem(festival_problem, x, status='Updated')


    ```
    Please provide the code snippet after the you inserted new definitions,
    please include all the code you have in your system message

    """


engineer = ConversableAgent(
    name="Engineer",
    max_consecutive_auto_reply=1,
    human_input_mode="NEVER",
    code_execution_config=False,
    default_auto_reply="",
    llm_config=llm_config,
    system_message=system_message_engineer,
)

# Define a system message for the executor role

system_message_code_executor = """
    As a helpful AI Assistant, your primary responsibility is to
    execute the code provided in the context.

    Please ensure that you do not make any additional modifications
    or add any comments before or after executing the code.

    Your role is strictly to run the code as it is.
    """

executor = ConversableAgent(
    name="Executor",
    max_consecutive_auto_reply=1,
    human_input_mode="NEVER",
    code_execution_config={
        "executor": LocalCommandLineCodeExecutor(timeout=10, work_dir="work_dir")
    },
    default_auto_reply="",
    llm_config=False,
    system_message=system_message_code_executor,
)

# Define a system message for the summarizer role

system_message_summarizer = """
    As an AI assistant, your role is to act as a summarizer.

    You need to summarize the history and identify what has been
    changed based on user input.

    In your summary, follow these steps:
    1.Explain what has been changed based on user input.
    2.Summarize the original scenario output.
    3.Summarize the updated scenario output.
    4.Compare the original and updated scenarios and make
    recommendations. Emphasize the changes in draw and cost.

    By following this structure, you will provide a clear and
    comprehensive summary of the changes and their implications.
    """

summarizer = ConversableAgent(
    name="Summarizer",
    max_consecutive_auto_reply=1,
    human_input_mode="NEVER",
    code_execution_config=False,
    default_auto_reply="",
    llm_config=llm_config,
    system_message=system_message_summarizer,
)


dummy = ConversableAgent(
    name="Dummy",
    max_consecutive_auto_reply=1,
    human_input_mode="NEVER",
    function_map=None,
    code_execution_config=False,
    default_auto_reply="",
    llm_config=llm_config,
)


# Define a custom function to select the next speaker in the group chat


def custom_speaker_selection_func(last_speaker: Agent, groupchat: autogen.GroupChat):
    # Retrieve the list of messages from the group chat
    messages = groupchat.messages

    # If there is only one or no messages, select the translator as the next speaker
    if len(messages) <= 1:
        return translator

    # Determine the next speaker based on the last speaker
    if last_speaker is admin:
        return (
            translator  # If the last speaker was admin, the next speaker is translator
        )
    elif last_speaker is translator:
        return (
            engineer  # If the last speaker was translator, the next speaker is engineer
        )
    elif last_speaker is engineer:
        return (
            executor  # If the last speaker was engineer, the next speaker is executor
        )
    elif last_speaker is executor:
        return summarizer  # If the last speaker was executor, the next speaker is summarizer
    elif last_speaker is summarizer:
        return dummy  # If the last speaker was summarizer, the next speaker is dummy


# Create a GroupChat instance with specified agents and configuration
groupchat = autogen.GroupChat(
    agents=[
        admin,
        translator,
        engineer,
        executor,
        summarizer,
        dummy,
    ],  # List of agents participating in the group chat
    messages=[],  # Initial list of messages, starting empty
    max_round=7,  # Maximum number of rounds for the chat
    speaker_selection_method=custom_speaker_selection_func,  # Function to select the speaker for each round
)

# Create a GroupChatManager instance to manage the group chat
manager = autogen.GroupChatManager(
    groupchat=groupchat,  # The GroupChat instance to be managed
    llm_config=llm_config,  # Configuration for the language model
)


# Define a dictionary to map user names to their corresponding avatars
avatar = {
    admin.name: "👨‍💼",  # Avatar for the admin
    translator.name: "👩",  # Avatar for the translator
    engineer.name: "👩‍💻",  # Avatar for the engineer
    executor.name: "🛠",  # Avatar for the executor
    summarizer.name: "😊",  # Avatar for the summarizer
    dummy.name: "👩‍🔬",  # Avatar for the dummy
}


# Define a function to print messages
def print_messages(recipient, messages, sender, config):
    # Check if the last message contains the key "name"

    if all(key in messages[-1] for key in ["name"]):
        # Send the message using the chat interface with the specified user and avatar
        chat_interface.send(
            messages[-1]["content"],  # The content of the last message
            user=messages[-1]["name"],  # The name of the user who sent the message
            avatar=avatar[messages[-1]["name"]],  # The avatar associated with the user
            respond=False,  # Do not expect a response
        )
    else:
        # Send the message using the chat interface with a default user and avatar
        chat_interface.send(
            messages[-1]["content"],  # The content of the last message
            user="SecretGuy",  # Default user name
            avatar="🥷",  # Default avatar
            respond=False,  # Do not expect a response
        )

    # Return a tuple indicating no further action is needed
    return False, None


# Register a reply function for the admin object
admin.register_reply(
    [autogen.Agent, None],  # List of agent types that this reply function will handle
    reply_func=print_messages,  # Function to call when a reply is received
    config={"callback": None},  # Configuration dictionary, with a callback set to None
)

# Register a reply function for the translator object
translator.register_reply(
    [autogen.Agent, None],  # List of agent types that this reply function will handle
    reply_func=print_messages,  # Function to call when a reply is received
    config={"callback": None},  # Configuration dictionary, with a callback set to None
)

# Register a reply function for the engineer object
engineer.register_reply(
    [autogen.Agent, None],  # List of agent types that this reply function will handle
    reply_func=print_messages,  # Function to call when a reply is received
    config={"callback": None},  # Configuration dictionary, with a callback set to None
)

# Register a reply function for the executor object
executor.register_reply(
    [autogen.Agent, None],  # List of agent types that this reply function will handle
    reply_func=print_messages,  # Function to call when a reply is received
    config={"callback": None},  # Configuration dictionary, with a callback set to None
)

# Register a reply function for the summarizer object
summarizer.register_reply(
    [autogen.Agent, None],  # List of agent types that this reply function will handle
    reply_func=print_messages,  # Function to call when a reply is received
    config={"callback": None},  # Configuration dictionary, with a callback set to None
)

# Register a reply function for the dummy object
dummy.register_reply(
    [autogen.Agent, None],  # List of agent types that this reply function will handle
    reply_func=print_messages,  # Function to call when a reply is received
    config={"callback": None},  # Configuration dictionary, with a callback set to None
)

# Extend Panel with the Material design theme
pn.extension(design="material")


# Define a callback function that will be triggered when a message is sent
def callback(contents: str, user: str, instance: pn.chat.ChatInterface):
    # Initiate a chat session with the provided message contents
    admin.initiate_chat(manager, message=contents)


# Create an instance of the ChatInterface with the callback function
chat_interface = pn.chat.ChatInterface(callback=callback)

# Send an initial message from the "System" user without expecting a response
chat_interface.send("Send a message!", user="System", respond=False)

# Make the chat interface servable, allowing it to be displayed in a web application
chat_interface.servable()
