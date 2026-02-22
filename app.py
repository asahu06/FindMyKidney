# Importing Relevant Libraries
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random
import math
import bisect

st.set_page_config(
    page_title="FindMyKidney",
    page_icon="🫘",
    layout="wide"
)

if 'patients' not in st.session_state:
    st.session_state.patients = [
    {"id": 1, "name": "Peter Parker", "age": 45, "sex": "M", "blood_type": "O+", "CPRA": 12, "living_donor": False, "days_on_waitlist": 450, "location": "Cleveland Clinic, OH", "distance": 142, "diabetes": False, "psot": False},
    {"id": 2, "name": "Gwen Stacy", "age": 32, "sex": "F", "blood_type": "A-", "CPRA": 98, "living_donor": True, "days_on_waitlist": 1200, "location": "UPMC Presbyterian, PA", "distance": 185, "diabetes": False, "psot": True},
    {"id": 3, "name": "Tony Stark", "age": 67, "sex": "M", "blood_type": "B+", "CPRA": 5, "living_donor": False, "days_on_waitlist": 2100, "location": "Johns Hopkins, MD", "distance": 405, "diabetes": True, "psot": False},
    {"id": 4, "name": "Natasha Romanoff", "age": 51, "sex": "F", "blood_type": "O-", "CPRA": 45, "living_donor": False, "days_on_waitlist": 15, "location": "Cincinnati Children's, OH", "distance": 105, "diabetes": False, "psot": False},
    {"id": 5, "name": "Steve Rogers", "age": 28, "sex": "M", "blood_type": "AB+", "CPRA": 0, "living_donor": False, "days_on_waitlist": 365, "location": "IU Health Methodist, IN", "distance": 175, "diabetes": False, "psot": False},
    {"id": 6, "name": "Wanda Maximoff", "age": 58, "sex": "F", "blood_type": "A+", "CPRA": 25, "living_donor": False, "days_on_waitlist": 2900, "location": "University of Chicago, IL", "distance": 310, "diabetes": True, "psot": False},
    {"id": 7, "name": "Bruce Banner", "age": 42, "sex": "M", "blood_type": "O+", "CPRA": 75, "living_donor": False, "days_on_waitlist": 890, "location": "University of Michigan, MI", "distance": 190, "diabetes": False, "psot": True},
    {"id": 8, "name": "Carol Danvers", "age": 73, "sex": "F", "blood_type": "B-", "CPRA": 15, "living_donor": True, "days_on_waitlist": 50, "location": "Vanderbilt University, TN", "distance": 380, "diabetes": True, "psot": False},
    {"id": 9, "name": "Matt Murdock", "age": 39, "sex": "M", "blood_type": "O+", "CPRA": 100, "living_donor": False, "days_on_waitlist": 3200, "location": "University of Virginia, VA", "distance": 350, "diabetes": False, "psot": True},
    {"id": 10, "name": "Jessica Jones", "age": 61, "sex": "F", "blood_type": "A+", "CPRA": 2, "living_donor": False, "days_on_waitlist": 600, "location": "WVU Medicine, WV", "distance": 160, "diabetes": True, "psot": False},
    {"id": 11, "name": "Luke Cage", "age": 44, "sex": "M", "blood_type": "B+", "CPRA": 33, "living_donor": False, "days_on_waitlist": 1100, "location": "Duke University, NC", "distance": 450, "diabetes": False, "psot": False},
    {"id": 12, "name": "Kamala Khan", "age": 35, "sex": "F", "blood_type": "AB-", "CPRA": 88, "living_donor": False, "days_on_waitlist": 1500, "location": "Mount Sinai, NY", "distance": 530, "diabetes": False, "psot": True},
    {"id": 13, "name": "Reed Richards", "age": 55, "sex": "M", "blood_type": "O-", "CPRA": 10, "living_donor": True, "days_on_waitlist": 300, "location": "Cleveland Clinic, OH", "distance": 142, "diabetes": True, "psot": False},
    {"id": 14, "name": "Susan Storm", "age": 49, "sex": "F", "blood_type": "A-", "CPRA": 55, "living_donor": False, "days_on_waitlist": 750, "location": "University of Kentucky, KY", "distance": 190, "diabetes": False, "psot": False},
    {"id": 15, "name": "Johnny Storm", "age": 31, "sex": "M", "blood_type": "B+", "CPRA": 12, "living_donor": False, "days_on_waitlist": 1400, "location": "Barnes-Jewish Hospital, MO", "distance": 420, "diabetes": False, "psot": False},
    {"id": 16, "name": "Janet Van Dyne", "age": 64, "sex": "F", "blood_type": "O+", "CPRA": 0, "living_donor": False, "days_on_waitlist": 2500, "location": "Christ Hospital, OH", "distance": 110, "diabetes": True, "psot": False},
    {"id": 17, "name": "Hank Pym", "age": 27, "sex": "M", "blood_type": "A+", "CPRA": 99, "living_donor": False, "days_on_waitlist": 1800, "location": "Georgetown University, DC", "distance": 400, "diabetes": False, "psot": True},
    {"id": 18, "name": "Peggy Carter", "age": 52, "sex": "F", "blood_type": "B-", "CPRA": 40, "living_donor": False, "days_on_waitlist": 45, "location": "Corewell Health, MI", "distance": 260, "diabetes": False, "psot": False},
    {"id": 19, "name": "Scott Lang", "age": 38, "sex": "M", "blood_type": "AB+", "CPRA": 60, "living_donor": True, "days_on_waitlist": 950, "location": "Penn Medicine, PA", "distance": 435, "diabetes": False, "psot": False},
    {"id": 20, "name": "Hope Van Dyne", "age": 70, "sex": "F", "blood_type": "O+", "CPRA": 8, "living_donor": False, "days_on_waitlist": 1300, "location": "Riverside Methodist, OH", "distance": 5, "diabetes": True, "psot": False},
    {"id": 21, "name": "Stephen Strange", "age": 41, "sex": "M", "blood_type": "A-", "CPRA": 92, "living_donor": False, "days_on_waitlist": 2200, "location": "Norton Healthcare, KY", "distance": 210, "diabetes": False, "psot": True},
    {"id": 22, "name": "Jean Grey", "age": 59, "sex": "F", "blood_type": "O+", "CPRA": 20, "living_donor": False, "days_on_waitlist": 110, "location": "Henry Ford Health, MI", "distance": 205, "diabetes": True, "psot": False},
    {"id": 23, "name": "Scott Summers", "age": 33, "sex": "M", "blood_type": "B+", "CPRA": 4, "living_donor": False, "days_on_waitlist": 500, "location": "Allegheny General, PA", "distance": 180, "diabetes": False, "psot": False},
    {"id": 24, "name": "Ororo Munroe", "age": 46, "sex": "F", "blood_type": "AB-", "CPRA": 70, "living_donor": False, "days_on_waitlist": 1600, "location": "Mayo Clinic, MN", "distance": 615, "diabetes": False, "psot": True},
    {"id": 25, "name": "Logan Howlett", "age": 50, "sex": "M", "blood_type": "O-", "CPRA": 15, "living_donor": True, "days_on_waitlist": 250, "location": "St. Vincent, IN", "distance": 170, "diabetes": False, "psot": False},
    {"id": 26, "name": "Kitty Pryde", "age": 63, "sex": "F", "blood_type": "A+", "CPRA": 30, "living_donor": False, "days_on_waitlist": 3400, "location": "Northwestern Memorial, IL", "distance": 315, "diabetes": True, "psot": False},
    {"id": 27, "name": "Remy LeBeau", "age": 29, "sex": "M", "blood_type": "B-", "CPRA": 85, "living_donor": False, "days_on_waitlist": 120, "location": "UofL Health, KY", "distance": 205, "diabetes": False, "psot": False},
    {"id": 28, "name": "Anna Marie", "age": 37, "sex": "F", "blood_type": "O+", "CPRA": 50, "living_donor": False, "days_on_waitlist": 2000, "location": "Einstein Medical, PA", "distance": 430, "diabetes": False, "psot": True},
    {"id": 29, "name": "Charles Xavier", "age": 68, "sex": "M", "blood_type": "AB+", "CPRA": 12, "living_donor": False, "days_on_waitlist": 720, "location": "Summa Health, OH", "distance": 125, "diabetes": True, "psot": False},
    {"id": 30, "name": "Emma Frost", "age": 43, "sex": "F", "blood_type": "A+", "CPRA": 0, "living_donor": False, "days_on_waitlist": 10, "location": "Temple University, PA", "distance": 440, "diabetes": False, "psot": False},
    {"id": 31, "name": "Warren Worthington", "age": 56, "sex": "M", "blood_type": "B+", "CPRA": 66, "living_donor": False, "days_on_waitlist": 2750, "location": "MedStar Washington, DC", "distance": 395, "diabetes": True, "psot": False},
    {"id": 32, "name": "Betsy Braddock", "age": 47, "sex": "F", "blood_type": "O-", "CPRA": 94, "living_donor": False, "days_on_waitlist": 1450, "location": "Akron General, OH", "distance": 130, "diabetes": False, "psot": True},
    {"id": 33, "name": "Kurt Wagner", "age": 30, "sex": "M", "blood_type": "A-", "CPRA": 18, "living_donor": True, "days_on_waitlist": 330, "location": "Dayton Children's, OH", "distance": 75, "diabetes": False, "psot": False},
    {"id": 34, "name": "Jubilation Lee", "age": 53, "sex": "F", "blood_type": "O+", "CPRA": 42, "living_donor": False, "days_on_waitlist": 1900, "location": "Froedtert Hospital, WI", "distance": 425, "diabetes": False, "psot": False},
    {"id": 35, "name": "Piotr Rasputin", "age": 40, "sex": "M", "blood_type": "B-", "CPRA": 7, "living_donor": False, "days_on_waitlist": 85, "location": "MetroHealth, OH", "distance": 138, "diabetes": False, "psot": False},
    {"id": 36, "name": "Illyana Rasputin", "age": 65, "sex": "F", "blood_type": "AB+", "CPRA": 97, "living_donor": False, "days_on_waitlist": 2400, "location": "NewYork-Presbyterian, NY", "distance": 535, "diabetes": True, "psot": True},
    {"id": 37, "name": "Bobby Drake", "age": 34, "sex": "M", "blood_type": "A+", "CPRA": 11, "living_donor": False, "days_on_waitlist": 150, "location": "Good Samaritan, OH", "distance": 108, "diabetes": False, "psot": False},
    {"id": 38, "name": "Laura Kinney", "age": 48, "sex": "F", "blood_type": "O+", "CPRA": 38, "living_donor": False, "days_on_waitlist": 3000, "location": "Emory Healthcare, GA", "distance": 560, "diabetes": False, "psot": False},
    {"id": 39, "name": "Sam Wilson", "age": 71, "sex": "M", "blood_type": "B+", "CPRA": 22, "living_donor": False, "days_on_waitlist": 1100, "location": "Cleveland Clinic Mercy, OH", "distance": 120, "diabetes": True, "psot": False},
    {"id": 40, "name": "Monica Rambeau", "age": 57, "sex": "F", "blood_type": "O-", "CPRA": 81, "living_donor": True, "days_on_waitlist": 480, "location": "Jefferson Health, PA", "distance": 445, "diabetes": True, "psot": True},
    {"id": 41, "name": "Bucky Barnes", "age": 26, "sex": "M", "blood_type": "A-", "CPRA": 0, "living_donor": False, "days_on_waitlist": 20, "location": "Miami Valley Hospital, OH", "distance": 80, "diabetes": False, "psot": False},
    {"id": 42, "name": "Felicia Hardy", "age": 62, "sex": "F", "blood_type": "AB-", "CPRA": 14, "living_donor": False, "days_on_waitlist": 1750, "location": "Loyola Medicine, IL", "distance": 325, "diabetes": True, "psot": False},
    {"id": 43, "name": "Eddie Brock", "age": 36, "sex": "M", "blood_type": "O+", "CPRA": 90, "living_donor": False, "days_on_waitlist": 2150, "location": "Massachusetts General, MA", "distance": 730, "diabetes": False, "psot": True},
    {"id": 44, "name": "Silver Sablinova", "age": 54, "sex": "F", "blood_type": "B+", "CPRA": 52, "living_donor": False, "days_on_waitlist": 920, "location": "Mercy Health, MI", "distance": 285, "diabetes": False, "psot": False},
    {"id": 45, "name": "Miles Morales", "age": 44, "sex": "M", "blood_type": "A+", "CPRA": 19, "living_donor": False, "days_on_waitlist": 3500, "location": "OhioHealth Grant, OH", "distance": 2, "diabetes": True, "psot": False},
    {"id": 46, "name": "Cindy Moon", "age": 32, "sex": "F", "blood_type": "O-", "CPRA": 6, "living_donor": True, "days_on_waitlist": 140, "location": "UPMC Hamot, PA", "distance": 195, "diabetes": False, "psot": False},
    {"id": 47, "name": "Frank Castle", "age": 69, "sex": "M", "blood_type": "B-", "CPRA": 47, "living_donor": False, "days_on_waitlist": 2600, "location": "University of Iowa, IA", "distance": 540, "diabetes": True, "psot": False},
    {"id": 48, "name": "Elektra Natchios", "age": 41, "sex": "F", "blood_type": "AB+", "CPRA": 76, "living_donor": False, "days_on_waitlist": 3600, "location": "Cleveland Clinic Main, OH", "distance": 142, "diabetes": False, "psot": True},
    {"id": 49, "name": "Marc Spector", "age": 51, "sex": "M", "blood_type": "O+", "CPRA": 28, "living_donor": False, "days_on_waitlist": 820, "location": "Mount Carmel East, OH", "distance": 12, "diabetes": True, "psot": False},
    {"id": 50, "name": "Maya Lopez", "age": 60, "sex": "F", "blood_type": "A-", "CPRA": 73, "living_donor": False, "days_on_waitlist": 1250, "location": "Inova Fairfax, VA", "distance": 385, "diabetes": False, "psot": True},
    {"id": 51, "name": "Danny Rand", "age": 45, "sex": "M", "blood_type": "B+", "CPRA": 9, "living_donor": False, "days_on_waitlist": 410, "location": "St. Elizabeth, KY", "distance": 115, "diabetes": False, "psot": False},
    {"id": 52, "name": "Colleen Wing", "age": 33, "sex": "F", "blood_type": "O+", "CPRA": 96, "living_donor": False, "days_on_waitlist": 1950, "location": "Brigham and Women's, MA", "distance": 730, "diabetes": False, "psot": True},
    {"id": 53, "name": "Shang-Chi", "age": 72, "sex": "M", "blood_type": "AB-", "CPRA": 3, "living_donor": True, "days_on_waitlist": 180, "location": "Kettering Health, OH", "distance": 78, "diabetes": True, "psot": False},
    {"id": 54, "name": "Katy Chen", "age": 38, "sex": "F", "blood_type": "O-", "CPRA": 59, "living_donor": False, "days_on_waitlist": 3100, "location": "Medical University of SC, SC", "distance": 630, "diabetes": False, "psot": False},
    {"id": 55, "name": "T'Challa", "age": 46, "sex": "M", "blood_type": "A+", "CPRA": 15, "living_donor": False, "days_on_waitlist": 550, "location": "Penn State Health, PA", "distance": 355, "diabetes": True, "psot": False},
    {"id": 56, "name": "Shuri", "age": 66, "sex": "F", "blood_type": "B+", "CPRA": 84, "living_donor": False, "days_on_waitlist": 2300, "location": "Hartford Hospital, CT", "distance": 620, "diabetes": True, "psot": True},
    {"id": 57, "name": "Clinton Barton", "age": 30, "sex": "M", "blood_type": "O+", "CPRA": 0, "living_donor": False, "days_on_waitlist": 25, "location": "Trinity Health, MI", "distance": 220, "diabetes": False, "psot": False},
    {"id": 58, "name": "Kate Bishop", "age": 42, "sex": "F", "blood_type": "A-", "CPRA": 48, "living_donor": False, "days_on_waitlist": 1350, "location": "Ascension St. John, MI", "distance": 215, "diabetes": False, "psot": False},
    {"id": 59, "name": "Bruce Rogers", "age": 53, "sex": "M", "blood_type": "B-", "CPRA": 91, "living_donor": False, "days_on_waitlist": 2800, "location": "Temple Health, PA", "distance": 440, "diabetes": True, "psot": True},
    {"id": 60, "name": "Sharon Carter", "age": 49, "sex": "F", "blood_type": "AB+", "CPRA": 10, "living_donor": True, "days_on_waitlist": 670, "location": "Fairview Health, MN", "distance": 745, "diabetes": False, "psot": False},
    {"id": 61, "name": "Nick Fury", "age": 34, "sex": "M", "blood_type": "O-", "CPRA": 23, "living_donor": False, "days_on_waitlist": 1150, "location": "University of Maryland, MD", "distance": 405, "diabetes": False, "psot": False},
    {"id": 62, "name": "Maria Hill", "age": 68, "sex": "F", "blood_type": "A+", "CPRA": 77, "living_donor": False, "days_on_waitlist": 400, "location": "Piedmont Atlanta, GA", "distance": 565, "diabetes": True, "psot": True},
    {"id": 63, "name": "Phil Coulson", "age": 37, "sex": "M", "blood_type": "O+", "CPRA": 1, "living_donor": False, "days_on_waitlist": 60, "location": "Community Health, IN", "distance": 175, "diabetes": False, "psot": False},
    {"id": 64, "name": "Melinda May", "age": 61, "sex": "F", "blood_type": "B+", "CPRA": 62, "living_donor": False, "days_on_waitlist": 3300, "location": "Carilion Clinic, VA", "distance": 310, "diabetes": True, "psot": False},
    {"id": 65, "name": "Daisy Johnson", "age": 43, "sex": "M", "blood_type": "AB-", "CPRA": 39, "living_donor": False, "days_on_waitlist": 1650, "location": "Main Line Health, PA", "distance": 440, "diabetes": False, "psot": False},
    {"id": 66, "name": "Jemma Simmons", "age": 55, "sex": "F", "blood_type": "O+", "CPRA": 95, "living_donor": False, "days_on_waitlist": 2100, "location": "Hackensack Meridian, NJ", "distance": 515, "diabetes": True, "psot": True},
    {"id": 67, "name": "Leo Fitz", "age": 29, "sex": "M", "blood_type": "A-", "CPRA": 13, "living_donor": True, "days_on_waitlist": 240, "location": "Genesis Health, OH", "distance": 55, "diabetes": False, "psot": False},
    {"id": 68, "name": "Bobbi Morse", "age": 47, "sex": "F", "blood_type": "B-", "CPRA": 56, "living_donor": False, "days_on_waitlist": 980, "location": "Hurley Medical, MI", "distance": 255, "diabetes": False, "psot": False},
    {"id": 69, "name": "Lance Hunter", "age": 70, "sex": "M", "blood_type": "O-", "CPRA": 0, "living_donor": False, "days_on_waitlist": 1200, "location": "St. Rita's, OH", "distance": 95, "diabetes": True, "psot": False},
    {"id": 70, "name": "Elena Rodriguez", "age": 52, "sex": "F", "blood_type": "AB+", "CPRA": 87, "living_donor": False, "days_on_waitlist": 2950, "location": "Thomas Jefferson, PA", "distance": 445, "diabetes": True, "psot": True},
    {"id": 71, "name": "Alphonso Mackenzie", "age": 40, "sex": "M", "blood_type": "A+", "CPRA": 31, "living_donor": False, "days_on_waitlist": 1500, "location": "University of Tennessee, TN", "distance": 470, "diabetes": False, "psot": False},
    {"id": 72, "name": "Idris Elba", "age": 58, "sex": "F", "blood_type": "O+", "CPRA": 44, "living_donor": False, "days_on_waitlist": 730, "location": "Spectrum Health, MI", "distance": 310, "diabetes": True, "psot": False},
    {"id": 73, "name": "Heimdall", "age": 35, "sex": "M", "blood_type": "B+", "CPRA": 93, "living_donor": False, "days_on_waitlist": 1850, "location": "St. Luke's, PA", "distance": 450, "diabetes": False, "psot": True},
    {"id": 74, "name": "Lady Sif", "age": 46, "sex": "F", "blood_type": "A-", "CPRA": 16, "living_donor": True, "days_on_waitlist": 420, "location": "Ohio State Wexner, OH", "distance": 0, "diabetes": False, "psot": False},
    {"id": 75, "name": "Thor Odinson", "age": 64, "sex": "M", "blood_type": "O-", "CPRA": 68, "living_donor": False, "days_on_waitlist": 2700, "location": "Cook County, IL", "distance": 320, "diabetes": True, "psot": False},
    {"id": 76, "name": "Jane Foster", "age": 31, "sex": "F", "blood_type": "AB-", "CPRA": 5, "living_donor": False, "days_on_waitlist": 80, "location": "Erie County Medical, NY", "distance": 325, "diabetes": False, "psot": False},
    {"id": 77, "name": "Loki Laufeyson", "age": 39, "sex": "M", "blood_type": "B+", "CPRA": 99, "living_donor": False, "days_on_waitlist": 3350, "location": "Robert Wood Johnson, NJ", "distance": 505, "diabetes": False, "psot": True},
    {"id": 78, "name": "Brunnhilde", "age": 67, "sex": "F", "blood_type": "O+", "CPRA": 27, "living_donor": False, "days_on_waitlist": 1100, "location": "Mercy Health Lorain, OH", "distance": 115, "diabetes": True, "psot": False},
    {"id": 79, "name": "Korg", "age": 48, "sex": "M", "blood_type": "A+", "CPRA": 41, "living_donor": False, "days_on_waitlist": 1900, "location": "WellSpan York, PA", "distance": 390, "diabetes": False, "psot": False},
    {"id": 80, "name": "Hela Odinsdottir", "age": 56, "sex": "F", "blood_type": "O-", "CPRA": 79, "living_donor": False, "days_on_waitlist": 2550, "location": "Cooper University, NJ", "distance": 450, "diabetes": True, "psot": True},
    {"id": 81, "name": "Pietro Maximoff", "age": 34, "sex": "M", "blood_type": "B-", "CPRA": 12, "living_donor": True, "days_on_waitlist": 310, "location": "Cleveland Clinic Akron, OH", "distance": 130, "diabetes": False, "psot": False},
    {"id": 82, "name": "Wasp", "age": 62, "sex": "F", "blood_type": "AB+", "CPRA": 61, "living_donor": False, "days_on_waitlist": 1400, "location": "Wake Forest, NC", "distance": 435, "diabetes": True, "psot": False},
    {"id": 83, "name": "Ant-Man", "age": 27, "sex": "M", "blood_type": "O+", "CPRA": 2, "living_donor": False, "days_on_waitlist": 55, "location": "Parkview Health, IN", "distance": 160, "diabetes": False, "psot": False},
    {"id": 84, "name": "Cassie Lang", "age": 73, "sex": "F", "blood_type": "A-", "CPRA": 98, "living_donor": False, "days_on_waitlist": 3000, "location": "NYU Langone, NY", "distance": 540, "diabetes": True, "psot": True},
    {"id": 85, "name": "Groot", "age": 44, "sex": "M", "blood_type": "B+", "CPRA": 35, "living_donor": False, "days_on_waitlist": 950, "location": "Larkin Community, FL", "distance": 980, "diabetes": False, "psot": False},
    {"id": 86, "name": "Gamora", "age": 54, "sex": "F", "blood_type": "AB-", "CPRA": 53, "living_donor": False, "days_on_waitlist": 2250, "location": "Reading Hospital, PA", "distance": 420, "diabetes": True, "psot": False},
    {"id": 87, "name": "Peter Quill", "age": 41, "sex": "M", "blood_type": "O-", "CPRA": 7, "living_donor": True, "days_on_waitlist": 470, "location": "Marietta Memorial, OH", "distance": 105, "diabetes": False, "psot": False},
    {"id": 88, "name": "Nebula", "age": 50, "sex": "F", "blood_type": "A+", "CPRA": 89, "living_donor": False, "days_on_waitlist": 1600, "location": "Geisinger Medical, PA", "distance": 415, "diabetes": False, "psot": True},
    {"id": 89, "name": "Drax", "age": 36, "sex": "M", "blood_type": "O+", "CPRA": 17, "living_donor": False, "days_on_waitlist": 120, "location": "Beaumont Health, MI", "distance": 210, "diabetes": False, "psot": False},
    {"id": 90, "name": "Mantis", "age": 69, "sex": "F", "blood_type": "B-", "CPRA": 43, "living_donor": False, "days_on_waitlist": 2400, "location": "Loyola Gottlieb, IL", "distance": 325, "diabetes": True, "psot": False},
    {"id": 91, "name": "Rocket Raccoon", "age": 43, "sex": "M", "blood_type": "AB+", "CPRA": 100, "living_donor": False, "days_on_waitlist": 3550, "location": "Rochester General, NY", "distance": 420, "diabetes": False, "psot": True},
    {"id": 92, "name": "Yondu Udonta", "age": 59, "sex": "F", "blood_type": "O-", "CPRA": 32, "living_donor": False, "days_on_waitlist": 810, "location": "Fairfield Medical, OH", "distance": 35, "diabetes": True, "psot": False},
    {"id": 93, "name": "Adam Warlock", "age": 32, "sex": "M", "blood_type": "A-", "CPRA": 0, "living_donor": True, "days_on_waitlist": 15, "location": "Mount Carmel Grove City, OH", "distance": 10, "diabetes": False, "psot": False},
    {"id": 94, "name": "Phyla-Vell", "age": 46, "sex": "F", "blood_type": "B+", "CPRA": 64, "living_donor": False, "days_on_waitlist": 1950, "location": "Richmond University, NY", "distance": 535, "diabetes": False, "psot": False},
    {"id": 95, "name": "Moondragon", "age": 51, "sex": "M", "blood_type": "O+", "CPRA": 82, "living_donor": False, "days_on_waitlist": 2850, "location": "Atlantic Health, NJ", "distance": 520, "diabetes": True, "psot": True},
    {"id": 96, "name": "Quasar", "age": 63, "sex": "F", "blood_type": "AB-", "CPRA": 11, "living_donor": False, "days_on_waitlist": 1550, "location": "Firelands Health, OH", "distance": 110, "diabetes": True, "psot": False},
    {"id": 97, "name": "Nova", "age": 38, "sex": "M", "blood_type": "A+", "CPRA": 54, "living_donor": False, "days_on_waitlist": 2100, "location": "Advocate Christ, IL", "distance": 320, "diabetes": False, "psot": False},
    {"id": 98, "name": "Wraith", "age": 55, "sex": "F", "blood_type": "O-", "CPRA": 97, "living_donor": False, "days_on_waitlist": 3450, "location": "Lenox Hill, NY", "distance": 540, "diabetes": True, "psot": True},
    {"id": 99, "name": "Cosmo", "age": 42, "sex": "M", "blood_type": "B+", "CPRA": 4, "living_donor": True, "days_on_waitlist": 620, "location": "Holzer Health, OH", "distance": 95, "diabetes": False, "psot": False},
    {"id": 100, "name": "Howard the Duck", "age": 60, "sex": "F", "blood_type": "A-", "CPRA": 21, "living_donor": False, "days_on_waitlist": 1300, "location": "Licking Memorial, OH", "distance": 40, "diabetes": True, "psot": False}
]

