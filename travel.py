import streamlit as st
from google import genai
import os
from dotenv import load_dotenv

# ---------------------------
# Load API Key
# ---------------------------
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

client = None

# Create Gemini client if API exists
try:
    if API_KEY:
        client = genai.Client(api_key=API_KEY)
except:
    client = None


# ---------------------------
# Smart Fallback Generator
# ---------------------------
def fallback_itinerary(destination, days, nights):

    itinerary = f"# Travel Itinerary for {destination}\n"
    itinerary += f"{days} Days / {nights} Nights\n\n"

    activities = [
        "Explore famous tourist attractions",
        "Visit historical landmarks",
        "Enjoy local street food",
        "Go shopping in local markets",
        "Experience cultural activities",
        "Visit parks and scenic spots",
        "Adventure activities",
        "Relax at popular cafes",
    ]

    food = [
        "Try local traditional dishes",
        "Taste famous street food",
        "Enjoy dinner at a popular restaurant",
        "Visit a local cafe",
    ]

    for i in range(1, days + 1):

        itinerary += f"## Day {i}: Explore {destination}\n\n"

        itinerary += f"Morning:\n{activities[(i*2) % len(activities)]}\n\n"

        itinerary += f"Afternoon:\n{activities[(i*3) % len(activities)]}\n\n"

        itinerary += f"Evening:\n{activities[(i*4) % len(activities)]}\n\n"

        itinerary += f"Night:\n{food[i % len(food)]}\n\n"

        itinerary += "---\n"

    itinerary += "\nEstimated Budget: ₹15,000 – ₹25,000 per person\n"
    itinerary += "Travel Tips:\n"
    itinerary += "- Carry ID proof\n"
    itinerary += "- Check weather before travel\n"
    itinerary += "- Book tickets early\n"

    return itinerary


# ---------------------------
# Generate Itinerary
# ---------------------------
def generate_itinerary(destination, days, nights):

    prompt = f"""
    Create a detailed {days}-day travel itinerary for {destination}.

    Follow this format strictly.

    Day 1: Title
    Morning:
    Afternoon:
    Evening:
    Night:

    Day 2: Title
    Morning:
    Afternoon:
    Evening:
    Night:

    Continue until Day {days}.

    Include:
    - Tourist attractions
    - Activities
    - Local food suggestions
    - Travel tips
    - Estimated budget

    Each day must have different activities.
    """

    try:

        if client:

            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )

            return response.text

        else:
            return fallback_itinerary(destination, days, nights)

    except Exception:
        return fallback_itinerary(destination, days, nights)


# ---------------------------
# MAIN FUNCTION
# ---------------------------
def main():

    st.title("Travel Itinerary Generator ✈️")

    st.write("Generate a personalized travel itinerary using AI.")

    destination = st.text_input("Enter your destination:")

    days = st.number_input(
        "Enter number of days:",
        min_value=1,
        step=1
    )

    nights = st.number_input(
        "Enter number of nights:",
        min_value=0,
        step=1
    )

    if st.button("Generate Itinerary", type="primary"):

        if destination.strip():

            with st.spinner("Generating itinerary..."):

                itinerary = generate_itinerary(
                    destination,
                    days,
                    nights
                )

            st.success("Itinerary Generated!")

            st.markdown(itinerary)

        else:
            st.error("Please enter a destination.")


# ---------------------------
# Entry Point
# ---------------------------
if __name__ == "__main__":
    main()