# Ask Emily – AI Trip Planner, Travel Advisor, GPS & RV Technician Finder

Ask Emily is a comprehensive travel assistant for RV owners, combining AI-powered trip planning, customized GPS routing, and an RV technician locator, with integrated music generation for road trips. This project leverages Google Maps for navigation, Waze for real-time updates, and the Suno API to generate and download music tracks based on trip prompts. 

## Features

### 1. AI Trip Planner and Travel Advisor
- **Customized Trip Recommendations**: Provides personalized travel recommendations based on user preferences and RV specifications.
- **RV-Specific GPS Routing**: Uses Google Maps and Waze APIs to create safe, RV-tailored routes that avoid obstacles like low bridges.
- **Bridge Clearance Alerts**: Warns of bridge heights and other clearance issues.
- **Campground and Fuel Station Suggestions**: Displays nearby campgrounds and fuel stations (especially diesel) along the route.

### 2. RV Technician Finder
- **Taskrabbit-Style Technician Locator**: Helps users locate RV technicians via the RV Technician Association of America (RVTAA) directory.
- **Real-Time Access to Technicians**: Allows users to search for RV repair services by location and need, whether at home or on the road.

### 3. Suno API Integration for Music Generation
- **Music Generation**: Generates music based on prompts to enhance the road trip experience.
- **Downloadable Tracks**: Allows users to download generated songs to enjoy offline.

## Getting Started

### Prerequisites

Install the required Python packages:
```bash
pip install googlemaps requests python-dotenv