def filter_patients(patients_list, donor_blood_type, max_dist=250):
    viable_candidates = []
    blood_compatibility = {
        'O-': ['O-', 'O+', 'A-', 'A+', 'B-', 'B+', 'AB-', 'AB+'], 
        'O+': ['O+', 'A+', 'B+', 'AB+'],
        'A-': ['A-', 'A+', 'AB-', 'AB+'],
        'A+': ['A+', 'AB+'],
        'B-': ['B-', 'B+', 'AB-', 'AB+'],
        'B+': ['B+', 'AB+'],
        'AB-': ['AB-', 'AB+'],
        'AB+': ['AB+'] 
    }
    for p in patients_list:
        if p['distance'] > max_dist:
            continue
        allowed_recipients = blood_compatibility.get(donor_blood_type, [])
        if p['blood_type'] not in allowed_recipients:
            continue
        viable_candidates.append(p)
    return viable_candidates

def calculate_kdpi(age, height, weight, creat, htn_status, diabetes_status, cause_is_cva, is_dcd): 
    COEFFICIENTS = { 
    'age': 0.0092, 'age_lt_18': 0.0113, 'age_gt_50': 0.0067, 
    'height': -0.0557,'weight_lt_80': -0.0333, 
    'htn': 0.1106, 'diabetes': 0.2577, 
    'cva': 0.0743, 'creat': 0.2128,'creat_gt_15': -0.2199, 
    'dcd': 0.1966 
    } 
    SCALING_FACTOR = 1.40436817065005  
    PROB_DIABETES = 0.17280542134655
    PROB_HTN = 0.43697057162578 
    MAPPING_TABLE = [ 
    (0.4375634737, 0), (0.5414040068, 1), (0.5645538527, 2), (0.5822767079, 3),  
    (0.5965563936, 4), (0.6082839390, 5), (0.6207371839, 6), (0.6321475158, 7),  
    (0.6434741002, 8), (0.6531885148, 9), (0.6630277059, 10), (0.6714555226, 11),  
    (0.6808757096, 12), (0.6902927465, 13), (0.6975148320, 14), (0.7069428145, 15),  
    (0.7147392408, 16), (0.7235848222, 17), (0.7316576973, 18), (0.7399671386, 19),  
    (0.7479168270, 20), (0.7559520725, 21), (0.7638029049, 22), (0.7716042414, 23),  
    (0.7802136387, 24), (0.7885134615, 25), (0.7965851095, 26), (0.8038769241, 27),  
    (0.8107289473, 28), (0.8185610469, 29), (0.8262764295, 30), (0.8331833933, 31),  
    (0.8412154228, 32), (0.8493571574, 33), (0.8564584267, 34), (0.8646067488, 35),  
    (0.8743482730, 36), (0.8837213323, 37), (0.8926948221, 38), (0.9007716438, 39),  
    (0.9093133716, 40), (0.9173563289, 41), (0.9257144131, 42), (0.9347487513, 43),  
    (0.9439552666, 44), (0.9536014129, 45), (0.9614728985, 46), (0.9714150063, 47),  
    (0.9799698226, 48), (0.9891438569, 49), (1.0000000000, 50), (1.0089575801, 51),  
    (1.0195817549, 52), (1.0288055807, 53), (1.0372590435, 54), (1.0474854672, 55),  
    (1.0570103503, 56), (1.0668330560, 57), (1.0757289222, 58), (1.0856691217, 59),  
    (1.0953308886, 60), (1.1052996768, 61), (1.1156436456, 62), (1.1258322039, 63),  
    (1.1359620340, 64), (1.1460766478, 65), (1.1556148026, 66), (1.1659505755, 67),  
    (1.1759715823, 68), (1.1879706307, 69), (1.1995884012, 70), (1.2109225401, 71),  
    (1.2213786016, 72), (1.2339747939, 73), (1.2467030402, 74), (1.2591419526, 75),  
    (1.2715218612, 76), (1.2844627005, 77), (1.2975222691, 78), (1.3137209083, 79),  
    (1.3291359892, 80), (1.3442879921, 81), (1.3600269272, 82), (1.3764565767, 83),  
    (1.3927434388, 84), (1.4108897009, 85), (1.4288222435, 86), (1.4468967621, 87),  
    (1.4700089643, 88), (1.4911706744, 89), (1.5157259498, 90), (1.5416488091, 91),  
    (1.5691161499, 92), (1.6023999897, 93), (1.6366811444, 94), (1.6807640790, 95),  
    (1.7236885474, 96), (1.7799842198, 97), (1.8616822212, 98), (1.9867765454, 99),  
    (float('inf'), 100) ] 
    status_lower_htn = htn_status.lower().strip() 
    if status_lower_htn in ['y', 'yes']:  
        htn_val = 1.0 
    elif status_lower_htn in ['n', 'no']:  
        htn_val = 0.0 
    else:  
        htn_val = PROB_HTN 
    status_lower_diab = diabetes_status.lower().strip() 
    if status_lower_diab in ['y', 'yes']:  
        diab_val = 1.0 
    elif status_lower_diab in ['n', 'no']:  
        diab_val = 0.0 
    else:  
        diab_val = PROB_DIABETES 
    x_beta = 0 
    x_beta += COEFFICIENTS['age'] * (age - 40) 
    if age < 18: x_beta += COEFFICIENTS['age_lt_18'] * (age - 18) 
    if age > 50: x_beta += COEFFICIENTS['age_gt_50'] * (age - 50) 
    x_beta += COEFFICIENTS['height'] * ((height - 170) / 10) 
    if weight < 80: 
        x_beta += COEFFICIENTS['weight_lt_80'] * ((weight - 80) / 5) 
    x_beta += COEFFICIENTS['htn'] * htn_val 
    x_beta += COEFFICIENTS['diabetes'] * diab_val 
    if cause_is_cva: x_beta += COEFFICIENTS['cva'] 
    creat_capped = min(creat, 8.0)  
    x_beta += COEFFICIENTS['creat'] * (creat_capped - 1) 
    if creat_capped > 1.5:  
        x_beta += COEFFICIENTS['creat_gt_15'] * (creat_capped - 1.5) 
    if is_dcd: x_beta += COEFFICIENTS['dcd'] 
    kdri_rao = math.exp(x_beta) 
    kdri_scaled = kdri_rao / SCALING_FACTOR 
    keys = [x[0] for x in MAPPING_TABLE] 
    idx = bisect.bisect_left(keys, kdri_scaled) 
    kdpi_percent = MAPPING_TABLE[idx][1] 
    return kdpi_percent

