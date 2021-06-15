const lanIP = `${window.location.hostname}:5000`;

let htmlTimesADay, htmlSecondInputFood, htmlSecondInputTime, htmlThirdInputFood, htmlThirdInputTime, htmlQ3, htmlQ4, htmlQ5, htmlQ6;

const addEventListeners = function () {
    htmlTimesADay.addEventListener('input', function () {
        checkValue();
    })
}

const checkValue = function () {
    console.log('checking')
    if (htmlTimesADay.value == 1) {
        htmlQ3.style.display = "none";
        htmlQ4.style.display = "none";
        htmlQ5.style.display = "none";
        htmlQ6.style.display = "none";
        htmlSecondInputFood.style.display = "none";
        htmlSecondInputTime.style.display = "none";
        htmlThirdInputFood.style.display = "none";
        htmlThirdInputTime.style.display = "none";
        listenToClickUpdate1();
        listenToClickUpdate2();
        listenToClickUpdate3();
    }
    else if (htmlTimesADay.value == 2) {
        htmlQ3.style.display = "flex";
        htmlQ4.style.display = "flex";
        htmlQ5.style.display = "none";
        htmlQ6.style.display = "none";
        htmlSecondInputFood.style.display = "flex";
        htmlSecondInputTime.style.display = "flex";
        htmlThirdInputFood.style.display = "none";
        htmlThirdInputTime.style.display = "none";
        listenToClickUpdate2();
        listenToClickUpdate3();
    }
    else if (htmlTimesADay.value == 3) {
        htmlQ3.style.display = "flex";
        htmlQ4.style.display = "flex";
        htmlQ5.style.display = "flex";
        htmlQ6.style.display = "flex";
        htmlSecondInputFood.style.display = "flex";
        htmlSecondInputTime.style.display = "flex";
        htmlThirdInputFood.style.display = "flex";
        htmlThirdInputTime.style.display = "flex";
        listenToClickUpdate3();
    }
}

const showUpdateKlaar = function(data) {
    console.log(data)
    const htmlEl = document.querySelector('.js-result');
    htmlEl.innerHTML = `Settings have been updated`;
    
}

const listenToClickUpdate1 = function (id) {
    id = 1
    const button = document.querySelector('.js-update');
    button.addEventListener('click', function () {
        const jsonobject = {
            Uur: document.querySelector('.js-food-time-input1').value,
            Hoeveelheid: document.querySelector('.js-food-input1').value,
        };
        handleData(`http://${lanIP}/schema/${id}`, showUpdateKlaar, null, 'PUT', JSON.stringify(jsonobject))
    })

}

const listenToClickUpdate2 = function (id) {
    id = 2
    const button = document.querySelector('.js-update');
    button.addEventListener('click', function () {
        const jsonobject = {
            Uur: document.querySelector('.js-food-time-input2').value,
            Hoeveelheid: document.querySelector('.js-food-input2').value,
        };
        handleData(`http://${lanIP}/schema/${id}`, showUpdateKlaar, null, 'PUT', JSON.stringify(jsonobject))
    })
}

const listenToClickUpdate3 = function (id) {
    id = 3
    const button = document.querySelector('.js-update');
    button.addEventListener('click', function () {
        const jsonobject = {
            Uur: document.querySelector('.js-food-time-input3').value,
            Hoeveelheid: document.querySelector('.js-food-input3').value,
        };
        handleData(`http://${lanIP}/schema/${id}`, showUpdateKlaar, null, 'PUT', JSON.stringify(jsonobject))
    })
}

const init = function () {
    htmlTimesADay = document.querySelector('.js-food-a-day')
    htmlSecondInputFood = document.querySelector('.js-food-input2')
    htmlSecondInputTime = document.querySelector('.js-food-time-input2')
    htmlThirdInputFood = document.querySelector('.js-food-input3')
    htmlThirdInputTime = document.querySelector('.js-food-time-input3')
    htmlQ3 = document.querySelector('.js-question3')
    htmlQ4 = document.querySelector('.js-question4')
    htmlQ5 = document.querySelector('.js-question5')
    htmlQ6 = document.querySelector('.js-question6')
    htmlQ3.style.display = "none";
    htmlQ4.style.display = "none";
    htmlQ5.style.display = "none";
    htmlQ6.style.display = "none";
    htmlSecondInputFood.style.display = "none";
    htmlSecondInputTime.style.display = "none";
    htmlThirdInputFood.style.display = "none";
    htmlThirdInputTime.style.display = "none";
    addEventListeners();
}

document.addEventListener("DOMContentLoaded", function () {
    console.info("DOM geladen");
    init();
  });