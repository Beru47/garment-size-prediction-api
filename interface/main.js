client = {
    "gender": null,
    "height_cm": null,
    "weight_kg": null,
    "morphology": null 
}

morphology_female_mapping = {
    0 : "A",
    1 : "X",
    2 : "8",
    3 : "V",
    4 : "H",
    5 : "O"
}

morphology_male_mapping = {
    0 : "V",
    1 : "H",
    2 : "O"
}

class Slider {
    constructor(rangeElement, valueElement, options) {
        this.rangeElement = rangeElement
        this.valueElement = valueElement
        this.options = options

        this.rangeElement.addEventListener('input', this.updateSlider.bind(this))
    }

    init() {
        this.rangeElement.setAttribute('min', this.options.min)
        this.rangeElement.setAttribute('max', this.options.max)
        this.rangeElement.value = this.options.cur

        this.updateSlider()
    }

    asMoney(value) {
        return parseFloat(value)
        .toLocaleString('en-US', {
            maximumFractionDigits: 2
        })
    }

    generateBackground() {
        if(this.rangeElement.value === this.options.min) {
            return
        }

        let percentage = (this.rangeElement.value - this.options.min) / (this.options.max - this.options.min) * 100
        return 'background: linear-gradient(to right, #50299c, #932e3e ' + percentage + '%, #d3edff ' + percentage + '%, #dee1e2 100%)'
    }

    updateSlider() {
        this.valueElement.innerHTML = this.asMoney(this.rangeElement.value)
        this.rangeElement.style = this.generateBackground(this.rangeElement.value)
    }
}

var options = {
    min: 140,
    max: 220,
    cur: 160
}

items = document.querySelectorAll(".item");

male_button = document.getElementById("male");
female_button = document.getElementById("female");
slider_male = document.getElementsByClassName("slider-male")[0];
slider_female = document.getElementsByClassName("slider-female")[0];

step1 = document.getElementsByClassName("step1")[0];
step2 = document.getElementsByClassName("step2")[0];
step3 = document.getElementsByClassName("step3")[0];
step4 = document.getElementsByClassName("step4")[0];
step5 = document.getElementsByClassName("step5")[0];

let next = document.getElementById("next");
let prev = document.getElementById("prev");

let set_height = document.getElementById("set-height");
let set_weight = document.getElementById("set-weight");

var active_items = [];
var active;
var slider;

function loadShow(){

    active_items[active].style.transform = `none`;
    active_items[active].style.zIndex = 1;
    active_items[active].style.filter = "none";
    active_items[active].style.opacity = 1;

    let stt = 0;
    for(var i = active + 1; i < active_items.length; i++){
        stt++;
        active_items[i].style.transform = `translateX(${120*stt}px) scale(${1-0.2*stt}) perspective(16px) rotateY(-1deg)`;
        active_items[i].style.zIndex = -stt;
        active_items[i].style.filter = "blur(5px)";
        active_items[i].style.opacity = (stt>2)?0:0.6;
    }
    stt = 0;
    for(var i = active - 1; i >=0; i--){
        stt++;
        active_items[i].style.transform = `translateX(${-120*stt}px) scale(${1-0.2*stt}) perspective(16px) rotateY(1deg)`;
        active_items[i].style.zIndex = -stt;
        active_items[i].style.filter = "blur(5px)";
        active_items[i].style.opacity = (stt>2)?0:0.6;
    }
}

function generateTableRows(data){
    let html = '';
    for (let key in data) {
        html += `<tr>
                    <td>${key}</td>
                    <td>${data[key]}</td>
                </tr>`;
    }
    return html;
}

function updateTable(data){
    let tableBody = document.getElementById('measurementsTableBody');
    if (tableBody) {
        tableBody.innerHTML = generateTableRows(data);
    }
}

male_button.addEventListener('click', () =>{
    step1.style.display = "none";
    step2.style.display = "block";
    slider_male.style.display = "block";

    client["gender"] = 1;

    for(var i = 0; i < items.length; i++){
        if(items[i].parentElement.style.display !== ""){
            active_items.push(items[i]);
        }
    }

    active = 1;
    loadShow();

})

