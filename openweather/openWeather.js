/*!

Name: Open Weather
Dependencies: jQuery, OpenWeatherMap API
Author: Michael Lynch
Author URL: http://michaelynch.com
Date Created: August 28, 2013
Licensed under the MIT license

*/

// Source: https://github.com/michael-lynch/open-weather

;(function($) {

	$.fn.openWeather  = function(options) {

		// return if no element was bound
		// so chained events can continue
		if(!this.length) {
			return this;
		}

		// define default parameters
		const defaults = {
			// Widget configuration params
			wrapperTarget: null,
			descriptionTarget: null,
			maxTemperatureTarget: null,
			minTemperatureTarget: null,
			windSpeedTarget: null,
			humidityTarget: null,
			sunriseTarget: null,
			sunsetTarget: null,
			placeTarget: null,
			forecastTarget: null,
			iconTarget: null,
			customIcons: null,
			// Query params
			units: 'c',
			windSpeedUnit: 'Mps',
			city: null,
			lat: null,
			lng: null,
			key: null,
			exclude: null,
			lang: 'en',
			query: 'weather', // default (weather) is current weather. Use onecall for forecast predictions
			success: function() {}, // Callbacks
			error: function(message) {}
		}

		const plugin = this; // define plugin
		const el = $(this); // define element
		plugin.settings = {} // define settings
		plugin.settings = $.extend({}, defaults, options); // merge defaults and options
		const s = plugin.settings; // define settings namespace

		// format time function
		const formatTime = function(unixTimestamp) {
			const milliseconds = unixTimestamp * 1000; // define milliseconds using unix time stamp
			const date = new Date(milliseconds); // create a new date using milliseconds
			let hours = date.getHours(); // define hours
			if(hours > 12) {
				// calculate remaining hours in the day
				let hoursRemaining = 24 - hours;
				// redefine hours as the reamining hours subtracted from a 12 hour day
				hours = 12 - hoursRemaining;
			}
			let minutes = date.getMinutes(); // define minutes
			minutes = minutes.toString(); // convert minutes to a string
			// if minutes has less than 2 characters
			if(minutes.length < 2) {
				minutes = 0 + minutes;
			}
			let time = hours + ':' + minutes; // construct time using hours and minutes
			return time;
		}
		
		// format icon function
		const mapCustomIconToURL = function(defaultIconFileName, timeOfDay) {
			// let iconName;
			// // if icon is clear sky
			// if (defaultIconFileName == '01d' || defaultIconFileName == '01n') {
			// 	iconName = 'clear';
			// }
			// // if icon is clouds
			// if (defaultIconFileName == '02d' || defaultIconFileName == '02n' || defaultIconFileName == '03d' || defaultIconFileName == '03n' || defaultIconFileName == '04d' || defaultIconFileName == '04n') {
			// 	iconName = 'clouds';
			// }
			// // if icon is rain
			// if (defaultIconFileName == '09d' || defaultIconFileName == '09n' || defaultIconFileName == '10d' || defaultIconFileName == '10n') {
			// 	iconName = 'rain';
			// }
			// // if icon is thunderstorm
			// if (defaultIconFileName == '11d' || defaultIconFileName == '11n') {
			// 	iconName = 'storm';
			// }
			// // if icon is snow
			// if (defaultIconFileName == '13d' || defaultIconFileName == '13n') {
			// 	iconName = 'snow';
			// }
			// // if icon is mist
			// if (defaultIconFileName == '50d' || defaultIconFileName == '50n') {
			// 	iconName = 'mist';
			// }
			// define custom icon URL
			// return `${s.customIcons}${timeOfDay}/${iconName}.svg`;
			return `${s.customIcons}${timeOfDay}/${defaultIconFileName}.svg`;
		}

		// define basic api endpoint
		let apiURL = 'https://api.openweathermap.org/data/2.5/' + s.query + '?lang=' + s.lang;

		let weatherObj;

		let temperature;
		let minTemperature;
		let maxTemperature;
		let windSpeed;

		// if city isn't null
		if(s.city != null) {
			// define API url using city (and remove any spaces in city)
			apiURL += '&q=' + s.city;
		} else if(s.lat != null && s.lng != null) {
			// define API url using lat and lng
			apiURL += '&lat=' + s.lat + '&lon=' + s.lng;
		}
		if(s.key != null) {
			apiURL += '&appid=' + s.key;
		}
		if (s.exclude != null) {
			apiURL += '&exclude=' + s.exclude;
		}

		$.ajax({
			type: 'GET',
			url: apiURL,
			dataType: 'json',
			success: function(data) {
				if(data) {
					// adjust data to expected format
					if (s.query.localeCompare('onecall') == 0) {
						data.main = {
							temp: data.current.temp,
							temp_min: data.daily[0].temp.min,
							temp_max: data.daily[0].temp.max,
							humidity: data.current.humidity,
						}; 
						data.wind = {
							speed: data.current.wind_speed
						};
						data.sys = {
							sunrise: data.current.sunrise,
							sunset: data.current.sunset
						};
					}

					if(s.units == 'f') {
						// define temperature as fahrenheit
						temperature = Math.round(((data.main.temp - 273.15) * 1.8) + 32) + '°F';
						// define min temperature as fahrenheit
						minTemperature = Math.round(((data.main.temp_min - 273.15) * 1.8) + 32) + '°F';
						// define max temperature as fahrenheit
						maxTemperature = Math.round(((data.main.temp_max - 273.15) * 1.8) + 32) + '°F';
					} else {
						// define temperature as celsius
						temperature = Math.round(data.main.temp - 273.15) + '°C';
						// define min temperature as celsius
						minTemperature = Math.round(data.main.temp_min - 273.15) + '°C';
						// define max temperature as celsius
						maxTemperature = Math.round(data.main.temp_max - 273.15) + '°C';
					}

					// if windSpeedUnit is km/h
					windSpeed = (s.windSpeedUnit == 'km/h') ? data.wind.speed*3.6 : data.wind.speed;

					weatherObj = {
						city: (s.query.localeCompare('weather') == 0) ? `${data.name}, ${data.sys.country}` : '',
						temperature: {
							current: temperature,
							min: minTemperature,
							max: maxTemperature,
							units: s.units.toUpperCase()
						},
						description: (s.query.localeCompare('weather') == 0) ? data.weather[0].description : data.current.weather[0].description,
						windspeed: `${Math.round(windSpeed)} ${ s.windSpeedUnit }`,
						humidity: `${data.main.humidity}%`,
						sunrise: `${formatTime(data.sys.sunrise)} AM`,
						sunset: `${formatTime(data.sys.sunset)} PM`
					};
					
					// set temperature
					el.html(temperature);

					if(s.minTemperatureTarget != null) {
						// set minimum temperature
						$(s.minTemperatureTarget).text(minTemperature);
					}
					if(s.maxTemperatureTarget != null) {
						// set maximum temperature
						$(s.maxTemperatureTarget).text(maxTemperature);
					}
					// set weather description
					$(s.descriptionTarget).text(weatherObj.description);
					// if iconTarget and default weather icon aren't null
					icon = (s.query.localeCompare('weather') == 0) ? data.weather[0].icon : data.current.weather[0].icon;
					if (s.iconTarget != null && icon != null) {
						let iconURL;
						if(s.customIcons != null) {
							// define the default icon name
							const defaultIconFileName = icon;
							let timeOfDay;
							// if default icon name contains the letter 'd'
							if(defaultIconFileName.indexOf('d') != -1) {
								// define time of day as day
								timeOfDay = 'day';
							} else {
								// define time of day as night
								timeOfDay = 'night';
							}
							// append class modifier to wrapper
							$(s.wrapperTarget).addClass(timeOfDay);
							iconURL = mapCustomIconToURL(defaultIconFileName, timeOfDay);
						} else {
							// define icon URL using default icon
							iconURL = `https://openweathermap.org/img/wn/${icon}@2x.png`;
						}
						// set iconTarget src attribute as iconURL
						$(s.iconTarget).attr('src', iconURL);
					}
					if(s.placeTarget != null) {
						// set place
						$(s.placeTarget).text(weatherObj.city);
					}
					// if windSpeedTarget isn't null
					if(s.windSpeedTarget != null) {
						// set wind speed
						$(s.windSpeedTarget).text(weatherObj.windspeed);
					}
					// if humidityTarget isn't null
					if(s.humidityTarget != null) {
						// set humidity
						$(s.humidityTarget).text(weatherObj.humidity);
					}
					// if sunriseTarget isn't null
					if(s.sunriseTarget != null) {
						// set sunrise
						$(s.sunriseTarget).text(weatherObj.sunrise);
					}
					// if sunriseTarget isn't null
					if(s.sunsetTarget != null) {
						// set sunset
						$(s.sunsetTarget).text(weatherObj.sunset);
					}
					// run success callback
					s.success.call(this, weatherObj);
				}

				// handle daily forecast if the query asks to do so
				if (s.query.localeCompare('onecall') == 0) {
					for (let day = 1; day < data.daily.length-1; day++) {
						const forecast = data.daily[day];
						const weekday = moment.unix(data.daily[day].dt).format('dd');
						// Week day and icon
						var main_container = document.createElement("div");
						main_container.id = 'day_' + day.toString();
						var img = document. createElement("img");
						var el_span = document.createElement('span');
						el_span.setAttribute('style', 'font-size: medium; align-self: center;');
						var textNode = document.createTextNode(weekday);
						el_span.appendChild(textNode);
						if (s.customIcons != null) {
							img.src = mapCustomIconToURL(forecast.weather[0].icon, 'day');
						} else {
							// img.src = `https://openweathermap.org/img/wn/${forecast.weather[0].icon}@2x.png`;
							img.src = `https://openweathermap.org/img/wn/${forecast.weather[0].icon}.png`;
						}
						main_container.appendChild(img);
						var element = document.getElementById(s.forecastTarget);
						var holder = document.createElement("div");
						holder.setAttribute('class', 'd-flex flex-column justify-content-center');
						element.appendChild(holder)
						holder.appendChild(el_span);
						holder.appendChild(main_container);
					}
				}
			},
			error: function(jqXHR, textStatus, errorThrown) {
				// run error callback
				s.error.call(this, {
					error: textStatus
				});
			}
		});
	}
})(jQuery);
