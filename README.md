# Carte de Contrôle Streamlit App
Video Demo: https://www.youtube.com/watch?v=h8924GEuNCU
## Description

The "Carte de Contrôle" Streamlit app is designed for statistical process control. It allows users to input data for quality control measurements, visualize control charts, and analyze the process capability. The app supports both X-bar (average) and R (range) charts.

## Features

- **Data Input**: Users can input quality control measurements for each sample.
- **Control Charts**: The app generates X-bar and R control charts with control limits and zones for monitoring process stability.
- **Data Analysis**: Detects points outside control limits, trends, and patterns in the data.
- **Process Capability Indices**: Calculates Cp, Pp, Cpk, and Ppk to assess short-term and long-term process capability.

## Installation

To run the app, follow these steps:

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/your-username/your-repository.git
   ```

2. Navigate to the project directory:

   ```bash
   cd your-repository
   ```

3. Install the required libraries using the following command:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

To launch the Streamlit app, run the following command:

```bash
streamlit run carte_de_controle_app.py
```

This will open the app in your default web browser. Follow the on-screen instructions to input data, visualize control charts, and analyze process capability.

## App Structure

- **Data Input Section**: Allows users to input quality control measurements, define control limits, and set sample size.
- **Control Charts Section**: Displays X-bar and R control charts with control limits and zones.
- **Data Analysis Section**: Detects points outside control limits and identifies trends or patterns.
- **Process Capability Section**: Calculates and displays process capability indices.

## Author

[Megdich Mohamed]


