from PIL import Image
from io import BytesIO
import base64
import streamlit as st
import time
from dotenv import load_dotenv
from modules.actions import get_car_data
load_dotenv()


def render_page():
    # Initialize session state to track the current step
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 0

    # Define the number of questions in the form
    TOTAL_STEPS = 6

    # Dictionary to store user preferences
    if 'user_data' not in st.session_state:
        st.session_state.user_data = {}

    # Function to handle the previous button
    def prev_step():
        if st.session_state.current_step > 0:
            st.session_state.current_step -= 1

    # Function to handle the next button
    def next_step():
        if st.session_state.current_step < TOTAL_STEPS:
            st.session_state.current_step += 1

    def final_step():
        st.session_state.current_step = -1

    # Display questions one by one based on the current step
    if st.session_state.current_step == 0:
        st.session_state['use_mock_data'] = False
        
        # Vraag 1: Uw budget
        st.subheader("1. Wat is uw budget?")
        budget_type = st.selectbox("Wilt u betalen per maand of in één keer (cash)?", ["Maandelijks", "Cash"])

        if budget_type == "Maandelijks":
            min_budget_monthly = st.number_input("Maandelijks minimum budget (€)", min_value=0, step=100)
            max_budget_monthly = st.number_input("Maandelijks maximum budget (€)", min_value=min_budget_monthly, step=100)
            st.session_state.user_data['budget'] = {"type": "Maandelijks", "min": min_budget_monthly, "max": max_budget_monthly}
        else:
            min_budget_cash = st.number_input("Cash minimum budget (€)", min_value=0, step=1000)
            max_budget_cash = st.number_input("Cash maximum budget (€)", min_value=min_budget_cash, step=1000)
            st.session_state.user_data['budget'] = {"type": "Cash", "min": min_budget_cash, "max": max_budget_cash}

    elif st.session_state.current_step == 1:
        # Vraag 2: Brandstofvoorkeur
        st.subheader("2. Wat is uw voorkeur voor brandstof?")
        fuel_type = st.selectbox("Kies uw brandstoftype", ["Benzine", "Diesel", "Hybride", "Elektrisch"])
        st.session_state.user_data['fuel_type'] = fuel_type

    elif st.session_state.current_step == 2:
        st.subheader(f"2.1 Aanvullende vragen over {st.session_state.user_data.get('fuel_type', '?')}")
        # Vraag 3: Vervolgvragen op basis van brandstoftype
        fuel_type = st.session_state.user_data.get('fuel_type', 'Benzine')
        if fuel_type == "Hybride":
            hybride_type = st.radio("Welke type hybride?", ["Mild-hybride", "Plug-in hybride"])
            st.session_state.user_data['hybride_type'] = hybride_type
        elif fuel_type == "Elektrisch":
            battery_range = st.slider("Gewenste actieradius (km)", min_value=100, max_value=600, step=50)
            st.session_state.user_data['battery_range'] = battery_range
        elif fuel_type == "Benzine":
            efficiency = st.slider("Wat is uw voorkeur voor brandstofzuinigheid? (L/100km)", min_value=5.0, max_value=15.0, step=0.5)
            st.session_state.user_data['efficiency'] = efficiency

    elif st.session_state.current_step == 3:
        st.subheader(f"2.2 Aanvullende vragen over {st.session_state.user_data.get('fuel_type', '?')}")
        # Vraag 4: Meer doorvragen over bereik of zuinigheid
        fuel_type = st.session_state.user_data.get('fuel_type', 'Benzine')
        if fuel_type == "Elektrisch":
            fast_charging = st.radio("Heeft u voorkeur voor snelle laadmogelijkheden?", ["Ja", "Nee"])
            st.session_state.user_data['fast_charging'] = fast_charging
        elif fuel_type == "Benzine":
            fuel_tank_size = st.slider("Gewenste tankinhoud (L)", min_value=30, max_value=100, step=5)
            st.session_state.user_data['fuel_tank_size'] = fuel_tank_size
        elif fuel_type == "Hybride":
            fuel_tank_size = st.slider("Gewenste tankinhoud (L)", min_value=30, max_value=100, step=5)
            st.session_state.user_data['fuel_tank_size'] = fuel_tank_size

    elif st.session_state.current_step == 4:
        # Vraag 5: Inhoud van de kofferbak
        st.subheader("5. Hoeveel koffers moeten er in de kofferbak passen?")
        suitcase_count = st.selectbox("Aantal koffers", ["1 koffer (120 liter)", "2 koffers (240 liter)", "3 koffers (360 liter)", "4 koffers (480 liter)", "5+ koffers (600 liter)"])
        st.session_state.user_data['suitcase_count'] = suitcase_count

    elif st.session_state.current_step == 5:
        # Vraag 6: Omstandigheid
        st.subheader("6. Welke omstandigheid beschrijft u het best?")
        circumstance = st.selectbox("Kies uw situatie", [
            "Woningstarter op zoek naar een eerste auto",
            "Ouder van 1-2 kinderen",
            "Ouder van 3+ kinderen",
            "Ouder op zoek naar een 2e auto",
            "Zakelijke rijder",
            "Auto voor lange afstanden",
            "Milieubewuste rijder",
            "Luxe en comfort belangrijk"
        ])
        st.session_state.user_data['circumstance'] = circumstance

    # Buttons for navigation
    col1, col2 = st.columns([1, 1])

    if st.session_state.current_step > 0:
        col1.button("Vorige", on_click=prev_step)

    if st.session_state.current_step < TOTAL_STEPS - 1 and not st.session_state.current_step == -1:
        col2.button("Volgende", on_click=next_step)
    else:
        if not st.session_state.current_step == -1:
            col2.button("Zoek mijn auto", on_click=final_step)

    if st.session_state.current_step == -1:
        render_result_page()


# Function to render the result page
def render_result_page():
    st.subheader("🎉 Gefeliciteerd! We hebben de perfecte auto voor u gevonden!")
    
    # OpenAI functie aanroepen om een auto te vinden
    car_data = get_car_data(st.session_state.user_data)
    
    # Show Car image base64 encoded
    aux_image = Image.open(BytesIO(base64.b64decode(car_data['image'])))
    st.image(aux_image, caption=car_data['name'], use_column_width=True)
    
    # Prijs in grote, opvallende stijl
    st.metric(label="Prijs", value=f"💶 {car_data['price']}")
    
    # Aanbieders weergeven in mooi opgemaakte kaarten
    st.write("Aanbieders:")
    for dealer in car_data['dealers']:
        st.markdown(
            f"""
            <div style='border: 1px solid #ddd; padding: 10px; border-radius: 10px; margin-bottom: 10px;'>
                <h4>{dealer['name']}</h4>
                <a href='{dealer['link']}' style='text-decoration: none;'>
                    <button style='background-color: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 5px;'>
                        Bekijk deze auto
                    </button>
                </a>
            </div>
            """, unsafe_allow_html=True)
    
    # E-mail invoerveld en knop om te verzenden
    email = st.text_input("Sla dit resultaat op. Voer uw e-mail in:")
    if st.button("Verstuur naar mijn e-mail"):
        with st.spinner("Bezig met verzenden..."):
            time.sleep(2)  # Simuleert het verzenden
            st.success("Succes! Uw mail is verzonden.")


if __name__ == "__main__":
    render_page()