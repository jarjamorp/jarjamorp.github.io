// Initialize the map
var map = L.map('map').setView([0, 0], 2); // Latitude and Longitude of the map's initial center and the initial zoom level

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

//         // Optional: Customize the marker based on flight status or other criteria
//         if (status === 'landed') {
//             // Create a custom div element for the firework effect
//             var flashMarker = L.divIcon({
//                 className: 'flash-marker',
//                 iconSize: [10, 10]
//             });

//             // Place the custom marker on the map
//             L.marker([lat, lng], { icon: flashMarker }).addTo(map);
//         }
//     });
// }

function processAndDisplayFlights(data) {
    for (let i = 0; i < 10000 && i < data.length; i++) {
        // Introduce a delay for each iteration
        setTimeout(function() {
            const [lat, lng, status] = data[i];

            if (status === 'landed') {
                // Create a custom div element for the firework effect
                var flashMarker = L.divIcon({
                    className: 'firework-marker',
                    iconSize: [100, 100]
                });

                // Place the custom marker on the map
                L.marker([lat, lng], { icon: flashMarker }).addTo(map);
            }
        }, i * 5); // 200 milliseconds delay per iteration
    }
}






// Call the function to fetch data
fetchFlightData();