def calculate_epts(age, has_diabetes, prior_transplant, years_on_dialysis):
    COEF_AGE = 0.047
    COEF_DIABETES = 0.399
    COEF_PRIOR_TX = 0.315
    COEF_DIALYSIS = 0.126
    REFERENCE_MEDIAN = -2.270
    raw_score = 0.0
    raw_score += COEF_AGE * (age - 25)
    raw_score += COEF_DIABETES * (1 if has_diabetes else 0)
    raw_score += COEF_PRIOR_TX * (1 if prior_transplant else 0)
    raw_score += COEF_DIALYSIS * years_on_dialysis
    EPTS_MAPPING = [
        (-3.0, 0), (-2.5, 5), (-2.0, 10), (-1.5, 15), (-1.0, 20),
        (-0.5, 30), (0.0, 40), (0.5, 50), (1.0, 60), (1.5, 70),
        (2.0, 80), (2.5, 90), (3.0, 95), (float('inf'), 100)
    ]
    for threshold, percentile in EPTS_MAPPING:
        if raw_score <= threshold:
            return percentile
    return 100

def calculate_kas(candidate_data, donor_data):
    kas_score = 0.0
    kas_score += candidate_data['waiting_days'] / 365.0
    if candidate_data['is_prior_living_donor']:
        kas_score += 4.0
    cpra = candidate_data['cpra']
    cpra_map = {
        100: 202.10, 99: 50.09, 98: 24.40, 97: 17.30, 96: 12.17,
        95: 10.82, 90: 6.71, 85: 4.05, 80: 2.46, 75: 1.58, 
        70: 1.09, 60: 0.81, 50: 0.48, 40: 0.34, 30: 0.21, 20: 0.08
    }
    cpra_score = 0.0
    for threshold in sorted(cpra_map.keys(), reverse=True):
        if cpra >= threshold:
            cpra_score = cpra_map[threshold]
            break
    kas_score += cpra_score
    epts = candidate_data['epts']
    kdpi = donor_data['kdpi']
    if epts <= 20 and kdpi <= 20:
        kas_score += 4.0
    age = candidate_data['age_at_match']
    if age < 18:
        kas_score += 3.0
    dist = candidate_data['distance_nm']
    if dist <= 250:
        kas_score += 4.0 - (dist / 250.0) * 2.0
    elif dist <= 2500:
        kas_score += 2.0 - ((dist - 250.0) / 2250.0) * 2.0
    return round(kas_score, 4)

