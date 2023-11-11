// Initialize the map
var map = L.map('map').setView([51.505, -0.09], 2); // Latitude and Longitude of the map's initial center and the initial zoom level

// Add a tile layer to add to our map
// Here, we're using OpenStreetMap's free tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
    maxZoom: 18,
}).addTo(map);

// Function to fetch flight data
function fetchFlightData() {
    const apiUrl = 'https://airlabs.co/api/v9/flights?_view=array&_fields=lat,lng,status&api_key=64eba062-3441-496f-8bd8-065df91e5e99';

    fetch(apiUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            // console.log(data); 
            processAndDisplayFlights(data); // Call the new function with the fetched data
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
        });
}

// function processAndDisplayFlights(data) {
//     data.forEach(flight => {
//         const [lat, lng, status] = flight;

//         // Create a marker and add it to the map
//         var marker = L.marker([lat, lng]).addTo(map);

//         // Optional: Customize the marker based on flight status or other criteria
//         if (status === 'landed') {
//             marker.bindPopup('Flight Landed');
//         }
//     });
// }

function processAndDisplayFlights(data) {
    // Process only the first 100 rows
    for (let i = 0; i < 10000 && i < data.length; i++) {
        const [lat, lng, status] = data[i];

        // Customize the marker popup based on flight status
        if (status === 'landed') {
            // Create a marker and add it to the map
            var marker = L.marker([lat, lng]).addTo(map);
            marker.bindPopup('Flight Landed');
        } else {
            // marker.bindPopup('Flight Status: ' + status);
        }
    }
}


// Call the function to fetch data
fetchFlightData();
