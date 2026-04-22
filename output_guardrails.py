from agents import Agent, output_guardrail, Runner, RunContextWrapper, GuardrailFunctionOutput
from models import RestaurantOutputGuardRailOuput, UserAccountContext

restaurant_output_guardrail_agent = Agent(
    name="Restaurant Support Guardrail",
    instructions="""
    You must respond to the customer in a professional, polite, and respectful manner at all times. When replying, you must never disclose, mention, or include any private or confidential information related to the restaurant, its internal operations, staff, or any other customers. Only provide information that is directly relevant to the customer’s request and appropriate for customer support.
    
    Return true for any field that contains inappropriate content for a restaurant support response.
    """,
    output_type=RestaurantOutputGuardRailOuput,
)

@output_guardrail
async def restaurant_output_guardrail(
    wrapper: RunContextWrapper[UserAccountContext],
    agent: Agent,
    output: str,
):
    result = await Runner.run(
        restaurant_output_guardrail_agent,
        output,
        context=wrapper.context,
    )

    validation = result.final_output

    triggered = validation.contains_off_topic or validation.contains_sensitive_info

    return GuardrailFunctionOutput(
        output_info=validation,
        tripwire_triggered=triggered,
    )