def calculate_likelihood_score(patient, kdpi):
    likelihood = 0.0
    if patient['age'] > 65:
        likelihood += 25
    elif patient['age'] > 55:
        likelihood += 15
    elif patient['age'] > 45:
        likelihood += 5
    if patient['CPRA'] > 98:
        likelihood += 30
    elif patient['CPRA'] > 90:
        likelihood += 20
    elif patient['CPRA'] > 75:
        likelihood += 10
    years_waiting = patient['days_on_waitlist'] / 365.0
    if years_waiting > 5:
        likelihood += 20
    elif years_waiting > 3:
        likelihood += 10
    elif years_waiting > 1:
        likelihood += 5
    if patient['diabetes']:
        likelihood += 10
    if kdpi > 85 and patient['age'] > 65:
        likelihood += 25
    elif kdpi > 70 and patient['age'] > 60:
        likelihood += 15
    elif kdpi > 50 and patient['age'] > 50:
        likelihood += 5
    if patient['distance'] < 50:
        likelihood += 10
    elif patient['distance'] < 150:
        likelihood += 5
    return round(likelihood, 2)

st.title("🫘 Find My Kidney - Smart Kidney Allocation System")
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["About","👥 Patient Registry/Waitlist", "🏥 Kidney Allocation Engine"])

