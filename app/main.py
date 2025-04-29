from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.chat_completion_client_base import ChatCompletionClientBase
from semantic_kernel.contents import ChatHistory
import asyncio
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.functions import kernel_function
from pizza_plugin import PizzaPlugin
from semantic_kernel.connectors.ai.ollama import OllamaChatCompletion
from semantic_kernel.connectors.ai.ollama.ollama_prompt_execution_settings import OllamaChatPromptExecutionSettings

async def main():


    kernel = Kernel()

    kernel.add_plugin(PizzaPlugin(), plugin_name="OrderPizzaPlugin")

    ollama_connector = OllamaChatCompletion(service_id="ollama", ai_model_id="mistral-small3.1", host="http://localhost:11434")
    kernel.add_service(ollama_connector)
    
    chat_history = ChatHistory()
    chat_history.add_system_message("Your name is 'Pizzer' and you are a pizza ordering agent. You can order pizza for the user. You can also check the available pizzas at the moment, and additionally each users has the pizza wallet to order, you can check the balance amount in the wallet.")

    execution_settings = OllamaChatPromptExecutionSettings()
    execution_settings.function_choice_behavior = FunctionChoiceBehavior.Auto()
    
    while True:
        user_input = input("Enter your message >>> ")
        if user_input.lower() == "q":
            print("You pressed 'q' exiting the program")
            break
        chat_history.add_user_message(user_input)

        response = await ollama_connector.get_chat_message_content(
            chat_history=chat_history,
            settings=execution_settings,
            kernel=kernel,
        )

        response = str(response)

        chat_history.add_assistant_message(response)

        print("Response from agent >>> ", response)

if __name__ == "__main__":
    asyncio.run(main())