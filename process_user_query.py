from groq import Groq 


class GroqClient:
    def __init__(self, API_KEY=None):
        self.client = Groq(
            api_key=API_KEY
        )
        self.conversation_history = []

    def _get_prompt(self):
        return """You are an assistant designed to process user queries about company performance metrics. The user will ask about a company's performance over a specific time period. Your task is to **only return the response in the following JSON format**. The output should **not include any explanations, clarifications, or additional text**. Only the exact JSON response should be returned.
            Output should be strictly in the following JSON format:

            ```json
            {
            "entity": "<company_name>",
            "parameter": "<performance_metric>",
            "start_date": "<YYYY-MM-DD>",
            "end_date": "<YYYY-MM-DD>"
            }

            """

    def get_completion(self, model, user_message):
        try:
            self.conversation_history.append({"role": "user", "content": user_message})
            # Request a completion from the model
            prompt = self._get_prompt()
            print(prompt)
            prompt = prompt.replace("<user_query>", user_message)

            completion = self.client.chat.completions.create(
                model=model,
                messages=self.conversation_history,  # Pass the entire conversation history
            )

            result = ""
            if completion and hasattr(completion, "choices") and completion.choices:
                content = completion.choices[0].message.content
                result += content

            self.conversation_history.append(
                {"role": "assistant", "content": content}
            )  # add the output reaply of ther assignt
            # Return the final result
            return result

        except Exception as e:
            return f"Error: {str(e)}"


# Example usage
if __name__ == "__main__":
    groq_client = GroqClient()
    print("Welcome! You can start querying now.")

    while True:
        user_query = input("Enter your query (or type 'exit' to end): ")

        if user_query.lower() == "exit":
            print("Ending conversation.")
            break

        response = groq_client.get_completion(
            model="llama3-70b-8192", user_message=user_query
        )

        print(f"Response: {response}")
