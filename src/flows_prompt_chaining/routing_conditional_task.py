from crewai.flow.flow import Flow, start, listen, router
from litellm import completion
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

class RoutedFlow(Flow):
    model = "gemini/gemini-1.5-flash"


    @start()
    def generate_topic(self):
        response = completion(
            model = self.model,
            messages = [{
                "role": "user",
                "content": "Generate a blog topic for 2025"
            }]
        )
        topic = response["choices"][0]["message"]["content"].strip()
        # For demonstration, add a fake flag to the state
        self.state["is_tech"] = "tech" in topic.lower()
        print(f"Topic {topic}")
        return topic
    
    @router(generate_topic)
    def route_topic(self):
        # Route based on the is_tech flag
        if self.state.get("is_tech"):
            return "tech_route"
        else:
            return "lifestyle_route"

    @listen("tech_route")
    def generate_tech_outline(self, topic):
        response = completion(
            model = self.model,
            messages = [{
                "role": "user",
                "content": "Create a detailed tech blog outline for : {topic}"
            }]
        )
        outline = response["choices"][0]["message"]["content"].strip()
        print("Tech Outline:")
        print(outline)
        return outline

    @listen("lifestyle_route")
    def generate_lifestyle_outlinee(self, topic):
        response = completion(
            model = self.model,
            messages= [{
                "role": "user",
                "content": "Create a detailed lifestyle blog outline for: {topic}"
            }]
        )
        outline = response["choices"][0]["message"]["content"].strip()
        print("Lifestyle Outline:")
        print(outline)
        return outline

def go():
    kick = RoutedFlow()
    kick.kickoff()
