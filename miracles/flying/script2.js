// var map;

// function initMap() {
//     // Map initialization here (as per the previous example)
//     var customMapType = new google.maps.StyledMapType([
//         {
//             stylers: [
//                 { hue: '#000000' },
//                 { visibility: 'simplified' },
//                 { gamma: 0.5 },
//                 { weight: 0.5 }
//             ]
//         },
//         {
//             elementType: 'labels',
//             stylers: [{ visibility: 'off' }]
//         },
//         {
//             featureType: 'water',
//             stylers: [{ color: '#000000' }]
//         }
//     ], {
//         name: 'Custom Style'
//     });
//     var customMapTypeId = 'custom_style';

//     map = new google.maps.Map(document.getElementById('map'), {
//         zoom: 2,
//         center: { lat: -34.397, lng: 150.644 },  // Example coordinates
//         mapTypeControlOptions: {
//             mapTypeIds: [google.maps.MapTypeId.ROADMAP, customMapTypeId]
//         }
//     });

//     map.mapTypes.set(customMapTypeId, customMapType);
//     map.setMapTypeId(customMapTypeId);

//     // Define the marker position (latitude and longitude)
//     var markerPosition = { lat: -34.397, lng: 150.644 }; // Replace with your coordinates

//     // Create a marker and set its position
//     var marker = new google.maps.Marker({
//         position: markerPosition,
//         map: map,
//         title: 'Hello World!' // Optional: Text that appears when hovering over the marker
//     });
// }

// {lat: -34.397, lng: 150.644}

// function initMap() {
//     map = new google.maps.Map(document.getElementById('map'), {
//         center: {lat: 0, lng: 0},
//         zoom: 3,
//         mapId: '51e2bf18a2e84dde'
//         });

//     // Add markers or other functionalities here
// }

// Additional JavaScript code as needed for map functionalities



// mapboxgl.accessToken = 'pk.eyJ1IjoiamFyamFtb3JwIiwiYSI6ImNsb3Yzbm44MjBndnUycmxzanVqYTNnMXYifQ.xh8kxK-OJ5MlxCyafAzplw';
// const map = new mapboxgl.Map({
//     container: 'map', // container ID
//     // style: 'mapbox://styles/jarjamorp/clov361xa008501r651gg2vx7', // style URL 
//     style: 'mapbox://styles/mapbox/dark-v10',
//     center: [0, 0], // starting position [lng, lat]
//     zoom: 2, // starting zoom
// });

mapboxgl.accessToken = 'pk.eyJ1IjoiamFyamFtb3JwIiwiYSI6ImNsb3Yzbm44MjBndnUycmxzanVqYTNnMXYifQ.xh8kxK-OJ5MlxCyafAzplw';
const map = new mapboxgl.Map({
    container: 'map', // container ID
    // style: 'mapbox://styles/mapbox/streets-v12', // style URL
    style: 'mapbox://styles/jarjamorp/clov361xa008501r651gg2vx7/draft', // style URL 
    // style: 'mapbox://styles/jarjamorp/clov2ehih007f01pq2im5gd8h/draft',
    
    center: [0, 0], // starting position [lng, lat]
    zoom: 1.5 // starting zoom
});

// // Function to add a marker to the map
// function addMarker(lat, lng, label) {
//     new mapboxgl.Marker()
//         .setLngLat([lng, lat])
//         .setPopup(new mapboxgl.Popup({ offset: 25 }) // add popups
//             .setHTML(`<h3>${label}</h3>`))
//         .addTo(map);
// }

// // Read and parse the CSV file
// Papa.parse("assets/new.csv", {
//     download: true,
//     header: true,
//     complete: function(results) {
//         results.data.forEach(function(row) {
//             // Assuming columns are named 'lat', 'lon', 'hex', 'time'
//             addMarker(row.lat, row.lon, `Hex: ${row.hex}, Time: ${row.time}`);
//         });
//     }
// });

// // Function to add a marker to the map
// function addMarker(lat, lng, label) {
//     new mapboxgl.Marker()
//         .setLngLat([lng, lat])
//         .setPopup(new mapboxgl.Popup({ offset: 25 })
//             .setHTML(`<h3>${label}</h3>`))
//         .addTo(map);
// }

