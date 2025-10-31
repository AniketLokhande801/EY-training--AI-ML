import streamlit as st
from backend import generate_itinerary, fetch_flights, fetch_hotels, fetch_youtube_vlogs

# Streamlit UI setup
st.title('AI Travel Agent')

# User Inputs
current_city = st.text_input('Current City')
vacation_city = st.text_input('Vacation City')
start_date = st.date_input('Start Date')
end_date = st.date_input('End Date')
trip_type = st.selectbox('Trip Type', ['Solo', 'Couple', 'Family', 'Friends'])
number_of_days = (end_date - start_date).days

# Call backend functions when the button is clicked
if st.button('Generate Travel Plan'):
    if current_city and vacation_city:
        # Step 1: Generate Itinerary
        itinerary = generate_itinerary(vacation_city, trip_type, number_of_days)
        st.subheader('Itinerary:')
        st.write(itinerary)

        # Step 2: Fetch Flights
        flights = fetch_flights(current_city, vacation_city, start_date)
        st.subheader('Flights:')
        for flight in flights:
            st.write(
                f"Airline: {flight['airline']}, Price: {flight['price']}, Departure Time: {flight['departure_time']}")

        # Step 3: Fetch Hotels
        hotels = fetch_hotels(vacation_city, start_date, end_date)
        st.subheader('Hotels:')
        for hotel in hotels:
            st.write(
                f"Hotel: {hotel['hotel_name']}, Price: {hotel['price']}, Rating: {hotel['rating']}, Address: {hotel['address']}")

        # Step 4: Fetch YouTube Vlogs
        vlogs = fetch_youtube_vlogs(vacation_city, trip_type)
        st.subheader('YouTube Travel Vlogs:')
        for vlog in vlogs:
            st.write(f"Title: {vlog['title']}, Channel: {vlog['channel']}, Link: [Watch here]({vlog['url']})")
    else:
        st.warning('Please enter both current and vacation city.')
