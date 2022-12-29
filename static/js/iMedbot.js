const BOT_IMG = "static/img/robot.svg";
const NURSE_IMG = "static/img/nurse.svg"
const PERSON_IMG = "static/img/woman.svg";
const BOT_NAME = "iMedBot";
PERSON_NAME = "You";
var input_question = JSON.parse(input_question)
var input_question10 = JSON.parse(input_question10)
var input_question5 = JSON.parse(input_question5)
train_model_year=0

var input = []
const SURVEY = "BYE, It is my pleasure to help you,Have a nice day!How many stars you can give us?"

var patientParameter_dis = {"race": "race_dis",
    "ethnicity": "ethnicity_dis",
    "smoking": "smoking_dis",
    "alcohol_useage": "alcohol_useage_dis",
    "family_history": "family_history_dis",
    "age_at_diagnosis": "age_at_diagnosis_dis",
    "menopause_status": "menopause_status_dis",
    "side": "side_dis",
    "TNEG": "TNEG_dis"}

// get the element for html
// Icons made by Freepik from www.flaticon.com
const msgerForm = get(".msger-inputarea");
const msgerInput = get(".msger-input");
const msgerChat = get(".msger-chat");

// const css ='<link rel="stylesheet" href="http://cdn.bootcss.com/bootstrap/3.3.0/css/bootstrap.min.css">\n' +
//     '    <script src="http://cdn.bootcss.com/jquery/1.11.1/jquery.min.js"></script>\n' +
//     '    <script src="http://cdn.bootcss.com/bootstrap/3.3.0/js/bootstrap.min.js"></script>'

const css ='<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">\n' +
    '    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>\n' +
    '    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>'

$body = $("body");

$(document).on({
    ajaxStart: function() { $body.addClass("loading");    },
     ajaxStop: function() { $body.removeClass("loading"); }
});



msgerForm.addEventListener("submit", event => {
console.log("11111111111");
alert("done")
  event.preventDefault();
  const msgText = msgerInput.value;
  if (!msgText) return;
  appendMessage(PERSON_NAME, PERSON_IMG, "right", msgText,"no information",[]);
  msgerInput.value = "";
  botResponse(msgText);
});



/**
 * @param {string} name if it is robot or user
 * @param {string} img the robot img or user img
 * @param {string} side location of dialogue right or left
 * @param {string} text the value of input
 */

function getValue(event){
    console.log(event)
    var radio = document.getElementsByClassName('stars');
    //var text = document.getElementById("usersuggestion");
    //console.log("70",text);
    console.log("72",radio);


    console.log(radio.length());

    for (i=0; i<radio.length(); i++) {
        if (radio[i].checked==true) {
            alert(radio[i].id)
        }
    }
    //$.post("/submitsurvey", {
      //          radio:radio,
        //        text:text
          //  }).done(function (data) {
       //         console.log(data)
            //})
}
var alreaView = false
function gobacktoBrowse() {
    console.log("11111111111");
alert("done")
    location.reload();
    text = "I can either predict breast cancer metastasis for your patient based on our deep learning models trained using one existing dataset,or I can train a model for you if you can provide your own dataset, so how do you want to proceed?Please enter 1 for the first choice, or 2 for the second choice"
    appendMessage(BOT_NAME, NURSE_IMG, "left", text,"no information",{"Predict":"Predict","Train a Model":"Train a Model"})

}
function uploadData(e) {
    add_userMsg("Upload Local Dataset")
    document.getElementById('fileid').click();
    if (alreaView == false){

        document.getElementById("fileid").onchange = function() {
        submit();

        };

            appendMessage(BOT_NAME, NURSE_IMG, "left", "Please check the dataset you uploaded and it will give your some basic stats","View your dataset",{"View your dataset":"View your dataset"})
            alreaView = true
    }

}




function runModelExampleDateset(e){
    add_userMsg("Run Model with Example Dataset")
    appendMessage(BOT_NAME, NURSE_IMG, "left", "Do you want to use our default parameter set to train the example dataset","Train Model",{"Yes": "Yes","No,I don't":"No,I don't"})
}

function uploadNewData(e) {
    alreaView=false;
    add_userMsg("Open new dataset")
    document.getElementById('fileid').click();
    console.log(document.getElementById("fileid"))
    if (alreaView == false){
        document.getElementById("fileid").onchange = function() {
            submit();
        };

        //appendMessage(BOT_NAME, NURSE_IMG, "left", "Please check the dataset you uploaded and it will give your some basic stats","View your dataset",{"View your dataset":"View your dataset"})
    console.log(4)
    alreaView = true
    }}

function csvToArray(dataset, delimiter = ",") {
  // slice from start of text to the first \n index
  // use split to create an array from string by delimiter
    var headers = dataset.slice(0, dataset.indexOf("\n")).split("\t").join(",").split(delimiter)


  // slice from \n index + 1 to the end of the text
  // use split to create an array of each csv value row
  var rows = dataset.slice(dataset.indexOf("\n") + 1).split("\t").join(",").split("\n");

  // Map the rows
  // split values from each row into an array
  // use headers.reduce to create an object
  // object properties derived from headers:values
  // the object passed as an element of the array
  const arr = rows.map(function (row) {
    const values = row.split(delimiter);
    const el = headers.reduce(function (object, header, index) {
      object[header] = values[index];
      return object;
    }, {});
    return el;
  });

  // return the array
  return arr;
}


function wait(ms){
   var start = new Date().getTime();
   var end = start;
   while(end < start + ms) {
     end = new Date().getTime();
  }
}
function viewDataset(dataset,name,size){
    // var statisticalData = "Your dataset name is <b>"+ name +"</b> ; dataset size is <b>"+ size/1000 +"</b> kb; dataset format is<b> "+name.slice(-3)+"</b>"
    // appendMessage(BOT_NAME, NURSE_IMG, "left", statisticalData,"statistical data of dataset",[])
    console.log("breakpoint 153 ",dataset,name,size)
    var showTable = document.getElementById('showdataset');
    var hidden_div = document.getElementById("hidden_div")
    var hidden_table = document.getElementById("hidden_table")
    var tableHTML = '<thead class="thead-dark"><tr>'
    // if (name.slice(-3) == 'txt'){
    //     var array = csvToArray(dataset, delimiter = " ")
    //     var tablehead = Object.keys(array[0]);
    // }else{
        var array = csvToArray(dataset, delimiter = ",")
        var tablehead = Object.keys(array[0]);
        var targetValue = String((tablehead[tablehead.length-1]).replace(/(?:\r\n|\r|\n)/g,""))
        // if (targetValue != "distant_recurrence"){
        //     alert("The target feature of the table you uploaded is not distant_recurrence, please review the demo and submit it again")
        //     location.reload();
        //     return
        // }

    //}
    var statisticalData = "Your dataset name is <b>"+ name +"</b>; row number of dataset is <b>"+ array.length +"</b>; column number of dataset is <b>"+ tablehead.length +"</b>;dataset size is <b>"+ size/1000 +"</b> kb; dataset format is<b> "+name.slice(-3)+"</b>"
    appendMessage(BOT_NAME, NURSE_IMG, "left", statisticalData,"statistical data of dataset",[])

    if (array.length < 30){
        alert ("Your dataset size is less than 30, please resubmit it ")
        location.reload();
        return
    }

    for(var  i= 0; i< tablehead.length; i++) {
        tableHTML+= '<th>' + tablehead[i] + '</th>'
    }
    tableHTML += '</tr></thead>'

    for(var row = 0; row< array.length; row++) {
       tableHTML+= '<tbody><tr>'
        value_list = Object.values(array[row])
            for(var col= 0; col< value_list.length; col++) {
                tableHTML+= '<td>' + value_list[col] + '</td>'
            }
       tableHTML+= '</tr></tbody>'
    }
    hidden_table.innerHTML = tableHTML
    // document.getElementById("hidden_div").style.display='inline'
    // document.getElementById("hidden_table").style.display='inline'
    var myWindow = window.open("", "MsgWindow", "width=500, height=500");
    // $(newWindow).load(function(){
    //     $(newWindow.document).find('body').html($('#hidden_table').html());
    // });
    if (myWindow != null){

    console.log("200",myWindow)
    myWindow.document.write(css + '<html><head><title>Table</title></head><body>');
    myWindow.document.write('<table  class="table">')
    myWindow.document.write(tableHTML)
    myWindow.document.write('</table>')
    myWindow.document.write('</body></html>');
    showTable.style = "display:inline"
    // console.log(tableHTML)
    }
    appendMessage(BOT_NAME, NURSE_IMG, "left", "Do you want to use our default parameter set to train  your dataset","Train Model",{"Yes":"Yes","No":"No"})
    var openWindow=function(event,tableHTML){
        var myWindow = window.open("", "MsgWindow", "width=500, height=500");
        myWindow.document.write(css + '<html><head><title>Table</title></head><body>');
        myWindow.document.write('<table  class="table">')
        myWindow.document.write(event)
        myWindow.document.write('</table>')
        myWindow.document.write('</body></html>');

    }
    showTable.addEventListener('click',openWindow.bind(event,tableHTML),false)
 }
