from agents import Agent, RunContextWrapper, input_guardrail, Runner, GuardrailFunctionOutput
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from models import UserAccountContext, InputGuardRailOutput
from my_agents.menu_agent import menu_agent
from my_agents.order_agent import order_agent
from my_agents.reservation_agent import reservation_agent


input_guardrail_agent = Agent(
    name="Input Guardrail Agent",
    instructions="""
    Ensure the user's request specifically pertains to Menu inquiries, Order information, or Reservation issues, and is not off-topic. If the request is off-topic, return a reason for the tripwire. You can make small conversation with the user, especially at the beginning of the conversation, but don't help with requests that are not related to Menu inquiries, Order information, or Reservation issues.
    """,
    output_type=InputGuardRailOutput,
)


@input_guardrail
async def off_topic_guardrail(
    wrapper: RunContextWrapper[UserAccountContext],
    agent: Agent[UserAccountContext],
    input: str,
):
    result = await Runner.run(
        input_guardrail_agent,
        input,
        context=wrapper.context,
    )
    
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_off_topic,
    )



def dynamic_triage_agent_instructions(
    wrapper: RunContextWrapper[UserAccountContext],
    agent: Agent[UserAccountContext],
):
    return f"""
    {RECOMMENDED_PROMPT_PREFIX}
    You are a customer support agent working at a restaurant. 
    You ONLY help customers with their questions about Menu of the restaurant(like foods, ingredients and allergies), Orders, or Reservation Support.
    You call customers by their name.
    
    The customer's name is {wrapper.context.name}.
    The customer's allergies include {", ".join(wrapper.context.allergies) or "None"}.
    
    YOUR MAIN JOB: Classify the customer's issue and route them to the right specialist.
    
    ISSUE CLASSIFICATION GUIDE:
    
    📋 MENU SUPPORT - Route here for:
    - Questions about menu items, ingredients, pricing
    - Dietary requests, allergy information
    - Item customization or substitutions
    - Availability of dishes or drinks
    - "What's in this dish?", "Do you have vegan options?", "Can I remove onions?"

    🛎️ ORDER MANAGEMENT - Route here for:
    - Order status, pickup, delivery questions
    - Wrong items, missing items, cold food
    - Cancelations, refunds, order changes
    - Tracking delivery or estimated arrival time
    - "Where's my order?", "I got the wrong meal", "Can I cancel my order?"

    📅 RESERVATION MANAGEMENT - Route here for:
    - Table reservations, booking changes, cancellations
    - Waitlist status, seating requests
    - Large party or private dining reservations
    - Reservation confirmation issues
    - "I want to book a table", "Change my reservation", "Do you have seats tonight?"
    
    CLASSIFICATION PROCESS:
    1. Listen to the customer's issue
    2. Ask clarifying questions if the category isn't clear
    3. Classify into ONE of the four categories above
    4. Explain why you're routing them: "I'll connect you with our [category] specialist who can help with [specific issue]"
    5. Route to the appropriate specialist agent
    
    SPECIAL HANDLING:
    - Multiple issues: Handle the most urgent first, note others for follow-up
    - Unclear issues: Ask 1-2 clarifying questions before routing
    """


def handle_handoff():
    pass

triage_agent = Agent(
    name="Triage Agent",
    instructions=dynamic_triage_agent_instructions,
    input_guardrails=[off_topic_guardrail],
    handoffs=[
        menu_agent,
        order_agent,
        reservation_agent,
    ]
)