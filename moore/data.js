
// data.js
const years = [
    1971, 1972, 1974, 1979, 1982, 1985, 1986, 1988, 1989, 1990, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 
    2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2016, 2017, 2018, 2019, 2020, 2021
];

const transistorCounts = [
    2308.2417, 3554.5222, 6097.5625, 29163.777, 135772.72, 273841.94, 273841.94, 273841.94, 1207900.8, 1207900.8,
    3105900.2, 3105900.2, 3105900.2, 9646616.0, 9646616.0, 9646616.0, 15261378.0, 21673922.0, 37180264.0, 42550656.0,
    220673400.0, 220673400.0, 273842000.0, 305052770.0, 582941600.0, 805842200.0, 805842200.0, 2308241400.0, 2308241400.0,
    2600000000.0, 2600000000.0, 5000000000.0, 5700000000.0, 8000000000.0, 19200000000.0, 21100000000.0, 39500000000.0,
    39500000000.0, 58200000000.0
];


const ctx = document.getElementById('moore').getContext('2d');
const chart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: years, // Loaded from data.js
        datasets: [{
            label: "",
            backgroundColor: 'rgb(255, 255, 255)',
            borderColor: 'rgb(0, 0, 255)',
            data: transistorCounts, // Loaded from data.js
            fill: false,
            tension: 0.5,
        }]
    },
    options: {
        maintainAspectRatio: false,
        responsive: true,
        title: {
            display: false,
            text: 'Transistor Count Over Years'
        },
        tooltips: {
            mode: 'index',
            intersect: false,
        },
        hover: {
            mode: 'nearest',
            intersect: true
        },
        plugins: {
            legend: {
              display: false
            }
        },
        elements: {
            point: {
                radius: 0
            }
        },
        scales: {
            x: {
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: 'Year'
                },
                grid: {
                    display: false // Set to false to remove grid lines
                },
                display: false,
            },
            y: {
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: 'Number of Transistors'
                },
                grid: {
                    display: false // Set to false to remove grid lines
                },
                display: false,
            }
        }
    }
});