function submit() {
    //showdataset.style = "display:inline"
    console.log("enter submit")
    function read(callback) {

        var dataset = $('#fileid').prop('files')[0];


        const name = dataset.name
        window.dataset_name = dataset.name
        const size = dataset.size
        if (name.slice(-3) != 'txt' && name.slice(-3) != 'csv'){
            alert ("Your format is not 'txt' or 'csv', please upload allowed format!  ")
            location.reload();
            return
        }
        var reader = new FileReader();
        reader.onload = function() {
            rawLog = reader.result
            console.log("break point 235 ")
            var array = csvToArray(rawLog, delimiter = ",")
            var tablehead = Object.keys(array[0]);
            if ((train_model_year==5 && tablehead.length!=21)||(train_model_year==10 && tablehead.length!=19)||(train_model_year==15 && tablehead.lenght!=18))
                {
                    alert ("Your dataset size does not match the year you selected, please resubmit it ")
                    location.reload();
                    return
             }
            viewDataset(rawLog,name,size)
        }
        reader.readAsText(dataset);
    }
    var dataset = $('#fileid').prop('files')[0];
    if (dataset === undefined){
        alert("please upload your dataset first")
        // gobacktoBrowse()
    }else {
        read()
    }
}

function getParameterExam(){
        console.log("enter getpara exam")
    document.getElementById('textInput').disabled = true;
    document.getElementById('textInput').placeholder = "Your model is training!";
        const name = '15_year_smote_balancedataset - Copy.csv'
        var learningrate = $("#parameterForm input[name=learningrate]").val()
        var decay = $("#parameterForm input[name=decay]").val()
        var batchsize= $("#parameterForm input[name=batchsize]").val()
        var dropoutrate = $("#parameterForm input[name=dropoutrate]").val()
        var epochs = $("#parameterForm input[name=epochs]").val()
        $.post("/parameterExam", {
            datasetname: name,
            learningrate: learningrate,
            decay: decay,
            batchsize: batchsize,
            dropoutrate: dropoutrate,
            epochs: epochs
        }).done(function (data) {
            appendMessage(BOT_NAME, NURSE_IMG, "left", "Please wait, we are training your model ", "no information", [])
            appendMessage(BOT_NAME, NURSE_IMG, "left", "Your model validation auc is " + data, "no information", [])
            wait(20000);
            appendMessage(BOT_NAME, NURSE_IMG, "left", "This is your roc curve","no information",[])
            appendMessage(BOT_NAME, NURSE_IMG, "left", "Do you want to use your model to test your patients? ", "Test Patient", {"Testing with new patients":"Testing with new patients","End task":"End task","Retrain the model":"Retrain the model","Open new dataset":"Open new dataset"})
            document.getElementById('textInput').disabled = true;
            //document.getElementById('textInput').placeholder = "Enter your message..."
        })
    }
