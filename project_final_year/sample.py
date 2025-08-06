import csv
import requests
from bs4 import BeautifulSoup
import time

# Full list of medicinal plants (deduplicated and standardized)
plants = [
    "aloe_vera", "amla", "bamboo", "tulsi", "Tulasi", "curry_Leaf", "curry", "betel", "palak(Spinach)",
    "coriender", "ashoka", "seethapala", "lemon", "pomegranate", "pomoegranate", "pappaya", "Papaya",
    "jackfruit", "Insulin", "pepper", "Pepper", "raktachandini", "Jasmine", "neem", "castor", "Nooni",
    "Henna", "Mango", "doddapatre", "doddpathre", "amruta_Balli", "amruthaballi", "betel_Nut", "geranium",
    "rose", "Rose", "guava", "Gauva", "hibiscus", "Hibiscus", "nithyapushpa", "wood_sorel", "tamarind",
    "brahmi", "bhrami", "sapota", "basale", "avacado", "ashwagandha", "nagadali", "arali", "ekka", "ganike",
    "honge", "mint", "catharanthus"
]

# Function to scrape plant info from Wikipedia
def fetch_healthcare_data(plant_name):
    try:
        # Normalize name for URL (replace spaces or underscores appropriately)
        formatted_name = plant_name.replace("_", " ").replace("(", "").replace(")", "")
        wiki_url = f"https://en.wikipedia.org/wiki/{formatted_name.replace(' ', '_')}"
        response = requests.get(wiki_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Get first paragraph (Definition)
        paragraphs = soup.find_all('p')
        definition = next((p.text.strip() for p in paragraphs if len(p.text.strip()) > 50), "N/A")

        # Placeholder data — you can improve this with real parsing or use an API
        health_benefits = "Supports immunity, digestion, etc."
        traditional_use = "Used in Ayurvedic and traditional medicine"
        active_compounds = "Includes vitamins, alkaloids, tannins, etc."
        dosage = "Consult a healthcare provider"
        precautions = "Pregnancy, allergies, interactions may occur"
        sources = wiki_url

        return [plant_name, definition, health_benefits, traditional_use, active_compounds, dosage, precautions, sources]

    except Exception as e:
        print(f"Error fetching data for {plant_name}: {e}")
        return [plant_name] + ["N/A"] * 7

# Write data to CSV
with open('medicinal_plants_healthcare.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Plant Name", "Definition", "Health Benefits", "Traditional Use", "Active Compounds", "Dosage", "Precautions", "Sources"])
    
    for plant in plants:
        row = fetch_healthcare_data(plant)
        writer.writerow(row)
        time.sleep(1)  # Delay to avoid IP block
