const BOT_IMG = "static/img/robot.svg";
const NURSE_IMG = "static/img/nurse.svg"
const PERSON_IMG = "static/img/woman.svg";
const BOT_NAME = "iMedBot";
const PERSON_NAME = "You";
var input_question = JSON.parse(input_question)
var input = []
const SURVEY = "BYE, It is my pleasure to help you,Have a nice day!How many stars you can give us?"
// get the element for html
// Icons made by Freepik from www.flaticon.com
const msgerForm = get(".msger-inputarea");
const msgerInput = get(".msger-input");
const msgerChat = get(".msger-chat");
const css ='<link rel="stylesheet" href="http://cdn.bootcss.com/bootstrap/3.3.0/css/bootstrap.min.css">\n' +
    '    <script src="http://cdn.bootcss.com/jquery/1.11.1/jquery.min.js"></script>\n' +
    '    <script src="http://cdn.bootcss.com/bootstrap/3.3.0/js/bootstrap.min.js"></script>'

$body = $("body");

$(document).on({
    ajaxStart: function() { $body.addClass("loading");    },
     ajaxStop: function() { $body.removeClass("loading"); }
});



msgerForm.addEventListener("submit", event => {
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
    var radio = document.getElementById("stars");
    // console.log(radio.length())
    for (i=0; i<radio.length(); i++) {
        if (radio[i].checked==true) {
            alert(radio[i].id)
        }
    }
}

function uploadData(e) {
    document.getElementById('fileid').click();
    appendMessage(BOT_NAME, NURSE_IMG, "left", "Please check the dataset you uploaded and it will give your some basic stats","View your dataset",{"View your dataset":"View your dataset"})
}

function csvToArray(str, delimiter = ",") {
  // slice from start of text to the first \n index
  // use split to create an array from string by delimiter
  const headers = str.slice(0, str.indexOf("\n")).split(delimiter);

  // slice from \n index + 1 to the end of the text
  // use split to create an array of each csv value row
  const rows = str.slice(str.indexOf("\n") + 1).split("\n");

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
// function openWindow(e) {
//     console.log('CHUHAN')
//     alert("happy")
// }


function viewDataset(dataset,name){
    var showTable = document.getElementById('showdataset');
    var hidden_div = document.getElementById("hidden_div")
    var hidden_table = document.getElementById("hidden_table")
    var tableHTML = '<thead class="thead-dark"><tr>'
    if (name.slice(-3) == 'txt'){
        var array = csvToArray(dataset, delimiter = " ")
        var tablehead = Object.keys(array[0]);
    }else{
        var array = csvToArray(dataset, delimiter = ",")
        var tablehead = Object.keys(array[0]);
        var targetValue = String((tablehead[tablehead.length-1]).replace(/(?:\r\n|\r|\n)/g,""))
        if (targetValue != "distant_recurrence"){
            alert("The target feature of the table you uploaded is not distant_recurrence, please review the demo and submit it again")
            location.reload();
            return
        }

    }

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
    myWindow.document.write(css + '<html><head><title>Table</title></head><body>');
    myWindow.document.write('<table  class="table">')
    myWindow.document.write(tableHTML)
    myWindow.document.write('</table>')
    myWindow.document.write('</body></html>');
    showTable.style = "display:inline"
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
    function read(callback) {
        var dataset = $('#fileid').prop('files')[0];
        const name = dataset.name
        if (name.slice(-3) != 'txt' && name.slice(-3) != 'csv'){
            alert ("Your format is not 'txt' or 'csv', please upload allowed format!  ")
            location.reload();
            return
        }
        var reader = new FileReader();
        reader.onload = function() {
            rawLog = reader.result
            viewDataset(rawLog,name)
        }
        reader.readAsText(dataset);
    }
    read()
}

function showDemo() {
    demoHtml = '<thead class="thead-dark"><tr><th></th><th>race</th><th>ethnicity</th><th>smoking</th><th>alcohol_useage</th><th>family_history</th><th>age_at_diagnosis</th><th>menopause_status</th><th>side</th><th>TNEG</th><th>ER</th><th>ER_percent</th><th>PR</th><th>PR_percent</th><th>P53</th><th>HER2</th><th>t_tnm_stage</th><th>n_tnm_stage</th><th>stage</th><th>lymph_node_removed</th><th>lymph_node_positive</th><th>lymph_node_status</th><th>Histology</th><th>size</th><th>grade</th><th>invasive</th><th>histology2</th><th>invasive_tumor_Location</th><th>DCIS_level</th><th>re_excision</th><th>surgical_margins</th><th>MRIs_60_surgery</th><th>distant_recurrence\n' +
        '</th></tr></thead><tbody><tr><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0\n' +
        '</td></tr></tbody><tbody><tr><td>1</td><td>0</td><td>0</td><td>0</td><td>1</td><td>0</td><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1</td><td>0</td><td>0</td><td>0</td><td>1</td><td>0</td><td>1</td><td>0</td><td>0</td><td>1</td><td>0</td><td>1</td><td>0</td><td>0</td><td>1</td><td>1</td><td>0</td><td>0</td><td>0</td><td>1\n' +
        '</td></tr></tbody><tbody><tr><td>2</td><td>0</td><td>0</td><td>0</td><td>2</td><td>1</td><td>0</td><td>1</td><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1</td><td>0</td><td>0</td><td>0</td><td>1</td><td>0</td><td>1</td><td>0</td><td>0</td><td>0</td><td>1</td><td>2</td><td>0</td><td>0</td><td>0</td><td>2</td><td>1</td><td>0</td><td>0</td><td>1\n' +
        '</td></tr>'
    var myWindow = window.open("", "MsgWindow", "width=500, height=500");

    myWindow.document.write(css + '<html><head><title>Table</title></head><body>');
    myWindow.document.write('<table class="table">')
    myWindow.document.write(demoHtml)
    myWindow.document.write('</table>')
    myWindow.document.write('</body></html>');

}

function nottrainModel() {
    more_que = "Do you have any other questions?"
    appendMessage(BOT_NAME, NURSE_IMG, "left", more_que,"no information",[])
    document.getElementById('textInput').disabled = false;
    document.getElementById('textInput').placeholder="Enter your message..."
}

function trainModel() {
    document.getElementById('textInput').disabled = true;
    document.getElementById('textInput').placeholder = "Your model is training!";
    function read(callback) {
        var dataset = $('#fileid').prop('files')[0];
        const name = dataset.name
        var reader = new FileReader();
        reader.onload = function() {
            rawLog = reader.result
            $.post("/dataset", { dataset: rawLog, name: name}).done(function (data) {
                appendMessage(BOT_NAME, NURSE_IMG, "left", "Please wait, we are training your model ","no information",[])
                appendMessage(BOT_NAME, NURSE_IMG, "left", "Your model validation auc is "+ data,"no information",[])
                document.getElementById('textInput').disabled = false;
                document.getElementById('textInput').placeholder="Enter your message..."
            })
        }
        reader.readAsText(dataset);

    }
    read()


}

function appendMessage(name, img, side, text, instruction,btnGroup){
    if (text == ""){
        return
    }
    var starHTML =``
    //Simple solution for small apps
    let buttonHtml = generateBtnGroup(btnGroup)
    if (btnGroup!=""){
        text = text + "(Please click the button)"
    }
    if (text == SURVEY){
       starHTML =`<div class="stars" id="stars"><form  onsubmit="getValue();return false">
            <input class="star star-5" id="star-5" type="radio" name="star" value ="5"/>
            <label class="star star-5" for="star-5"></label>
            <input class="star star-4" id="star-4" type="radio" name="star" value ="4"/>
            <label class="star star-4" for="star-4"></label>
            <input class="star star-3" id="star-3" type="radio" name="star" value ="3"/>
            <label class="star star-3" for="star-3"></label>
            <input class="star star-2" id="star-2" type="radio" name="star" value ="2"/>
            <label class="star star-2" for="star-2"></label>
            <input class="star star-1" id="star-1" type="radio" name="star" value ="1"/>
            <label class="star star-1" for="star-1"></label>
            <input type="submit" value="Submit" class ="msger-send-btn">
        </form>
        </div>`
    }
    var msgHTML =
    `<div class="msg ${side}-msg">
        <div class="msg-img" style="background-image: url(${img})"></div>
        <div class="msg-bubble">
            <div class="msg-info">
                <div class="msg-info-name">${name}</div>
                <div class="msg-info-time">${formatDate(new Date())}
                    <a href="#" id="show-option" title="${instruction}"><i class="fas fa-info-circle" style="color:black"></i></a>
                </div>
            </div>
        <div class="msg-text">${text}</div>` + buttonHtml + starHTML+`</div></div>`;
    //'beforeend': Just inside the element, after its last child.
    msgerChat.insertAdjacentHTML("beforeend", msgHTML);
    msgerChat.scrollTop += 500;
    if(buttonHtml != " "){
        const btn_group = document.getElementsByClassName("btn btn-success");
         if (instruction == "View your dataset") {
             btn_group[4].addEventListener('click', submit, false)
         }
        else if (instruction == "Browse data"){
            btn_group[2].addEventListener('click',showDemo,false)
            btn_group[3].addEventListener('click',uploadData,false)
            // btn_group[5].addEventListener('click',submit,false)
        }
        else if ( instruction == "Train Model"){
            btn_group[5].addEventListener('click',trainModel,false)
            btn_group[6].addEventListener('click',nottrainModel,false)
            // btn_group[5].addEventListener('click',submit,false)
        }
        else{
            for (var i = 0 ; i < btn_group.length; i++) {
               btn_group[i].addEventListener('click',showNext,false)
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
    if (pattern == "Choice 1"){
        input_choice = input_question["Choice 1"]
    }else if(pattern == "Choice 2"){
        input_choice = input_question["Choice 2"]
    }
    if (pattern == "Choice 1"){
        appendMessage(BOT_NAME, NURSE_IMG, "left", "I can predict the recurrence probability of breast cancer, please tell me which year you want to predict","treatment_year instruction",{"5 year":"5 year","10 year":"10 year","15 year":"15 year"})
    }else if(pattern == "Choice 2"){
        appendMessage(BOT_NAME, NURSE_IMG, "left", "Please review the demo dataset first and upload your local dataset, only .txt and .csv format are permitted","Browse data",{"Demo":"Demo","Browse Local":"Browse Local"})
    }else {
        for (var i = 0; i < input_choice.length; i++) {
            if (Object.keys(input_choice[i].patterns).indexOf(pattern) != -1) {
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
    for (var i = 0 ; i < input_choice.length; i++) {
        if (input_choice[i].tag == nextques){
            let index = Math.floor((Math.random()*input_choice[i].responses.length))
            msgText = input_choice[i].responses[index]
            btnGroup = Object.keys(input_choice[i].patterns)
            instruction = Object.keys(input_choice[i].instruction)
        }
    }
    appendMessage(BOT_NAME, NURSE_IMG, "left", msgText, instruction, btnGroup);
}

function getinput(input_copy){
  $.get("/getInput", { msg: input_copy.toString() }).done(function (data) {
    res = "Your risk of breast cancer recurrence is" +" "+data.substring(2,data.length-2)
    more_que = "Do you have any other questions?"
    appendMessage(BOT_NAME, NURSE_IMG, "left", res,"no information",[])
    appendMessage(BOT_NAME, NURSE_IMG, "left", more_que,"no information",[])
    document.getElementById('textInput').disabled = false;
    document.getElementById('textInput').placeholder="Enter your message..."

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
    let front = '<div class="btn-group" role="group" aria-label="Basic example">'
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
firstMsg = "Hi, welcome to iMedBot! Go ahead and send me a message. 😄"
btnGroup = []
window.οnlοad = appendMessage(BOT_NAME, NURSE_IMG, "left", firstMsg,"no information", btnGroup);



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
  console.log("hello")
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