function getParameter(){
    document.getElementById('textInput').disabled = true;
    document.getElementById('textInput').placeholder = "Your model is training!";
    function read_parameter(callback) {

        var dataset = $('#fileid').prop('files')[0];
        var name = dataset.name
        var learningrate = $("#parameterForm input[name=learningrate]").val()
        var decay = $("#parameterForm input[name=decay]").val()
        var batchsize= $("#parameterForm input[name=batchsize]").val()
        var dropoutrate = $("#parameterForm input[name=dropoutrate]").val()
        var epochs = $("#parameterForm input[name=epochs]").val()
        var reader = new FileReader();
        reader.onload = function() {
            rawLog = reader.result
            $.post("/parameter", {
                dataset: rawLog,
                datasetname: name,
                learningrate: learningrate,
                decay: decay,
                batchsize: batchsize,
                dropoutrate: dropoutrate,
                epochs: epochs
            }).done(function (data) {
                appendMessage(BOT_NAME, NURSE_IMG, "left", "Please wait, we are training your model ", "no information", [])
                appendMessage(BOT_NAME, NURSE_IMG, "left", "Your model validation auc is " + data, "no information", [])
                wait(20000);
                appendMessage(BOT_NAME, NURSE_IMG, "left", "This is your roc curve","no information",[])
                appendMessage(BOT_NAME, NURSE_IMG, "left", "Do you want to use your model to test your patients? ", "Test Patient", {"Testing with new patients":"Testing with new patients","End task":"End task","Retrain the model":"Retrain the model","Open new dataset":"Open new dataset"})
                document.getElementById('textInput').disabled = true;
                //document.getElementById('textInput').placeholder = "Enter your message..."
            })
        }
    reader.readAsText(dataset);
    }
   read_parameter()
}
var myWindow = null
function showDemo() {

    //add_userMsg("Example dataset")
    if (train_model_year==5){
    demoHtml =
    '<thead class="thead-dark"><tr><th>race</th><th>smoking</th><th>family_history</th><th>age_at_diagnosis</th><th>TNEG</th><th>ER</th><th>ER_percent</th><th>PR</th><th>PR_percent</th><th>P53</th><th>HER2</th><th>t_tnm_stage</th><th>n_tnm_stage</th><th>stage</th><th>lymph_node_positive</th><th>Histology</th><th>size</th><th>invasive_tumor_Location</th><th>DCIS_level</th><th>surgical_margins</th><th>distant_recurrence</th></tr></thead>'+
    '<tr><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr>'+
    '<tr><td>0</td><td>0</td><td>1</td><td>1</td><td>0</td><td>0</td><td>0</td><td>1</td><td>0</td><td>0</td><td>0</td><td>1</td><td>1</td><td>1</td><td>1</td><td>0</td><td>1</td><td>0</td><td>1</td><td>0</td><td>0</td></tr>'+
    '<tr><td>0</td><td>0</td><td>2</td><td>2</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1</td><td>0</td><td>0</td><td>2</td><td>2</td><td>0</td><td>0</td><td>1</td><td>0</td><td>1</td><td>2</td><td>0</td><td>0</td></tr>'+
    '<tr><td>0</td><td>0</td><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1</td><td>2</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1</td><td>0</td><td>2</td><td>1</td><td>0</td><td>0</td></tr>'+
    '<tr><td>0</td><td>0</td><td>2</td><td>1</td><td>0</td><td>0</td><td>0</td><td>1</td><td>2</td><td>0</td><td>0</td><td>0</td><td>2</td><td>2</td><td>2</td><td>1</td><td>0</td><td>2</td><td>0</td><td>0</td><td>0</td></tr>'
    }
    if (train_model_year==10){
    demoHtml=
    '<thead class="thead-dark"><tr><th>lymph_node_positive</th><th>ER</th><th>PR_percent</th><th>smoking</th><th>ER_percent</th><th>family_history</th><th>alcohol_useage</th><th>Histology</th><th>age_at_diagnosis</th><th>DCIS_level</th><th>TNEG</th><th>surgical_margins</th><th>grade</th><th>stage</th><th>HER2</th><th>ethnicity</th><th>n_tnm_stage</th><th>PR</th><th>distant_recurrence</th></tr></thead>'+
    '<tr><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr>'+
    '<tr><td>1</td><td>0</td><td>1</td><td>0</td><td>0</td><td>1</td><td>0</td><td>1</td><td>1</td><td>1</td><td>0</td><td>0</td><td>0</td><td>1</td><td>0</td><td>0</td><td>1</td><td>1</td><td>0</td></tr>'+
    '<tr><td>1</td><td>0</td><td>1</td><td>0</td><td>0</td><td>2</td><td>0</td><td>1</td><td>0</td><td>2</td><td>0</td><td>0</td><td>1</td><td>1</td><td>0</td><td>0</td><td>2</td><td>1</td><td>0</td></tr>'+
    '<tr><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>2</td><td>1</td><td>0</td><td>0</td><td>2</td><td>1</td><td>0</td></tr>'+
    '<tr><td>0</td><td>0</td><td>2</td><td>1</td><td>0</td><td>0</td><td>2</td><td>1</td><td>1</td><td>3</td><td>0</td><td>1</td><td>1</td><td>2</td><td>1</td><td>0</td><td>1</td><td>1</td><td>0</td></tr>'
    }
    if (train_model_year==15){
    demoHtml=
    '<thead class="thead-dark"><tr><th>invasive_tumor_Location</th><th>ER</th><th>ER_percent</th><th>alcohol_useage</th><th>Histology</th><th>size</th><th>age_at_diagnosis</th><th>t_tnm_stage</th><th>lymph_node_status</th><th>menopause_status</th><th>surgical_margins</th><th>grade</th><th>stage</th><th>histology2</th><th>race</th><th>n_tnm_stage</th><th>re_excision</th><th>distant_recurrence</th></tr></thead>'+
    '<tr><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr>'+
    '<tr><td>1</td><td>0</td><td>0</td><td>1</td><td>1</td><td>0</td><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1</td><td>0</td><td>0</td><td>0</td><td>1</td><td>0</td><td>1</td></tr>'+
    '<tr><td>0</td><td>0</td><td>0</td><td>2</td><td>0</td><td>1</td><td>0</td><td>0</td><td>0</td><td>1</td><td>0</td><td>2</td><td>0</td><td>0</td><td>0</td><td>1</td><td>1</td><td>1</td></tr>'+
    '<tr><td>2</td><td>0</td><td>0</td><td>1</td><td>2</td><td>0</td><td>2</td><td>0</td><td>1</td><td>0</td><td>0</td><td>1</td><td>1</td><td>1</td><td>1</td><td>2</td><td>0</td><td>1</td></tr>'+
    '<tr><td>0</td><td>0</td><td>0</td><td>2</td><td>0</td><td>0</td><td>1</td><td>0</td><td>1</td><td>0</td><td>0</td><td>1</td><td>1</td><td>0</td><td>1</td><td>2</td><td>0</td><td>1</td></tr>'
    }
    requirements = '<h2>Instructions:</h2>'+
        '<ul className="list-group list-group-flush">'+
        '<li className="list-group-item">1.The size of dataset should be in 50kb-500kb</li>'+
        '<li className="list-group-item">2.The dataset must be in .csv or .txt format</li>'+
        '<li className="list-group-item">3.The label must be the first row of dataset</li>'+
        '<li className="list-group-item">4.Can only use categorical data for now</li>'+
        '<li className="list-group-item">5.The last column will be considered to the target</li>'+
    '</ul>'
    if ((myWindow == null) || (myWindow.closed)) {
        myWindow = window.open("", "MsgWindow", "width=500, height=500");

        myWindow.document.write(css + '<html><head><title>Table</title></head><body>');
        myWindow.document.write('<table class="table">')
        myWindow.document.write(requirements)
        myWindow.document.write(demoHtml)
        myWindow.document.write('</table>')

        myWindow.document.write('<button id = "runDemo" type="button" class="btn btn-info " >Run Demo!</button>')
        //myWindow.document.write('<span id = "Validation_AUC" className = "badge badge-primary" style="display:none"  ><br />The Validation_AUC of demo dataset is 0.841</span>')
        myWindow.document.write('<script>' +
            'document.getElementById("runDemo").addEventListener("click",()=>{ document.getElementById("Validation_AUC").style.display="inline"},false)' +
            '</script>');
        myWindow.document.write('</body></html>');
        myWindow.document.close();
    }else{
         Swal.fire("The example dataset is already open")
        }

    // var runDemo = myWindow.document.getElementById('runDemo')
    //
    // function trainDemoModel() {
    //     fetch('../../dataset/LSM-15Year.txt')
    //       .then(response => response.text())
    //       .then(text => console.log(text))
    //
    // }

    //runDemo.addEventListener('click',trainDemoModel,false)
}

function nottrainModel() {

    add_userMsg("End task")

    appendMessage(BOT_NAME, NURSE_IMG, "left",SURVEY,"no information",[])

    // more_que = "Do you have any other questions?"
    // appendMessage(BOT_NAME, NURSE_IMG, "left", more_que,"survey",{"I have no questions":"I have no questions","I have questions":"I have questions"})
    document.getElementById('textInput').disabled = true;
    console.log("end task")
    //document.getElementById('textInput').placeholder="Enter your message..."
}

