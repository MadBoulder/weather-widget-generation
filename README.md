# weather-widget-generation
Generate weather widgets for all the bouldering areas

## Overview

The main idea is to:
1. Retrieve list of locations from BetaLibrary's data folder
2. Geocode each of the locations and get its coordinates via [Open Cage's API](https://opencagedata.com/api)
3. Build the url and code of the widget required by [https://weatherwidget.io/](https://weatherwidget.io/)
4. Add the widget to each of the zone pages

## Requirements
* Python 3
* A free account and API key from Open Cage

## Usage
