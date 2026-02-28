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

# Try creating Gemini client
try:
    if API_KEY:
        client = genai.Client(api_key=API_KEY)
except:
    client = None


# ---------------------------
# Backup Itinerary (IMPORTANT)
# ---------------------------
def fallback_itinerary(destination, days, nights):
    return f"""
Travel Itinerary (Sample Mode)

Destination: {destination}
Days: {days}
Nights: {nights}

Day 1:
- Arrival and hotel check-in
- Local sightseeing
- Try famous local food

Day 2:
- Visit major tourist attractions
- Shopping and cultural experience

Day 3:
- Adventure activities
- Explore markets
- Departure preparation

Estimated Budget:
₹15,000 – ₹25,000 per person

Travel Tips:
- Carry ID proof
- Check weather updates
- Book tickets early
"""


# ---------------------------
# Generate Itinerary
# ---------------------------
def generate_itinerary(destination, days, nights):

    prompt = f"""
    Create a detailed travel itinerary.

    Destination: {destination}
    Days: {days}
    Nights: {nights}
    """

    try:
        if client:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )

            return response.candidates[0].content.parts[0].text

        else:
            return fallback_itinerary(destination, days, nights)

    except Exception:
        # ✅ API fails → still works
        return fallback_itinerary(destination, days, nights)


# ---------------------------
# MAIN FUNCTION
# ---------------------------
def main():

    st.title("Travel Itinerary Generator ✈️")

    destination = st.text_input("Enter destination:")
    days = st.number_input("Number of days:", min_value=1)
    nights = st.number_input("Number of nights:", min_value=0)

    if st.button("Generate Itinerary", type="primary"):

        if destination.strip():

            with st.spinner("Generating itinerary..."):
                itinerary = generate_itinerary(
                    destination,
                    days,
                    nights
                )

            st.text_area(
                "Generated Itinerary",
                value=itinerary,
                height=350
            )

        else:
            st.error("Please enter destination.")


# ---------------------------
# ENTRY POINT
# ---------------------------
if __name__ == "__main__":
    main()