function trainModel() {
    add_userMsg("YES")

    Swal.fire({
                  title: 'Default Parameter Settings',
                  text: " 'mstruct': [(50, 1)],\n" +
                      "        'drate': [0.2],\n" +
                      "        'kinit': ['glorot_normal'],\n" +
                      "        'iacti': ['relu'],\n" +
                      "        'hacti': ['relu'],\n" +
                      "        'oacti': ['sigmoid'],\n" +
                      "        'opti': ['Adagrad'],\n" +
                      "        'lrate': [0.01],\n" +
                      "        'momen': [0.4],\n" +
                      "        'dec': [0.0005],\n" +
                      "        'ls': ['binary_crossentropy'],\n" +
                      "        'batch_size': [40],\n" +
                      "        'epochs': [85],\n" +
                      "        'L1': [0.005],\n" +
                      "        'L2': [0.005],\n" +
                      "        'ltype': [3]",
                  icon: 'info',
                  showCancelButton: true,
                  confirmButtonColor: '#3085d6',
                  cancelButtonColor: '#d33',
                  cancelButtonText: 'No,I want to set it manually',
                  confirmButtonText: 'Yes, Go on!',
                  reverseButtons: true
                }).then((result) => {
                  if (result.isConfirmed) {
                      document.getElementById('textInput').disabled = true;
                      document.getElementById('textInput').placeholder = "Your model is training!";
                      var dataset = $('#fileid').prop('files')[0];
                      console.log("dataset",dataset);
                      if (dataset == null){
                          if (train_model_year == 5) {data_name='Book1.csv'}
                          else if (train_model_year == 10) {data_name='Book2.csv'}
                          else if (train_model_year == 15) {data_name='Book3.csv'};
                          console.log(data_name);
                          $.post("/Examdataset", {name: data_name}).done(function (data) {
                                    appendMessage(BOT_NAME, NURSE_IMG, "left", "Please wait, we are training your model ","no information",[])
                                    appendMessage(BOT_NAME, NURSE_IMG, "left", "Your model validation auc is "+ data,"no information",[])
                                    appendMessage(BOT_NAME, NURSE_IMG, "left", "This is your roc curve","no information",[])

                                    appendMessage(BOT_NAME, NURSE_IMG, "left", "Do you want to use your model to test your patients? ", "Test Patient", {"Testing with new patients":"Testing with new patients","End task":"End task","Retrain the model":"Retrain the model","Open new dataset":"Open new dataset"})
                                    document.getElementById('textInput').disabled = true;
                                    //document.getElementById('textInput').placeholder="Enter your message..."
                                })

                      }else{
                        function read(callback) {
                            var dataset = $('#fileid').prop('files')[0];
                            const name = dataset.name
                            console.log("upload dataset",name)
                            var reader = new FileReader();
                            reader.onload = function() {
                                rawLog = reader.result
                                $.post("/dataset", { dataset: rawLog, name: name}).done(function (data) {
                                    appendMessage(BOT_NAME, NURSE_IMG, "left", "Please wait, we are training your model ","no information",[])
                                    appendMessage(BOT_NAME, NURSE_IMG, "left", "Your model validation auc is "+ data,"no information",[])
                                    appendMessage(BOT_NAME, NURSE_IMG, "left", "This is your roc curve","no information",[])
                                    appendMessage(BOT_NAME, NURSE_IMG, "left", "Do you want to use your model to test your patients? ", "Test Patient", {"Testing with new patients":"Testing with new patients","End task":"End task","Retrain the model":"Retrain the model","Open new dataset":"Open new dataset"})
                                    document.getElementById('textInput').disabled = true;
                                    //document.getElementById('textInput').placeholder="Enter your message..."
                                })
                            }
                            reader.readAsText(dataset);
                        }read()}
                  }else{
                      trainModelWithParameter()
                  }
                }
                )}
function trainModelWithParameterExam() {
    add_userMsg("No, I don't")

    const question = "Please input the parameters you want to train the example dataset"
    appendMessage(BOT_NAME, NURSE_IMG, "left", question,"Train Model with Example dataset",[])
    document.getElementById('textInput').disabled = true;
    //document.getElementById('textInput').placeholder="Enter your message..."

}
function trainModelWithParameter() {
    add_userMsg("No")

    const question = "Please input the parameters you want"
    appendMessage(BOT_NAME, NURSE_IMG, "left", question,"Parameters",[])
    document.getElementById('textInput').disabled = true;
    //document.getElementById('textInput').placeholder="Enter your message..."

}
function retrainModelWithParameter() {
    add_userMsg("Retrain the model")
    const question = "Please input the parameters you want"
    appendMessage(BOT_NAME, NURSE_IMG, "left", question,"Parameters",[])
    document.getElementById('textInput').disabled = true;
    //document.getElementById('textInput').placeholder="Enter your message..."

}
function submitPatientForm(){
    console.log("submitPatientForm")
    document.getElementById('textInput').disabled = true;
    document.getElementById('textInput').placeholder = "We are evaluating your patient...";
    var patient_dic = []
    var patient_Form = document.getElementById("patientForm")
    var shap_check = document.getElementById("shapCheck").checked

    for (var i = 0; i < patient_Form.elements.length-1; i++) {
         console.log("patient form ",i," is ",patient_Form.elements[i])

        patient_dic.push({key:patient_Form.elements[i].id, value:patient_Form.elements[i].value})
    }
    console.log(patient_dic)
    if (window.dataset_name===undefined)
    {
        if (train_model_year==5){window.dataset_name="LSM-5Year-I-240.txt";}
        if (train_model_year==10){window.dataset_name="LSM-10Year-I-240.txt";}
        if (train_model_year==15){window.dataset_name="LSM-15Year-I-240.txt";}
    }
    console.log(window.dataset_name)

    $.post("/patientform", {patient_dic: JSON.stringify(patient_dic),dataset_name: JSON.stringify(window.dataset_name),shap_check: JSON.stringify(shap_check)}).done(function (data) {
        appendMessage(BOT_NAME, NURSE_IMG, "left", "Your distant_recurrence probability is " + data, "no information", [])
        if(shap_check == true){
        appendMessage(BOT_NAME, NURSE_IMG, "left", "This is your SHAP plot","no information",[])}

        appendMessage(BOT_NAME, NURSE_IMG, "left", "Do you want to use your model to test your patients? ", "Test Patient", {"Testing with new patients":"Testing with new patients","End task":"End task","Retrain the model":"Retrain the model","Open new dataset":"Open new dataset"})
        document.getElementById('textInput').disabled = true;
        //document.getElementById('textInput').placeholder = "Enter your message..."
    })

}
function generatePatientForm(labelList,table_result) {
    //console.log(labelList.toString())
    //console.log(table_result)
    var labelList_withouttarget = labelList
    console.log(labelList_withouttarget)
    labelList_withouttarget.pop()
    if (labelList_withouttarget.length == 0){
        labelList_withouttarget = (labelList.toString()).split("\t")
        labelList_withouttarget.pop()
    }
    //console.log(labelList_withouttarget)
    //console.log(table_result)
    var final_result = labelList_withouttarget.map((e, i) => e + "&"+table_result[i]);
    //console.log(final_result)
    let patientFormHtml = ""
          if (labelList.length != 0){
              document.getElementById('textInput').disabled = true;
              document.getElementById('textInput').placeholder = "You can not input now";
              patientFormHtml = final_result.map(function(item){
                  const label = item.split("&")[0]
                  const option_list = item.split("&")[1].split(',')
                //const element = `<div class="form-group row"><label for=${label} class="col-sm-2 col-form-label"><font size="-1">${label}</font></label><div class="col-sm-2"><input type="number" size="4" step="0.001" class="form-control" id=${label} name=${label} placeholder = "0"></div></div>`
                 const element = `<div id="label" class="form-group row">
                                    <a href="#" id="show-option" title=${patientParameter_dis[label]}>
                                       <i class="fas fa-info-circle" style="color:black"></i>
                                    </a>
                                       <label for=${label} class="col-sm-5 col-form-label"><font size="-1">${label}</font></label>
                                       <div class="col-sm-6">
                                      
                                                <select id=${label} class="form-control" required>
                                        <option selected value="1">1</option>`

                  const option_html = option_list.map(function(option){
                      const one_option =  `<option value=${option}>${option}</option>`

                      return one_option
                  })
                  //console.log(option_html)
                  return element + option_html.join("") +`</select></div> </div>`
              })
            let front = '<form id="patientForm" onsubmit="submitPatientForm();return false" method="post">\n'
            let end =' <div class="form-check">\n' +
                '    <input type="checkbox" class="form-check-input" id="shapCheck">\n' +
                '    <label class="form-check-label" for="shapCheck">Do you want to plot shap anlysis graph for this patient, it will take longer time according to your dataset size and model</label>\n' +
                '  </div> <div class="form-group row"><div class="col-sm-10"> <button type="submit" class="btn btn-primary">Submit</button></div></div></form>'
            patientFormHtml = front+patientFormHtml.join("")+end
          }else {
                patientFormHtml=" "
          }
          appendMessage(BOT_NAME, NURSE_IMG, "left", "Please fill the patient form below and click submit",patientFormHtml,[])
    }