// // Time compression: 24 hours into 60 seconds
// const startTime = 1696118400.016; // First unix timestamp in your dataset
// const endTime = 1696204795.016; // Last unix timestamp in your dataset
// const realDuration = endTime - startTime; // Real time duration in seconds
// const animationDuration = 60; // Animation duration in seconds (1 minute)
// const timeScale = realDuration / animationDuration; // Scale factor

// let currentTime = startTime;

// // Read and parse the CSV file
// Papa.parse('assets/new.csv', {
//     download: true,
//     header: true,
//     complete: function(results) {
//         const data = results.data;
//         console.log('Data loaded:', data); // Debug: Check data format

//         const timer = setInterval(function() {
//             const virtualTime = currentTime + timeScale;
//             console.log('Current Time:', currentTime, 'Virtual Time:', virtualTime); // Debug: Check times

//             // Loop through data and add markers for the current virtual time
//             data.forEach(function(row) {
//                 if (parseFloat(row.time) >= currentTime && parseFloat(row.time) < virtualTime) {
//                     addMarker(row.lat, row.lon, `Hex: ${row.hex}, Time: ${row.time}`);
//                 }
//             });

//             currentTime = virtualTime;

//             // Stop the timer if the end of the dataset is reached
//             if (currentTime >= endTime) {
//                 clearInterval(timer);
//             }
//         }, 50); // Update every second
//     }
// });

// Function to get the earliest Unix timestamp from the parsed CSV data
function getEarliestTimestamp(parsedData) {
    if (!parsedData || parsedData.length === 0) {
        return null; // Return null if the parsed data is empty or not provided
    }

    // Assuming 'time' is the property name for the Unix timestamp in your data
    return parsedData.reduce((min, row) => {
        const timestamp = parseFloat(row.time);
        return timestamp < min ? timestamp : min;
    }, parseFloat(parsedData[0].time)); // Initialize with the timestamp of the first row
}

// Function to get the latest Unix timestamp from the parsed CSV data
function getLatestTimestamp(parsedData) {
    if (!parsedData || parsedData.length === 0) {
        return null; // Return null if the parsed data is empty or not provided
    }

    // Assuming 'time' is the property name for the Unix timestamp in your data
    return parsedData.reduce((max, row) => {
        const timestamp = parseFloat(row.time);
        return timestamp > max ? timestamp : max;
    }, parseFloat(parsedData[0].time)); // Initialize with the timestamp of the first row
}

// Function to add a marker to the map
function addMarker(lat, lng, label) {
    new mapboxgl.Marker()
        .setLngLat([lng, lat])
        .setPopup(new mapboxgl.Popup({ offset: 25 })
            .setHTML(`<h3>${label}</h3>`))
        .addTo(map);
}

// Constants
const realDuration = 24 * 60 * 60; // 24 hours in seconds
const animationDuration = 60; // Animation duration in seconds
const timeScale = realDuration / animationDuration; 
const tickDuration = realDuration / (animationDuration * 20); // 20 ticks per second

// Variables
let currentTime = getEarliestTimestamp(); // Function to get the earliest timestamp from your data

startTime = 1696118400.016; // First unix timestamp in your dataset
const endTime = 1696204795.016; // Last unix timestamp in your dataset

Papa.parse('assets/unique_flight_data.csv', {
    download: true,
    header: true,
    complete: function(results) {
        const flightData = results.data;
        console.log('Data loaded:', flightData); // Debug: Check data format

        // Interval for animation
        const interval = setInterval(() => {

            // Iterate through your flight data here
            flightData.forEach(flight => {
                const flightTime = parseFloat(flight.time);
                // console.log('Comparing:', flightTime, 'with range:', startTime, 'to', startTime + tickDuration);

                // Check if flight time is within the current animation frame
                if (flightTime >= startTime && flightTime < startTime + tickDuration) {
                    // Add marker logic here
                    addMarker(flight.lat, flight.lon);
                }
            });

            startTime += tickDuration;

            // Check if animation is complete
            if (startTime >= endTime) {
                clearInterval(interval);
            }
        }, 50);
    }
});



