# ShionX

## Project Overview

ShionX is a project that aims to create a comprehensive system integrating audio, test and memory processing using various technologies. This document provides an overview and setup instructions.

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/felt404/ShionX.git
   cd ShionX
   ```
2. Create a Virtual Environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   uvicorn backend.main:app --reload
   ```