function testPatient() {
    add_userMsg("Testing with new patients")
    $.get("/getTestPatient", { msg: train_model_year }).done(function (data) {
        generatePatientForm(data["labellist"], data["tableresult"])

    })
}



function add_userMsg(msgText) {

    appendMessage(PERSON_NAME, PERSON_IMG, "right", msgText,"no information",[]);
    const btn_group = document.getElementsByClassName("btn btn-success");
    for (let i = 0; i < btn_group.length; i++) {
    btn_group[i].className = "btn btn-success disabled"
    }
    // if(msgText == "View Example Dataset"){
    //     appendMessage(BOT_NAME, NURSE_IMG, "left", "Please review the demo dataset first and upload your local dataset, only .txt and .csv format are permitted","Upload Local Dataset",{"View Example Dataset":"View Example Dataset","Upload Local Dataset":"Upload Local Dataset"})
    // }

}


function noQuestion() {
    add_userMsg("I have no questions")
    appendMessage(BOT_NAME, NURSE_IMG, "left",SURVEY,"no information",[])
}

function train5year(){
            train_model_year=5;
            add_userMsg("5 year");
            appendMessage(BOT_NAME, NURSE_IMG, "left", "Please review the demo dataset first and upload your local dataset, only .txt and .csv format are permitted","Browse data",{"View Example Dataset":"View Example Dataset","Upload Local Dataset":"Upload Local Dataset","Run Model with Example Dataset":"Run Model with Example Dataset"});
}
function train10year(){
            train_model_year=10;
            add_userMsg("10 year");
            appendMessage(BOT_NAME, NURSE_IMG, "left", "Please review the demo dataset first and upload your local dataset, only .txt and .csv format are permitted","Browse data",{"View Example Dataset":"View Example Dataset","Upload Local Dataset":"Upload Local Dataset","Run Model with Example Dataset":"Run Model with Example Dataset"});
}
function train15year(){
            train_model_year=15;
            add_userMsg("15 year");
            appendMessage(BOT_NAME, NURSE_IMG, "left", "Please review the demo dataset first and upload your local dataset, only .txt and .csv format are permitted","Browse data",{"View Example Dataset":"View Example Dataset","Upload Local Dataset":"Upload Local Dataset","Run Model with Example Dataset":"Run Model with Example Dataset"});
}

function takesurvey(){
appendMessage(BOT_NAME, NURSE_IMG, "left",SURVEY,"no information",[]);
}

function takenosurvey(){

            location.reload();
            return
}

function haveQuestion() {
    add_userMsg("I have questions")
    appendMessage(BOT_NAME, NURSE_IMG, "left","Please tell me your questions, I will pass your question to our experts ","no information",[])
}

