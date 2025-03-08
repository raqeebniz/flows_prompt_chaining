from crewai.flow.flow import Flow, start, listen
from litellm import completion
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")



class TopicOutlineFlow(Flow):
    model = "gemini/gemini-1.5-flash"

    @start()
    def generate_topic(self):
        # Prompt the llm to generate a blog topic
        response = completion(
            model = self.model,
            messages= [{
                "role": "user",
                "content": "Generate a creative blog topic for 2025."
            }]
        )
        topic = response["choices"][0]["message"]["content"].strip()
        print(f"Generate Topic: {topic}")
        return topic
    
    @listen(generate_topic)
    def generate_outline(self, topic):
        # New chain the output by using the topic in a follow-up prompt.
        response = completion(
            model = self.model,
            messages = [{
                "role": "user",
                "content": f"Based on the topic '{topic}', create a detailed outline for a blog post"
            }]
        )
        outline = response["choices"][0]["message"]["content"].strip()
        print("Generated Outline:")
        print(outline)
        self.state['outline'] = outline
    
    @listen(generate_outline)    
    def save_outline(self):
        with open("outline.md", "w")as file:
            file.write(self.state['outline'])
            return self.state['outline']
    
def kickoff():
    obj = TopicOutlineFlow()
    obj.kickoff()
    

def plot():
    obj = TopicOutlineFlow()
    obj.plot()