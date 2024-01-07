import streamlit as st
import random

# Definieer een set om de getrokken nummers bij te houden
if 'drawn_numbers' not in st.session_state:
    st.session_state.drawn_numbers = set()

# Definieer een functie om het laatste getrokken nummer weer te geven
def display_last_drawn(number):
    if number is not None:
        # Gebruik HTML en inline CSS om de stijl van het getoonde nummer aan te passen
        st.markdown(
            f'<div style="font-size: 2em; line-height: 2em; width: 2em; height: 2em; '
            f'background-color: #28a745; color: white; border-radius: 50%; display: flex; '
            f'justify-content: center; align-items: center; margin: 10px auto;">'
            f'{number}</div>',
            unsafe_allow_html=True
        )
    else:
        st.write("Nog geen nummers getrokken.")

def display_numbers(drawn_numbers):
    # Breedte van elk nummer instellen
    num_width = "40px"  # Breedte van elk nummer
    num_margin = "5px"  # Marge rond elk nummer
    total_margin = "10px"  # Totale marge (links + rechts)
    container_width = f"calc((16 * ({num_width} + (2 * {num_margin}))))"

    # Begin met het maken van de HTML voor de nummers
    html_str = f'<div style="display: flex; flex-wrap: wrap; justify-content: start; width: {container_width}; padding: 10px;">'

    for number in range(1, 76):
        if number in drawn_numbers:
            # Nummer is getrokken, gebruik groene achtergrond
            bg_color = "#28a745"
            color = "white"
        else:
            # Nummer is niet getrokken, gebruik witte achtergrond
            bg_color = "white"
            color = "black"

        # Voeg HTML voor elk nummer toe
        html_str += f'<div style="background-color: {bg_color}; color: {color}; ' \
                    f'border: 2px solid black; border-radius: 50%; width: {num_width}; height: {num_width}; ' \
                    f'display: flex; justify-content: center; align-items: center; ' \
                    f'margin: {num_margin}; font-size: 16px;">' \
                    f'{number}</div>'

    html_str += '</div>'

    # Toon de HTML in Streamlit
    st.markdown(html_str, unsafe_allow_html=True)


def draw_specific_number(number):
    try:
        number = int(number)
        if 1 <= number <= 75:
            if number not in st.session_state.drawn_numbers:
                st.session_state.drawn_numbers.add(number)
                st.session_state.last_drawn = number
            else:
                st.error(f'Nummer {number} is al getrokken.')
        else:
            st.error('Voer een geldig nummer in (1-75).')
    except ValueError:
        st.error('Voer een geldig nummer in (1-75).')

def draw_random_number():
    available_numbers = set(range(1, 76)) - st.session_state.drawn_numbers
    if available_numbers:
        number = random.choice(list(available_numbers))
        st.session_state.drawn_numbers.add(number)
        st.session_state.last_drawn = number
    else:
        st.error('Alle nummers zijn al getrokken.')

def reset_game():
    st.session_state.drawn_numbers = set()
    st.session_state.last_drawn = None

# UI
st.title('Mechels Bos Bingo App')

with st.form(key='number_input'):
    number_input = st.text_input('Voer een nummer in (1-75):', '')
    submit_number = st.form_submit_button(label='Nummer toevoegen')
    if submit_number:
        draw_specific_number(number_input)

if st.button('Trek Willekeurig Nummer'):
    draw_random_number()

if st.button('Nieuw Spel'):
    reset_game()

# Laatst getrokken nummer en de lijst van getrokken nummers
st.subheader("Laatst getrokken nummer:")
display_last_drawn(st.session_state.last_drawn if 'last_drawn' in st.session_state else None)

st.subheader('Getrokken Nummers:')
display_numbers(st.session_state.drawn_numbers if 'drawn_numbers' in st.session_state else set())

# Run dit script met: streamlit run bingo_app.py
