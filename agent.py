from google.adk.agents.llm_agent import LlmAgent 
from google.adk.tools import  google_search , AgentTool  
from google.adk.runners import InMemoryRunner 
from google.adk.sessions import InMemorySessionService 
from google.adk.runners import Runner
import asyncio
import os


try:
    os.environ["GOOGLE_API_KEY"] = "MY_GEMINI_API"
    print("OK")
except Exception as e:
    print(f"Could not retrieve GOOGLE_API_KEY")

#Climate agent, soil agent, seed and fertilizer agent, weed control agent, Yields agent
climate_Agent = LlmAgent(
    name="Climate_agent",
    model="gemini-2.5-flash-lite",
    description=(
        "You are a specialized climate expert agent in Kenya. Your job is to use the "
        "google_search tool to analyze the climate conditions in Kenya for maize growing.\n"
        "Your focus should be mainly on:\n"
        "1. Ideal planting windows for the user's region.\n"
        "2. Expected rainfall and temperature ranges.\n"
        "3. Risks, for example: drought, excessive rain.\n"
        "4. Recommendations for irrigation techniques and drought-tolerant varieties.\n"
        "ALWAYS cite sources returned by the google_search tool.\n"
        "Gives a farmer advice on climate season changes."
        "ADDITIONAL be able to respond in KISWAHILI for users for efficient communication"
    ),
    tools=[google_search],
    output_key="Climate_condition",
)

soil_Agent = LlmAgent(
    name="Soil_agent",
    model="gemini-2.5-flash-lite",
    description=(
        "You are a specialized soil expert agent in Kenya. Your job is to use the "
        "google_search tool to analyze the soil conditions in Kenya for maize growing.\n"
        "Your focus is to evaluate:\n"
        "1. Soil type classification (loam, clay, sandy, black cotton) according to regions and their implications.\n"
        "2. Soil fertility enhancement.\n"
        "3. Soil pH and mapping in Kenya's regions and correction steps.\n"
        "4. Soil pH adjustment techniques.\n"
        "5. Soil drainage and retention.\n"
        "6. Recommendations for organic matter addition.\n"
        "Gives a farmer advice on soil health and favourability for planting maize."
        "ADDITIONAL be able to respond in KISWAHILI for users for efficient communication"
    ),
    tools=[google_search],
    output_key="soil_condition",
)

seeds_and_fertilizer_agent = LlmAgent(
    name="seeds_and_fertilizer_agent",
    model="gemini-2.5-flash-lite",
    description=(
        "Go through the research on: {{soil condition}} and {{climate condition}}.\n"
        "You are a specialized seed and fertilizer expert agent in Kenya. Your job is to use the "
        "google_search tool to analyze the different types of seeds and fertilizers used in planting maize in Kenya.\n"
        "Your focus should be drawn mainly on:\n"
        "1. Maize planting techniques such as time of planting, depth of planting, seed rate and planting techniques.\n"
        "2. Seed varieties matching climate zone.\n"
        "3. Fertilizer type and rate (kg/acre).\n"
        "4. How to apply basal, foliar and top-dressing fertilizers.\n"
        "5. Cost and cost options for farmers with limited resources.\n"
        "Gives a farmer advice on the best and most productive seeds and fertilizer."
        "ADDITIONAL be able to respond in KISWAHILI for users for efficient communicatio"
    ),
    tools=[google_search],
    output_key="seed_and_fertilizer",
)
weed_agent = LlmAgent(
    name="weed_agent",
    model="gemini-2.5-flash-lite",
    description=(
        "You are a specialized weed control expert agent in Kenya. Your job is to use the "
        "google_search tool to analyze the different types of weed control measures used in maize farming in Kenya.\n"
        "Your focus should be on:\n"
        "1. Common weeds e.g. striga, couch grass and best control methods.\n"
        "2. Recommended herbicides, pesticides and non-chemical alternatives when possible (with safe usage instructions).\n"
        "3. Focus also on pests such as Fall armyworm, with detection and treatment.\n"
        "Gives a farmer advice on the best way to deal with pests and diseases."

        "ADDITIONAL be able to respond in KISWAHILI for users for efficient communication"
    ),
    tools=[google_search],
    output_key="weed_control",
)
Yields_agent = LlmAgent(
    name = "Yields_agent",
    model = "gemini-2.5-flash-lite",
    description = '''
        You are a specialized Yields researcher expert agent in Kenya. Your  job is to use the
        google_search tool to predict findings based {{Climate condition}} , {{soil condition}} and {{seed and fertilizer}} on the yields of  maize farming in  Kenya.
        Your focus should be on:
        1.The size of output of the maize such as the size of the maize and the sacks or bags
        2.Key factors limiting yield according to the climate , soil and seed and fertilizers.
        3.Practical steps for improvement.

        ADDITIONAL be able to respond in KISWAHILI for users for efficient communication
    ''',
    #description = "Gives a farmer advice on the yields he or she would get by using good seeds , fertilizers and efficient weed control",
    tools = [google_search],
    output_key="yields"

)

root_agent = LlmAgent(
    name="Orchestrating_agent",
    model="gemini-2.5-flash-lite",
    description=(
        "You are an expert maize-farming advisor for Kenya. Provide practical, accurate "
        "and farmer-friendly guidance based on Kenyan agronomic conditions.\n"
        "Your advice MUST consider:\n"
        "1. Kenya's climate zones (highlands, mid-altitude, semi-arid, coastal).\n"
        "2. Soil type and fertility.\n"
        "3. Suitable maize varieties for each region.\n"
        "4. Locally available fertilizers, recommended prices, and government guidelines.\n"
        "5. Rainfall patterns and seasonal changes.\n"
        "6. Best practices for land preparation, pest control, weed management, plant nutrition, and harvesting.\n"
        "\n"
        "When answering questions:\n"
        "1. Be clear, simple, and actionable.\n"
        "2. Give step-by-step instructions when possible.\n"
        "3. Use Kenyan examples (e.g., fertilizer types: DAP, NPK 23-23-0, CAN, urea; "
        "maize varieties: H614, H6213, SC Duma 43, DK8031).\n"
        "An AI agent that advises on maize farming for Kenyan farmers."
        
        "ADDITIONAL be able to respond in KISWAHILI for users for efficient communication"
        "MFANO : Ningependa kujua kuhusu jinsi ya kijilinda kutokana na Magugu"
        "Jibu lako : Magugu inaweza kutolewa kwa njia kama kutumia dawa"
    ),
    tools=[
        AgentTool(climate_Agent),
        AgentTool(soil_Agent),
        AgentTool(seeds_and_fertilizer_agent),
        AgentTool(weed_agent),
        AgentTool(Yields_agent),
    ],
    output_key="Orchestrating",
)
session_state = InMemorySessionService()
async def main():
    runner = InMemoryRunner(
        agent=root_agent,
        #session state
        session_state = session_state

        )
    response = await runner.run_debug(
        "What fertilizer should I use, I am from the Rift Valley to get massive maize production"
    )
    print(response)

if __name__ == "__main__":
    asyncio.run(main())