female_button.addEventListener('click', () =>{
    step1.style.display = "none";
    step2.style.display = "block";
    slider_female.style.display = "block";

    client["gender"] = 0;

    for(var i = 0; i < items.length; i++){
        if(items[i].parentElement.style.display !== ""){
            active_items.push(items[i]);
        }
    }

    active = 3;
    loadShow();

})

next.addEventListener('click', () =>{
    active = active+1 < active_items.length?active+1:active;
    loadShow();
})

prev.addEventListener('click', () =>{
    active = active-1 >= 0?active-1:active;
    loadShow();
})

choose.addEventListener('click', (e) =>{

    e.preventDefault();

    step2.style.display = "";
    step3.style.display = "flex";

    if(client["gender"]) client["morphology"] = morphology_male_mapping[active];
    else client["morphology"] = morphology_female_mapping[active];

    let rangeElement = document.querySelector('.step3 .range [type="range"]')
    let valueElement = document.querySelector('.step3 .range .range_value span')


    if(rangeElement) {
        slider = new Slider(rangeElement, valueElement, options)
        slider.init()
    }

})

set_height.addEventListener('click', (e) =>{

    e.preventDefault();

    step3.style.display = "";
    step4.style.display = "flex";

    client["height_cm"] = document.querySelector('.step3 .range [type="range"]').value;

    options = {
        min: 44,
        max: 220,
        cur: 70
    }

    let rangeElement = document.querySelector('.step4 .range [type="range"]');
    let valueElement = document.querySelector('.step4 .range .range_value span');

    slider = new Slider(rangeElement, valueElement, options)
    slider.init();

})

set_weight.addEventListener('click', (e) =>{

    e.preventDefault();

    client["weight_kg"] = document.querySelector('.step4 .range [type="range"]').value;

    console.log(client);

    const requiredFields = {
        user_id: null,
        gender: null,
        adult: 1,
        height_cm: null,
        weight_kg: null,
        morphology: null,
        Head_Circumference: null,
        Right_Elbow: null,
        Biceps: null,
        Waist_Circumference: null,
        Chest_Circumference: null,
        Chest_Base: null,
        Right_Knee: null,
        Left_Knee: null,
        Right_Calf: null,
        Left_Calf: null,
        High_Hip: null,
        Low_Hip: null,
        Right_Thigh: null,
        Right_Thigh_Widest: null,
        Left_Thigh: null,
        Left_Thigh_Widest: null,
        Shoulder_Width: null,
        Arm_Length: null,
        Trunk_Length: null,
        Leg_Length: null,
    };
    
    for (let key in client) {
        if (requiredFields.hasOwnProperty(key)) {
            requiredFields[key] = client[key];
        }
    }
    
    let id  = Math.floor(Date.now() / 1000);
    let csvContent = `user_id,${id}
gender,${requiredFields.gender}
adult,${requiredFields.adult}
height_cm,${requiredFields.height_cm}
weight_kg,${requiredFields.weight_kg}
morphology,${requiredFields.morphology}
Head_Circumference,null
Right_Elbow,null
Biceps,null
Waist_Circumference,null
Chest_Circumference,null
Chest_Base,null
Right_Knee,null
Left_Knee,null
Right_Calf,null
Left_Calf,null
High_Hip,null
Low_Hip,null
Right_Thigh,null
Right_Thigh_Widest,null
Left_Thigh,null
Left_Thigh_Widest,null
Shoulder_Width,null
Arm_Length,null
Trunk_Length,null
Leg_Length,null`;

    let csvBlob = new Blob([csvContent], { type: 'text/csv' });

    let formData = new FormData();
    formData.append('file', csvBlob, 'client_data.csv'); 

    fetch('http://127.0.0.1:8000/add_client', {
        method: 'POST',
        body: formData,
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Network response was not ok: ${response.status} - ${response.statusText}`);
        }
        return response.json();
    })
    .then(data => {
        console.log("Response from add_client API:", data);

        fetch(`http://127.0.0.1:8000/get_measures_predictions/${id}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Network response was not ok: ${response.status} - ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            console.log("Response from get_measures_predictions API:", data);

            updateTable(data["Measures Prediction"]);
            
            step4.style.display = "";
            step5.style.display = "block";

        })
        .catch(error => {
            console.error('Error fetching get_measures_predictions API:', error);
        });

    })
    .catch(error => {
        console.error('Error fetching add_client API:', error);
    });
})