with tab1:
    st.header("Welcome to Find My Kidney!")
    st.markdown("""
    FindMyKidney is a web application designed to optimize the kidney allocation system by reducing patient wait times and kidney discard rates.
    The app modernizes kidney allocation with a streamlined interface that makes patient management and donor matching faster and more intuitive than current UNOS systems. 
    For marginal-quality kidneys (KDPI >20%), it implements dual-track batch processing: the system maintains legal KAS priority while simultaneously identifying candidates with high acceptance likelihood. 
    By notifying both tracks in parallel instead of sequentially, we reduce refusal cycles and cold ischemia time. 
    Since over 20 percent of recovered kidneys are high-KDPI and face the greatest discard risk, this approach accelerates placement for the most vulnerable organs while preserving allocation equity.   
                

    """)
    st.image("Gemini_Generated_Image_7gurtb7gurtb7gur.png", width = 300)

with tab2:
    st.header("Patient Registry")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Add New Patient")
        with st.form("add_patient_form"):
            name = st.text_input("Patient Name")
            age = st.number_input("Age", min_value=0, max_value=120, value=25)
            blood_type = st.selectbox("Blood Type", ['O+', 'O-', 'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-'])
            location = st.text_input("Location", value="New York, NY")
            distance = st.number_input("Distance from Hospital (miles)", min_value=0, value=500)
            cpra = st.number_input("CPRA Score", 0, 100, 0)
            psot = st.checkbox("Prior Solid Organ Transplant (PSOT)")
            diabetes_status = st.checkbox("Diabetes")
            sex_status = st.selectbox("Sex", ["M", "F"])
            living_donor_status = st.checkbox("Living Donor")
            submitted = st.form_submit_button("Add Patient")
            if submitted and name:
                new_patient = {
                'id': len(st.session_state.patients) + 1,
                'name': name,
                'age': age,
                'sex': sex_status, 
                'blood_type': blood_type,
                'CPRA': cpra,           
                'living_donor': living_donor_status,  
                'days_on_waitlist': 0,
                'location': location,
                'distance': distance,   
                'diabetes': diabetes_status, 
                'psot': psot          
            }
                st.session_state.patients.append(new_patient)
                st.success(f"✅ Added {name} to registry!")
    with col2:
        st.subheader("Updated Patient Waitlist")
        all_patients = st.session_state.patients
        sorted_patients = sorted(all_patients, key=lambda x: x['days_on_waitlist'], reverse=True)
        if st.session_state.patients:
            df = pd.DataFrame(sorted_patients)
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.info(f"📊 Total patients in registry: {len(st.session_state.patients)}")
        else:
            st.warning("No patients in registry yet.")