function appendMessage(name, img, side, text, instruction,btnGroup,tag="") {
    if (text == "") {

        return
    }

    var starHTML = ``
    var parameterHTML = ``
    var patientHtml = ``
    var rocHTML = ``
    if(text.includes("roc curve")){
        rocHTML = `<img className="fit-picture" src="static/img/roc/roc_curve.png" alt="ROC Curve" style="width:300px;height:250px;">`
    }
    if(text.includes("SHAP")){
        rocHTML = `<img className="fit-picture" src="static/img/shap/shap.png" alt="SHAP" style="width:300px;height:250px;">`
    }
    //Simple solution for small apps
    let buttonHtml = generateBtnGroup(btnGroup)
    original_text=text
    if (btnGroup != "") {
        if (text=="What is your " || text=="Could you tell me your " || text=="What is your tumor " || text=="Could you tell me your tumor ")
        {
            text = text +"<a href='#' id='show-option' title='"+instruction+"'>"+tag+"</a>"+ " (Please select one choice according to your situation)"
        }
        else{
        text = text + "(Please select one choice according to your situation)"
        }
    }
    if (text == SURVEY) {
        starHTML = '<div class="stars" id="stars"><form  onsubmit="getValue();" >\n' +
           ' <input class="star star-5" id="star-5" type="radio" name="star" value ="5" onsubmit="getValue();"/>\n' +
           ' <label class="star star-5" for="star-5"></label>\n' +
           ' <input class="star star-4" id="star-4" type="radio" name="star" value ="4" onsubmit="getValue();"/>\n' +
            '<label class="star star-4" for="star-4"></label>\n' +
            '<input class="star star-3" id="star-3" type="radio" name="star" value ="3" onsubmit="getValue();"/>\n' +
            '<label class="star star-3" for="star-3"></label>\n' +
            '<input class="star star-2" id="star-2" type="radio" name="star" value ="2" onsubmit="getValue();"/>\n' +
            '<label class="star star-2" for="star-2"></label>\n' +
            '<input class="star star-1" id="star-1" type="radio" name="star" value ="1" onsubmit="getValue();"/>\n' +
            '<label class="star star-1" for="star-1"></label>\n' +
            '<label for="exampleFormControlTextarea1">Please leave your suggestions for iMedBot</label>\n' +
            '<textarea class="form-control" id="usersuggestion" rows="5"></textarea>\n' +
            '<input type="submit" value="Submit" class ="btn btn-success">\n' +
        '</form>\n' +
        '</div>\n'
    }
    if (instruction == "Parameters") {
        parameterHTML = '<form id="parameterForm" onsubmit="getParameter();return false" method="post">\n' +
            '  <div class="form-group row">\n' +
            '    <label for="learningrate" class="col-sm-2 col-form-label"><font size="-1">Learning Rate</font></label>\n' +
            '    <div class="col-sm-10">\n' +
            '      <input type="number" min="0" step="0.001" class="form-control" id="learningrate" name="learningrate" placeholder=0.001 value=0.001>\n' +
            '    </div>\n' +
            '  </div>\n' +
            '  <div class="form-group row">\n' +
            '    <label for="batchsize" class="col-sm-2 col-form-label">Batch Size</label>\n' +
            '    <div class="col-sm-10">\n' +
            '      <input type="number" min="0" class="form-control" id="batchsize" name="batchsize" placeholder=10 value=10>\n' +
            '    </div>\n' +
            '  </div>\n' +
            '  <div class="form-group row">\n' +
            '    <label for="epoch" class="col-sm-2 col-form-label">Epoch</label>\n' +
            '    <div class="col-sm-10">\n' +
            '      <input type="number" min="0" class="form-control" id="epoch" name="epochs" placeholder=10 value=10>\n' +
            '    </div>\n' +
            '  </div>\n' +
            '  <div class="form-group row">\n' +
            '    <label for="decay" class="col-sm-2 col-form-label">Decay</label>\n' +
            '    <div class="col-sm-10">\n' +
            '      <input type="number" min="0" step="0.001" class="form-control" id="decay" name="decay" placeholder=0.001 value=0.001>\n' +
            '    </div>\n' +
            '  </div>\n' +
            '  <div class="form-group row">\n' +
            '    <label for="dropoutrate" class="col-sm-2 col-form-label">Dropout Rate</label>\n' +
            '    <div class="col-sm-10">\n' +
            '      <input type="number" min="0" step="0.001" class="form-control" id="dropoutrate" name="dropoutrate" placeholder=0.02 value=0.02>\n' +
            '    </div>\n' +
            '  </div>\n' +
            '  <div class="form-group row">\n' +
            '  <div class="col-sm-10"> <button type="submit" class="btn btn-primary">Submit</button>\n' +
            '</div>\n' +
            '</div>\n' +
            '</form>\n'
    }
    if(instruction == "Train Model with Example dataset" ||(instruction=="Parameters"&& $('#fileid').prop('files')[0]==null)) {
        parameterHTML = '<form id="parameterForm" onsubmit="getParameterExam();return false" method="post">\n' +
            '  <div class="form-group row">\n' +
            '    <label for="learningrate" class="col-sm-2 col-form-label"><font size="-1">Learning Rate</font></label>\n' +
            '    <div class="col-sm-10">\n' +
            '      <input type="number" min="0" step="0.001" class="form-control" id="learningrate" name="learningrate" placeholder=0.001 value=0.001>\n' +
            '    </div>\n' +
            '  </div>\n' +
            '  <div class="form-group row">\n' +
            '    <label for="batchsize" class="col-sm-2 col-form-label">Batch Size</label>\n' +
            '    <div class="col-sm-10">\n' +
            '      <input type="number" min="0" class="form-control" id="batchsize" name="batchsize" placeholder=10 value=10>\n' +
            '    </div>\n' +
            '  </div>\n' +
            '  <div class="form-group row">\n' +
            '    <label for="epoch" class="col-sm-2 col-form-label">Epoch</label>\n' +
            '    <div class="col-sm-10">\n' +
            '      <input type="number" min="0" class="form-control" id="epoch" name="epochs" placeholder=10 value=10>\n' +
            '    </div>\n' +
            '  </div>\n' +
            '  <div class="form-group row">\n' +
            '    <label for="decay" class="col-sm-2 col-form-label">Decay</label>\n' +
            '    <div class="col-sm-10">\n' +
            '      <input type="number" min="0" step="0.001" class="form-control" id="decay" name="decay" placeholder=0.001 value=0.001>\n' +
            '    </div>\n' +
            '  </div>\n' +
            '  <div class="form-group row">\n' +
            '    <label for="dropoutrate" class="col-sm-2 col-form-label">Dropout Rate</label>\n' +
            '    <div class="col-sm-10">\n' +
            '      <input type="number" min="0" step="0.001" class="form-control" id="dropoutrate" name="dropoutrate" placeholder=0.02 value=0.02>\n' +
            '    </div>\n' +
            '  </div>\n' +
            '  <div class="form-group row">\n' +
            '  <div class="col-sm-10"> <button type="submit" class="btn btn-primary">Submit</button>\n' +
            '</div>\n' +
            '</div>\n' +
            '</form>\n'
    }
    if (text == "Please fill the patient form below and click submit") {
        patientHtml = instruction
        instruction = "Patient Parameters"
    }
    if (instruction != "no information" && original_text!="What is your " && original_text!="Could you tell me your " && original_text!="What is your tumor " && original_text!="Could you tell me your tumor " )
    {

    var msgHTML =
        `<div class="msg ${side}-msg">
        <div class="msg-img" style="background-image: url(${img})"></div>
        <div class="msg-bubble">
            <div class="msg-info">
                <div class="msg-info-name">${name}</div>
                <div class="msg-info-time">
                <a href="#" id="show-option" title= "${instruction}"><i class="fas fa-info-circle" style="color:black"></i></a>
                ${formatDate(new Date())}

                </div>
            </div>
        <div class="msg-text">
            ${text}
        </div>` + rocHTML + buttonHtml + patientHtml + starHTML + parameterHTML + `</div> </div>`;
    } else
    {

    var msgHTML =
        `<div class="msg ${side}-msg">
        <div class="msg-img" style="background-image: url(${img})"></div>
        <div class="msg-bubble">
            <div class="msg-info">
                <div class="msg-info-name">${name}</div>
                <div class="msg-info-time">${formatDate(new Date())}
                </div>
            </div>
        <div class="msg-text">${text}</div>` + rocHTML + buttonHtml + patientHtml + starHTML + parameterHTML + `</div></div>`;

    }
    //'beforeend': Just inside the element, after its last child.
    msgerChat.insertAdjacentHTML("beforeend", msgHTML);
    msgerChat.scrollTop += 500;
    if (buttonHtml != " ") {
        const btn_group = document.getElementsByClassName("btn btn-success");

        for (let i = 0; i < btn_group.length; i++) {
            if (btn_group[i].innerHTML == "5 year" && instruction == "no information")
            {
            btn_group[i].addEventListener('click', train5year, false)
            }
            else if (btn_group[i].innerHTML == "10 year" && instruction == "no information")
            {
            btn_group[i].addEventListener('click', train10year, false)
            }
            else if (btn_group[i].innerHTML == "15 year" && instruction == "no information")
            {
            btn_group[i].addEventListener('click', train15year, false)
            }
            else if (btn_group[i].innerHTML == "Yes" && original_text == "Would you like to take a survey?")
            {
            console.log(text)
            btn_group[i].addEventListener('click', takesurvey, false)
            }
            else if (btn_group[i].innerHTML == "No" && original_text == "Would you like to take a survey?")
            {
            btn_group[i].addEventListener('click', takenosurvey, false)
            }
            else if (btn_group[i].innerHTML == "View Example Dataset") {
                btn_group[i].addEventListener('click', showDemo, false)

            }else if (btn_group[i].innerHTML == "Run Model with Example Dataset") {
                btn_group[i].addEventListener('click', runModelExampleDateset, false)
            }else if (btn_group[i].innerHTML == "Upload Local Dataset") {
                btn_group[i].addEventListener('click', uploadData, false)
            }else if (btn_group[i].innerHTML == "Open new dataset") {
                btn_group[i].addEventListener('click', uploadNewData, false)
            } else if (btn_group[i].innerHTML == "No,I don't") {
                btn_group[i].addEventListener('click', trainModelWithParameterExam, false)
            }else if (btn_group[i].innerHTML == "Yes") {
                btn_group[i].addEventListener('click', trainModel, false)
            } else if (btn_group[i].innerHTML == "No") {
                btn_group[i].addEventListener('click', trainModelWithParameter, false)
            } else if (btn_group[i].innerHTML == "Testing with new patients") {
                btn_group[i].addEventListener('click', testPatient, false)
            } else if (btn_group[i].innerHTML == "End task") {
                btn_group[i].addEventListener('click', nottrainModel, false)
            } else if (btn_group[i].innerHTML == "Retrain the model") {
                btn_group[i].addEventListener('click', retrainModelWithParameter, false)
            }
            else if (btn_group[i].innerHTML == "I have no questions") {
                btn_group[i].addEventListener('click', noQuestion, false)
            }
            else if (btn_group[i].innerHTML == "I have questions") {
                btn_group[i].addEventListener('click', haveQuestion, false)
            }
            else {
                    btn_group[i].addEventListener('click', showNext, false)
            }

        }
    }
}


