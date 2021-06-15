const lanIP = `${window.location.hostname}:5000`;
const socket = io(`http://${lanIP}`);

let htmlWaterSchema, htmlFoodSchema, htmlLastTimeAte, htmlFsrFood, htmlFsrWater, htmlWatersensor, htmlDmsFood, htmlDmsWater;

const listenToUI = function () {
  let button_water = document.querySelector(".js-fill-water");
  button_water.addEventListener("click", function () {
      console.log("button water pressed");
      socket.emit("F2B_activate_waterpump", 1);
  });

  let button_food = document.querySelector(".js-fill-food");
  button_food.addEventListener("click", function () {
      console.log("button food pressed");
      socket.emit("F2B_activate_motor", 1);
  });

  let button_shutdown = document.querySelector('.js-shutdown');
  button_shutdown.addEventListener('click', function () {
      console.log('Shutting down')
      socket.emit('F2B_shutdown')
  })
};

const listenToSocket = function () {
  socket.on('connected', function () {
    console.log("verbonden met socket webserver");
  })

  socket.on('message', function (msg) {
    console.log(`${msg}`)
    socket.send(msg)
    socket.emit('F2B_data');
  });

  socket.on("B2F_update_value_fsr_food", function(jsonObject) {
      console.log('Update value fsr food: ', jsonObject);
      console.log(htmlFsrFood)
      htmlFsrFood.innerHTML = `${jsonObject.Waarde}`;
  })

  socket.on("B2F_update_value_fsr_water", function(jsonObject) {
        console.log('Update value fsr water: ', jsonObject);
        console.log(htmlFsrWater)
        htmlFsrWater.innerHTML = `${jsonObject.Waarde}`;
  })

  socket.on("B2F_update_value_dms_food", function (jsonObject) {
      console.log('Update value dms food: ', jsonObject);
      console.log(htmlDmsFood)
      htmlDmsFood.innerHTML = `${jsonObject.Dag} ${jsonObject.Uur}`
    })

  socket.on("B2F_update_value_dms_water", function (jsonObject) {
    console.log('Update value dms water: ', jsonObject);
    console.log(htmlDmsWater)
    htmlDmsWater.innerHTML = `${jsonObject.Dag} ${jsonObject.Uur}`
})

  socket.on("B2F_update_value_watersensor", function(jsonObject) {
    console.log('Update value watersensor: ', jsonObject);
    console.log(htmlWatersensor)
    if (jsonObject.Waarde == 0) {
        htmlWatersensor.innerHTML = `No`;
    }
    else if (jsonObject.Waarde == 1 ) {
        htmlWatersensor.innerHTML = `Enough`;
    }
    
})


  getSchemaWater();
  getSchemaFood();
  getLastTimeAte();
  getLastTimeDrank();
  };

  const showDataFood = function(data) {
      let converted_labels = []
      let converted_data = []
      for (const row of data) {
          converted_labels.push(row.AteToday)
          converted_data.push(row.DailyFood)
      }
  }


  const drawChartFood = function() {
      var options = {
          chart: {
              height: 340,
              type: "radialBar"
          },
          series: [70],
          colors: ["#FF0077"],
          plotOptions: {
              radialBar: {
                  hollow: {
                      margin: 15,
                      size: "70%"
                  },

                  track: {
                      background: "#4D4549"
                  },

                  dataLabels: {
                      showOn: "always",
                      name: {
                          show: false,
                      },
                      value: {
                          color: "#4D4549",
                          fontSize: "50px",
                          fontFamily: 'semplicitapro',
                          fontWeight: 500,
                          show: true
                      }
                  }
              }
          }
        }
      var FoodChart = new ApexCharts(document.querySelector(".js-chart-food"), options);
      FoodChart.render();
  }

  const drawChartWater = function() {
    var options = {
        chart: {
            height: 340,
            type: "radialBar"
        },

        series: [35],
        colors: ["#FF0077"],
        plotOptions: {
            radialBar: {
                hollow: {
                    margin: 15,
                    size: "70%"
                },
                track: {
                    background: "#4D4549"
                },

                dataLabels: {
                    showOn: "always",
                    name: {
                        show: false,
                    },
                    value: {
                        color: "#4D4549",
                        fontSize: "50px",
                        fontFamily: 'semplicitapro',
                        fontWeight: 500,
                        show: true
                    }
                }
            }
        }
    };

    var WaterChart = new ApexCharts(document.querySelector(".js-chart-water"), options);
    console.log('maak chart')
    WaterChart.render();
  }


  const showSchemaWater = function (data) {
    const tableWater = document.querySelector('.js-water');
    let htmlWater = `<caption class="first-row">Current water settings</caption>`
    for (const row of data) {
        if (row.Hoeveelheid != 0) {
                htmlWater += `<tr>
                <td>${row.Uur}</td>
                <td>${row.Hoeveelheid}ml</td>
                </tr>`
        }
 
    }
    tableWater.innerHTML = htmlWater;
  }

  const showSchemaFood = function (data) {
    const tableFood = document.querySelector('.js-food');
    let htmlFood = `<caption class="first-row">Current food settings</caption>`
    for (const row of data) {
        if (row.Hoeveelheid != 0) {
                  htmlFood += `<tr>
                    <td>${row.Uur}</td>
                    <td>${row.Hoeveelheid}g</td>
                    </tr>`
        }
    tableFood.innerHTML = htmlFood;
  }
}
const showLastTimeAte = function(data) {
    htmlDmsFood.innerHTML = `${data.Dag} ${data.Uur}`
}

const showLastTimeDrank = function(data) {
  htmlDmsWater.innerHTML = `${data.Dag} ${data.Uur}`
}

const getLastTimeAte = function() {
    handleData(`http://${lanIP}/lasttimeate`, showLastTimeAte, null, "GET")
}

const getLastTimeDrank = function() {
    handleData(`http://${lanIP}/lasttimedrank`, showLastTimeDrank, null, "GET")
}
const getSchemaWater = function() {
  handleData(`http://${lanIP}/schemawater`, showSchemaWater, null, "GET")
}

const getSchemaFood = function() {
    handleData(`http://${lanIP}/schemafood`, showSchemaFood, null, "GET")
  }
  
document.addEventListener("DOMContentLoaded", function () {
    console.info("DOM geladen");
    htmlFsrFood = document.querySelector('.js-bowl-food');
    htmlFsrWater = document.querySelector('.js-bowl-water');
    htmlWatersensor = document.querySelector('.js-tank-water');
    htmlDmsFood = document.querySelector('.js-time-food');
    htmlDmsWater = document.querySelector('.js-time-water')
    listenToSocket();
    listenToUI();
    drawChartFood();
    drawChartWater();
  });