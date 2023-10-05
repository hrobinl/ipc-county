import {addTooltips} from "../lib/tooltip.js"

const response = await fetch('http://127.0.0.1:5000/config');
const us = await response.json();
const counties = topojson.feature(us, us.objects.counties)
const states = topojson.feature(us, us.objects.states)
const diplomas = [ 'NoHSB', 'HSB', 'CAD', 'BD']
const labelsObj = {
    'laborforce': "Civilian Labor Force" ,
    'Employed': "Employed Population", 
    'Unemployed': "Unemployed Population",
    'POP': "Estimated Population", 
    'BIRTHS': "Birth Total", 
    'DEATHS': "Death Total",
    'NoHSB': "Citizens with no Highschool Diplomas", 
    'HSB': "Citizens with Highschool Diplomas only", 
    'CAD': "Citizens with Some College or Associates Degree", 
    'BD': "Citizens with Bachelors or higher"
}

// function to update plot via dropdown
const updatePlot = () => {
    const dropdownCat = d3.select("#selCategory");
    const category = dropdownCat.property("value");
    const dropdownYear = d3.select("#selYear");
    const year = dropdownYear.property("value");
    plotData(`${category}${year}`)
}

// listeners for dropdown
d3.selectAll("#selCategory").on("change", updatePlot);
d3.selectAll("#selYear").on("change", updatePlot);

// main function containing all three plots
const plotData = async (category = 'Unemployed_2020') => {
    // fetch data from flask
    const data = await fetch('http://127.0.0.1:5000/visuals', {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json',
        },
        body: JSON.stringify({ data: category }),
    });

    // initialize variables
    const catLabel = category.split('_')[0]
    const catYear = category.split('_')[1]
    const countyData = await data.json();
    const countyDataMap = new Map();
    const barData = []
    const scatData = []

    // create map variable for map plot
    for (const key in countyData.map) {
        if (countyData.map.hasOwnProperty(key)) {
            countyDataMap.set(key, countyData.map[key]);
        }
    }
    
    // create list of dict for bar plot
    for (const key in countyData.bar) {
        let i = 0
        countyData.bar[key].forEach( x => {
            let labels = ''
            if (diplomas.includes(catLabel)) {
                labels = labelsObj[diplomas[i]]
            } else {
                labels = `${catLabel} 202${i}`
            }
            barData.push({
                "county":key,
                "category": labels,
                "data":x
            })
            i++
        });
    }

    // create list of dict for scatter plot
    for (const key in countyData.scatter) {
        if (countyData.scatter.hasOwnProperty(key)) {

            let scatObj = {
                "County": countyData.scatter[key][0],
                "Unemployment Rate": countyData.scatter[key][1],
            }
            scatObj[labelsObj[catLabel]] = countyData.scatter[key][2]
            scatData.push(scatObj)
        }
    }



    // set min and max
    const valuesArray = [...countyDataMap.values()]
    const maxValue = Math.max(...valuesArray);
    const minValue = Math.min(...valuesArray);

    // create map
    const mapLabel = `${labelsObj[catLabel]} in ${catYear}`
    const plotMap = Plot.plot({
        projection: "albers-usa",
        marks: [
            Plot.geo(counties, { 
                fill: (d) => countyDataMap.get(`${Number(d.id)}`),
                title: (d) => `${d.properties.name} County \n ${countyDataMap.get(`${Number(d.id)}`)} ${category.split('_')[0]}`
            }),
            Plot.geo(states, {stroke: "#fff", strokeWidth: 0.5})
        ],
        color: {
            scheme: "pubugn",
            unknown: "#ddd",
            type: "linear",
            legend: true,
            label: mapLabel,
            percent: true,
            domain: [minValue, maxValue]
        }
    })

    // insert into html
    const mapDiv = document.querySelector("#map");
    mapDiv.innerHTML = ''
    mapDiv.append(addTooltips(plotMap));

    // create bar chart
    const plotBar = Plot.plot({
        x: {axis: null},
        y: {tickFormat: "s", grid: true},
        color: {scheme: "spectral", legend: true},
        width: 1000,
        marks: [
          Plot.barY(barData, {
            x: "category",
            y: "data",
            fill: "category",
            fx: "county",
            sort: {x: null, color: null, fx: {value: "-y", reduce: "sum"}}
          }),
          Plot.ruleY([0])
        ]
      })

    // insert into html
    const barDiv = document.querySelector("#bar");
    barDiv.innerHTML = ''
    barDiv.append(addTooltips(plotBar));

    // create scatter plot
    const plotScatter = Plot.dot(scatData, {
        x: labelsObj[catLabel], 
        y: 'Unemployment Rate', 
        stroke: "County",
        tip: true
    }).plot()

    // insert into html
    const scatDiv = document.querySelector("#scatter");
    scatDiv.innerHTML = ''
    scatDiv.append(addTooltips(plotScatter));
}

await plotData()