function showNext(e){

    var instruction = ""
    var msgText = ""
    var btnGroup = []
    var nextques = ""
    var pattern = e.target.innerHTML
    if (e.target.innerHTML != "Predict" && e.target.innerHTML != "Train a Model"){
    add_userMsg(e.target.innerHTML)
    }


    if (pattern == "Predict"){
        input_choice = input_question["Predict"]
        PERSON_NAME="Your choice is"
    }else if(pattern == "Train a Model"){
        input_choice = input_question["Train a Model"]
        PERSON_NAME="Your choice is"
    }

    if (pattern == "Predict"){
        add_userMsg("Predict")
        appendMessage(BOT_NAME, NURSE_IMG, "left", "I can predict the recurrence probability of breast cancer, please tell me which year you want to predict","treatment_year instruction",{"5 year":"5 year","10 year":"10 year","15 year":"15 year"})
    }else if(pattern == "Train a Model"){
        add_userMsg("Train a Model")
                Swal.fire({
                  title: 'Model Method Description ',
                  text: " We will use 80% of your dataset to train this model with 5 fold cross validation strategies and 20% dataset as validation dataset to return the validation AUC, do you want to proceed it?",
                  icon: 'info',
                  showCancelButton: true,
                  confirmButtonColor: '#3085d6',
                  cancelButtonColor: '#d33',
                    cancelButtonText: 'No, cancel!',
                  confirmButtonText: 'Yes, Go on!'
                }).then((result) => {
                  if (result.isConfirmed) {
                      //appendMessage(BOT_NAME, NURSE_IMG, "left", "Please review the demo dataset first and upload your local dataset, only .txt and .csv format are permitted","Browse data",{"View Example Dataset":"View Example Dataset","Upload Local Dataset":"Upload Local Dataset","Run Model with Example Dataset":"Run Model with Example Dataset"})
                      appendMessage(BOT_NAME, NURSE_IMG, "left", "We can train the model for 5 year, 10 year and 15 year respectively. The dataset format is different from three choices","no information",{"5 year":"5 year","10 year":"10 year","15 year":"15 year"})
                  }else {
                      console.log("hello")
                        secMsg = "I can either predict breast cancer metastasis for your patient based on our deep learning models trained using one existing dataset,or I can train a model for you if you can provide your own dataset, so how do you want to proceed?Please enter 1 for the first choice, or 2 for the second choice"
                        appendMessage(BOT_NAME, NURSE_IMG, "left", secMsg,"no information", {"Predict":"Predict","Train a Model":"Train a Model"});
                      }
                })
        //alert("Do you really want to train the model?")

    }else {
        for (var i = 0; i < input_choice.length; i++) {
            if (Object.keys(input_choice[i].patterns).indexOf(pattern) != -1) {
                console.log(input_choice[i].patterns[pattern])
                if (input_choice[i].tag=="treatment_year")
                {
                    if (input_choice[i].patterns[pattern]=="10")
                    {
                        input_choice = input_question10["Predict"]
                    }
                    if (input_choice[i].patterns[pattern]=="5")
                    {
                        input_choice = input_question5["Predict"]
                    }
                }
                input.push(input_choice[i].patterns[pattern])
                nextques = input_choice[i].nextques
            }
        }
    }
    if(nextques == "none"){
        var input_cpoy = input
        input = []
        getinput(input_cpoy)
        appendMessage(BOT_NAME, NURSE_IMG, "left", "Thank you! you answered all questions, we are calculating recurrence","no information",btnGroup);
        return
    }
    tag=""
    for (var i = 0 ; i < input_choice.length; i++) {
        if (input_choice[i].tag == nextques){

            let index = Math.floor((Math.random()*input_choice[i].responses.length))
            msgText = input_choice[i].responses[index]
            btnGroup = Object.keys(input_choice[i].patterns)
            instruction = input_choice[i].instruction
            tag = input_choice[i].tag
        }
    }
    appendMessage(BOT_NAME, NURSE_IMG, "left", msgText, instruction, btnGroup,tag);
}

function getinput(input_copy){
  $.get("/getInput", { msg: input_copy.toString() }).done(function (data) {
    res = "Your risk of breast cancer recurrence is" +" "+data.substring(2,data.length-2)
      appendMessage(BOT_NAME, NURSE_IMG, "left", res,"no information",[])
      appendMessage(BOT_NAME, NURSE_IMG, "left","Would you like to take a survey?","no information",{"Yes":"Yes","No":"No"})
     // appendMessage(BOT_NAME, NURSE_IMG, "left",SURVEY,"no information",[])



    // appendMessage(BOT_NAME, NURSE_IMG, "left", "Do you have any other questions?","no information",{"I have no questions":"I have no questions","I have questions":"I have questions"})
    document.getElementById('textInput').disabled = true;
    //document.getElementById('textInput').placeholder="Enter your message..."

})
}

function generateBtnGroup(btn_group){
  let buttonHtml = ""
  let btn_array = Object.values(btn_group)
  // console.log( btn_array )
  if (btn_array.length != 0){
      document.getElementById('textInput').disabled = true;
      document.getElementById('textInput').placeholder = "You can not input now";
      buttonHtml = btn_array.map(function(btn){
        const element = `<button type="button" class="btn btn-success">${btn}</button>`
    return element
  })
    let front = '<div class="btn-group-vertical" role="group" aria-label="Basic example">'
    let end = '</div>'
    buttonHtml = front+buttonHtml.join("")+end
  }else {
        buttonHtml=" "
  }
  // console.log(buttonHtml)
  return buttonHtml
}

function botResponse(rawText) {
  // Bot Response
  $.get("/get", { msg: rawText }).done(function (data) {
    const msgText = data["response"];
    const btnGroup = data["button_group"]
    const instruction = data["instruction"]
    appendMessage(BOT_NAME, NURSE_IMG, "left", msgText,instruction,btnGroup);
  });
}

// Utils
function get(selector, root = document) {
    return root.querySelector(selector);
}

function formatDate(date) {
    const h = "0" + date.getHours();
    const m = "0" + date.getMinutes();
    return `${h.slice(-2)}:${m.slice(-2)}`;
}
function load(){

    firstMsg = "Hi, welcome to iMedBot! Go ahead and send me a message. 😄"
    secMsg = "I can either predict breast cancer metastasis for your patient based on our deep learning models trained using one existing dataset,or I can train a model for you if you can provide your own dataset, so how do you want to proceed?Please enter 1 for the first choice, or 2 for the second choice"
    btnGroup = []
    appendMessage(BOT_NAME, NURSE_IMG, "left", firstMsg,"no information", btnGroup);
    appendMessage(BOT_NAME, NURSE_IMG, "left", secMsg,"no information", {"Predict":"Predict","Train a Model":"Train a Model"});
}

window.οnlοad =load()
// window.οnlοad = appendMessage(BOT_NAME, NURSE_IMG, "left", firstMsg,"no information", btnGroup);
//window.οnlοad = appendMessage(BOT_NAME, NURSE_IMG, "left", secMsg,"Two choices", {"Predict":"1","Train a Model":"2"});