with tab3:
    st.header("KidneyMatch")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("New Kidney Available")
        with st.form("kidney_form"):
            st.write("**Donor Kidney Characteristics**")
            k_blood = st.selectbox("Blood Type", ['O+', 'O-', 'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-'], key='kidney_blood')
            k_age = st.number_input("Age", min_value=0, max_value=120, value=45)
            k_weight = st.number_input("Weight (kg)", min_value=0.0, value=70.0)
            k_height = st.number_input("Height (cm)", min_value=0.0, value=170.0)
            k_creatinine = st.number_input("Serum Creatinine (mg/dL)", min_value=0.0, value=1.0, step=0.1)
            st.write("**Medical History & COD**")
            k_hypertension = st.checkbox("History of Hypertension")
            k_diabetes = st.checkbox("History of Diabetes")
            k_stroke = st.checkbox("Death by Stroke")
            k_circulatory = st.checkbox("Circulatory Death (DCD)")
            k_location = st.text_input("Donor Location", value="Columbus, OH", disabled=True)
            find_match = st.form_submit_button("🔍 Find Best Match", type="primary")
    with col2:
        if find_match:
            kidney_data = {
                'blood_type': k_blood,
                'age': k_age,
                'weight': k_weight,
                'height': k_height,
                'creatinine': k_creatinine,
                'hypertension': k_hypertension,
                'diabetes': k_diabetes,
                'stroke': k_stroke,
                'circulatory': k_circulatory,
                'location': k_location
            }
            htn_val = "Yes" if k_hypertension else "No"
            dm_val = "Yes" if k_diabetes else "No"
            kdpi_score = calculate_kdpi(
                age=k_age,
                height=k_height,
                weight=k_weight,
                creat=k_creatinine,
                htn_status=htn_val,
                diabetes_status=dm_val,
                cause_is_cva=k_stroke,
                is_dcd=k_circulatory
            )
            viable_patients = filter_patients(st.session_state.patients, k_blood, max_dist=250)
            scored_patients = []
            for p in viable_patients:
                years_dialysis = p['days_on_waitlist'] / 365.0
                epts = calculate_epts(
                    age=p['age'],
                    has_diabetes=p['diabetes'],
                    prior_transplant=p['psot'],
                    years_on_dialysis=years_dialysis
                )
                c_data = {
                    'waiting_days': p['days_on_waitlist'],
                    'is_prior_living_donor': p['living_donor'],
                    'cpra': p['CPRA'],
                    'age_at_match': p['age'],
                    'epts': epts,
                    'distance_nm': p['distance']
                }
                p['kas_score'] = calculate_kas(c_data, {'kdpi': kdpi_score})
                p['likelihood_score'] = calculate_likelihood_score(p, kdpi_score)
                p['epts'] = epts
                scored_patients.append(p)
            track_a = sorted(scored_patients, key=lambda x: x['kas_score'], reverse=True)
            if kdpi_score > 20:
                track_b = sorted(track_a, key=lambda x: x['likelihood_score'], reverse=True)
            
            st.write("### 🏥 Allocation Results")
            col_k1, col_k2, col_k3 = st.columns(3)
            col_k1.metric("KDPI Score", f"{kdpi_score}%")
            col_k2.metric("Kidney Quality", "Premium" if kdpi_score < 20 else "Standard" if kdpi_score < 85 else "Poor")
            col_k3.metric("Viable Candidates", len(track_a))
            st.divider()
            
            st.write("Sorted list of ideal candidates")
            st.caption("Allocation order based on KAS score")
            
            batch_size = 5
            for i in range(0, min(len(track_a), 15), batch_size):
                batch = track_a[i:i+batch_size]
                batch_num = (i // batch_size) + 1

                st.subheader(f"Batch {batch_num}")
                df_batch = pd.DataFrame(batch)
                st.dataframe(
                    df_batch[['name', 'kas_score', 'epts', 'CPRA', 'age', 'days_on_waitlist', 'distance']],
                    use_container_width=True,
                    hide_index=True
                )
                if i + batch_size < min(len(track_a), 15):
                    st.markdown("---")
            
            if kdpi_score > 20:
                st.divider()
                st.warning(f"⚠️ **KDPI of {kdpi_score}% is greater than 20%** - Generating probability list to optimize acceptance rates")
                st.write("Candidates with high likelihood of acceptance")
                st.caption("List reordered by chance of acceptance - notified simultaneously to reduce refusal cycles")
                
                for i in range(0, min(len(track_b), 15), batch_size):
                    batch = track_b[i:i+batch_size]
                    batch_num = (i // batch_size) + 1

                    st.subheader(f"Batch {batch_num}")
                    df_batch = pd.DataFrame(batch)
                    st.dataframe(
                        df_batch[['name', 'likelihood_score', 'kas_score', 'age', 'CPRA', 'distance']],
                        use_container_width=True,
                        hide_index=True
                    )
                    if i + batch_size < min(len(track_b), 15):
                        st.markdown("---")