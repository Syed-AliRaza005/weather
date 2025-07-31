import streamlit as st
import requests
import json
import os


def get_weather(city_name):
   
    API_KEY = os.getenv("API_KEY") 
    BASE_URL = os.getenv("BASE_URL")
    
    params = {
        'q': city_name,
        'appid': API_KEY,
        'units': 'metric'  
    }
    
    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # Extract weather information
            weather_info = {
                'city': data['name'],
                'country': data['sys']['country'],
                'temperature': data['main']['temp'],
                'feels_like': data['main']['feels_like'],
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'description': data['weather'][0]['description'],
                'wind_speed': data['wind']['speed'],
               
            }
            
            return weather_info
            
        elif response.status_code == 404:
            return st.error({'error': f'City "{city_name}" not found. Please check the spelling.'})
        elif response.status_code == 401:
            return st.error({'error': 'Invalid API key. Please check your OpenWeatherMap API key.'})
        else:
            return st.error({'error': f'API Error: {response.status_code} - {response.text}'})
            
    except requests.exceptions.RequestException as e:
        return ({'error': f'Network error: {str(e)}'})
    except json.JSONDecodeError:
        return ({'error': 'Invalid response from weather API'})
    except Exception as e:
        return ({'error': f'Unexpected error: {str(e)}'})

def display_weather(weather_data):
    
    if 'error' in weather_data:
        st.error(f"❌ Error: {weather_data['error']}")
        return

    st.write(
    ("=" * 50),"\n",
    (f"# **🌍 Weather for {weather_data['city']}, {weather_data['country']}**"),"\n",
    
    ("=" * 50),"\n")
    temp= st.write(f"### 🌡️  Temperature: {weather_data['temperature']}°C"),"\n",
    st.write(
    (f"### 🤔 Feels like: {weather_data['feels_like']}°C"),"\n",
    (f"### 💧 Humidity: {weather_data['humidity']}%"),"\n",
    (f"### 🌪️  Wind Speed: {weather_data['wind_speed']} m/s"),"\n",
    (f"### 🌤️  Weather: {weather_data['description'].title()}"),"\n",    
    ("=" * 50))

    temp = weather_data['temperature']
    if temp <= 0:
        page_bg_img = """
        <style> 
         [data-testid="stAppViewContainer"] {
        background-color : rgba(0, 102, 204, 0.85);
        }"""
        st.markdown(page_bg_img, unsafe_allow_html=True)
    
    elif 0< temp <=15 :
        page_bg_img = """
        <style> 
         [data-testid="stAppViewContainer"] {
        background-color : rgba(0, 204, 255, 0.85);
        }"""
        st.markdown(page_bg_img, unsafe_allow_html=True) 
    
    elif 15< temp <=25 :
        page_bg_img = """
        <style> 
         [data-testid="stAppViewContainer"] {
        background-color : rgba(102, 204, 0, 0.85);
        }"""
        st.markdown(page_bg_img, unsafe_allow_html=True)   
    
    elif 25< temp <=35 :
        page_bg_img = """
        <style> 
         [data-testid="stAppViewContainer"] {
        background-color : rgba(255, 153, 51, 0.85);
        }"""
        st.markdown(page_bg_img, unsafe_allow_html=True)
    else :
        page_bg_img = """
        <style> 
         [data-testid="stAppViewContainer"] {
        background-color : rgba(255, 71, 41, 0.70);
        }"""
        st.markdown(page_bg_img, unsafe_allow_html=True)

    
def main():

    st.write("# **🌤️  Weather App - OpenWeatherMap API**")
    st.write("-" * 40)
    
    # You can change the city here or make it interactive
    city = st.text_input("Enter city name .karachi city as default: ").strip()
    
    if not city:
        city = "Karachi"
    
    print(f"\n🔍 Fetching weather data for {city}...")
    
    
    weather_data = get_weather(city)
    display_weather(weather_data)

if __name__ == "__main__":
    main()