// ****************************************************************************
const start_button = document.getElementById("start_button");
const hint = document.getElementById("hint");
//start_button.onclick = startButton;
const start_img = document.getElementById("start_img");


var final_transcript = '';
var recognizing = false;
var if_error;
var start_timestamp;
// if (!('webkitSpeechRecognition' in window)) {
//   upgrade();
// } else {
//   start_button.style.display = 'inline-block';
//
//   var recognition = new webkitSpeechRecognition();
//   recognition.continuous = true;
//   recognition.interimResults = true;
//
//   recognition.onstart = function() {
//     recognizing = true;
//     // alert('info_speak_now');
//     start_img.src = 'static/img/mic-animate.gif';
//
//   };
//
//   recognition.onerror = function(event) {
//     if (event.error == 'no-speech') {
//       start_img.src = 'static/img/mic.gif';
//       alert('info_no_speech');
//       if_error = true;
//     }
//     if (event.error == 'audio-capture') {
//       start_img.src = 'static/img/mic.gif';
//       alert('info_no_microphone');
//       if_error = true;
//     }
//
//     }
//   };
//
//   recognition.onend = function() {
//     recognizing = false;
//     if (if_error) {
//       return;
//     }
//     start_img.src = 'static/img/mic.gif';
//     if (!final_transcript) {
//       return;
//     }
//   };
//
//   recognition.onresult = function(event) {
//     var interim_transcript = '';
//     for (var i = event.resultIndex; i < event.results.length; ++i) {
//       if (event.results[i].isFinal) {
//         final_transcript += event.results[i][0].transcript;
//       } else {
//         interim_transcript += event.results[i][0].transcript;
//       }
//     }
//     final_transcript = capitalize(final_transcript);
//     msgerInput.value =linebreak(final_transcript);
//
//   };


// function upgrade() {
//   start_button.style.visibility = 'hidden';
//   alert('info_upgrade');
// }
//
// var two_line = /\n\n/g;
// var one_line = /\n/g;
// function linebreak(s) {
//   return s.replace(two_line, '<p></p>').replace(one_line, '<br>');
// }
//
// var first_char = /\S/;
// function capitalize(s) {
//   return s.replace(first_char, function(m) { return m.toUpperCase(); });
// }
//
//
// function startButton(event) {
//   start_button.title = '&nbsp&nbsp Stop recording when you click'
//   hint.innerHTML = '&nbsp&nbsp Stop recording when you click microphone'
//   hint.style.color = "red"
//   if (recognizing) {
//
//     recognition.stop();
//     start_button.title = '&nbsp&nbsp Start recording when you click'
//     hint.innerHTML = '&nbsp&nbsp Start recording when you click microphone'
//     hint.style.color = "green"
//     return;
//   }
//
//   final_transcript = '';
//   recognition.lang = 'en-US';
//   recognition.start();
//
//   if_error = false;
//   start_img.src = 'static/img/mic-slash.gif';
//   start_timestamp = event.timeStamp;
// }

// ===========================================================================

function autocomplete(inp, arr) {
  /*the autocomplete function takes two arguments,
  the text field element and an array of possible autocompleted values:*/
  var currentFocus;
  /*execute a function when someone writes in the text field:*/
  inp.addEventListener("input", function(e) {
      var a, b, i, val = this.value;
      /*close any already open lists of autocompleted values*/
      closeAllLists();
      if (!val) { return false;}
      currentFocus = -1;
      /*create a DIV element that will contain the items (values):*/
      a = document.createElement("DIV");
      a.setAttribute("id", this.id + "autocomplete-list");
      a.setAttribute("class", "autocomplete-items");
      /*append the DIV element as a child of the autocomplete container:*/
      this.parentNode.appendChild(a);
      /*for each item in the array...*/
      for (i = 0; i < arr.length; i++) {
        /*check if the item starts with the same letters as the text field value:*/
        if (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
          /*create a DIV element for each matching element:*/
          b = document.createElement("DIV");
          /*make the matching letters bold:*/
          b.innerHTML = "<strong>" + arr[i].substr(0, val.length) + "</strong>";
          b.innerHTML += arr[i].substr(val.length);
          /*insert a input field that will hold the current array item's value:*/
          b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
          /*execute a function when someone clicks on the item value (DIV element):*/
          b.addEventListener("click", function(e) {
              /*insert the value for the autocomplete text field:*/
              inp.value = this.getElementsByTagName("input")[0].value;
              /*close the list of autocompleted values,
              (or any other open lists of autocompleted values:*/
              closeAllLists();
          });
          a.appendChild(b);
        }
      }
  });
  /*execute a function presses a key on the keyboard:*/
  // inp.addEventListener("keydown", function(e) {
  //     var x = document.getElementById(this.id + "autocomplete-list");
  //     if (x) x = x.getElementsByTagName("div");
  //     if (e.keyCode == 40) {
  //       /*If the arrow DOWN key is pressed,
  //       increase the currentFocus variable:*/
  //       currentFocus++;
  //       /*and and make the current item more visible:*/
  //       addActive(x);
  //     } else if (e.keyCode == 38) { //up
  //       /*If the arrow UP key is pressed,
  //       decrease the currentFocus variable:*/
  //       currentFocus--;
  //       /*and and make the current item more visible:*/
  //       addActive(x);
  //     } else if (e.keyCode == 13) {
  //       /*If the ENTER key is pressed, prevent the form from being submitted,*/
  //       e.preventDefault();
  //       if (currentFocus > -1) {
  //         /*and simulate a click on the "active" item:*/
  //         if (x) x[currentFocus].click();
  //       }
  //     }
  // });
  function addActive(x) {
    /*a function to classify an item as "active":*/
    if (!x) return false;
    /*start by removing the "active" class on all items:*/
    removeActive(x);
    if (currentFocus >= x.length) currentFocus = 0;
    if (currentFocus < 0) currentFocus = (x.length - 1);
    /*add class "autocomplete-active":*/
    x[currentFocus].classList.add("autocomplete-active");
  }
  function removeActive(x) {
    /*a function to remove the "active" class from all autocomplete items:*/
    for (var i = 0; i < x.length; i++) {
      x[i].classList.remove("autocomplete-active");
    }
  }
  function closeAllLists(elmnt) {
    /*close all autocomplete lists in the document,
    except the one passed as an argument:*/
    var x = document.getElementsByClassName("autocomplete-items");
    for (var i = 0; i < x.length; i++) {
      if (elmnt != x[i] && elmnt != inp) {
        x[i].parentNode.removeChild(x[i]);
      }
    }
  }
  /*execute a function when someone clicks in the document:*/
  document.addEventListener("click", function (e) {
      closeAllLists(e.target);
  });
}

/*An array containing all the country names in the world:*/
var possiblequestions = [ "Hello", "What can you do?",
                  "What is a breast cancer?",
                  "Could you help me predict my breast cancer recurrence probability?",
                  "Could you tell me your name?",
                  "I want to know my risk of metastatic cancer",
                  "No, I do not have other questions",
                  "I do not have other questions",
                  "Yes, I have some other problems",
                  "Thank you"


];



autocomplete(document.getElementById("textInput"), possiblequestions);


//
// <!--                                                <datalist id="itemlist">-->
//  <!-- <input type="number" required="required" id=${label} name=${label} value=0 placeholder = "0">-->
// <!--                                                    <option>0</option><option>1</option><option>2</option>-->
// <!--                                                </datalist>-->