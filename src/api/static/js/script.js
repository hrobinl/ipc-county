import {addTooltips} from "../lib/tooltip.js"

const response = await fetch('http://127.0.0.1:5000/config');
const us = await response.json();
const counties = topojson.feature(us, us.objects.counties)
const states = topojson.feature(us, us.objects.states)
const diplomas = [ 'NoHSB', 'HSB', 'CAD', 'BD']

const updatePlot = () => {
    const dropdownCat = d3.select("#selCategory");
    const category = dropdownCat.property("value");
    const dropdownYear = d3.select("#selYear");
    const year = dropdownYear.property("value");
    plotData(`${category}${year}`)
}

d3.selectAll("#selCategory").on("change", updatePlot);
d3.selectAll("#selYear").on("change", updatePlot);

const plotData = async (category = 'Unemployed_2020') => {
    // fetch data from flask
    const data = await fetch('http://127.0.0.1:5000/map', {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json',
        },
        body: JSON.stringify({ data: category }),
    });

    // convert data to map
    const countyData = await data.json();
    const countyDataMap = new Map();
    const barData = []
    const barCat = category.split('_')[0]
    const scatData = []

    for (const key in countyData.map) {
        if (countyData.map.hasOwnProperty(key)) {
            countyDataMap.set(key, countyData.map[key]);
        }
    }
 
    for (const key in countyData.bar) {
        let i = 0
        countyData.bar[key].forEach( x => {
            let labels = ''
            if (diplomas.includes(category)) {
                labels = diplomas[i]
            } else {
                labels = `${barCat} 202${i}`
            }
            barData.push({
                "county":key,
                "category": labels,
                "data":x
            })
            i++
        });
    }

    console.log(countyData.scatter)

    for (const key in countyData.scatter) {
        if (countyData.scatter.hasOwnProperty(key)) {

            let scatObj = {
                "States": countyData.scatter[key][0],
                "Unemployment Rate": countyData.scatter[key][1],
            }
            scatObj[category] = countyData.scatter[key][2]
            scatData.push(scatObj)
        }
    }



    // set min and max
    const valuesArray = [...countyDataMap.values()]
    const maxValue = Math.max(...valuesArray);
    const minValue = Math.min(...valuesArray);


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
            percent: true,
            domain: [minValue, maxValue]
        }
    })

    const mapDiv = document.querySelector("#map");
    mapDiv.innerHTML = ''
    mapDiv.append(addTooltips(plotMap));

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

    const barDiv = document.querySelector("#bar");
    barDiv.innerHTML = ''
    barDiv.append(addTooltips(plotBar));

    const plotScatter = Plot.dot(scatData, {x: category, y: 'Unemployment Rate', stroke: "States"}).plot()

    const scatDiv = document.querySelector("#scatter");
    scatDiv.innerHTML = ''
    scatDiv.append(addTooltips(plotScatter));
}

await plotData()