// Icons made by Freepik from www.flaticon.com
const BOT_IMG = "static/img/robot.svg";
const NURSE_IMG = "static/img/nurse.svg"
const PERSON_IMG = "static/img/woman.svg";
const BOT_NAME = "iMedBot";
const PERSON_NAME = "You";
var input_question = JSON.parse(input_question)
var input = []
// get the element for html

const msgerForm = get(".msger-inputarea");
const msgerInput = get(".msger-input");
const msgerChat = get(".msger-chat");




msgerForm.addEventListener("submit", event => {
  event.preventDefault();
  const msgText = msgerInput.value;
  if (!msgText) return;
  appendMessage(PERSON_NAME, PERSON_IMG, "right", msgText,[]);
  msgerInput.value = "";
  botResponse(msgText);
});

// function readTextFile(file, callback) {
//     var cb_json
//     var rawFile = new XMLHttpRequest();
//     rawFile.overrideMimeType("application/json");
//     rawFile.open("GET", file, true);
//     rawFile.onreadystatechange = function() {
//         if (rawFile.readyState === 4 && rawFile.status == "200") {
//             cb_json = callback(rawFile.responseText);
//         }
//     }
//     rawFile.send(null);
//     return cb_json
// }
//
// //usage:
// const cb_json = readTextFile("static/assets/classes_button.json", function(text){
//     var cb_json = JSON.parse(text);
//     return cb_json
// });
//
// console.log(cb_json)


// function GetButtonjson() {
//   var cb_json
//   const url = "static/assets/classes_button.json";/*json文件url，本地的就写本地的位置，如果是服务器的就写服务器的路径*/
//   const request = new XMLHttpRequest();
//   request.open("get", url);/*设置请求方法与路径*/
//   request.send(null);/*不发送数据到服务器*/
//   request.onload = function () {/*XHR对象获取到返回信息后执行*/
//     if (request.status == 200) {/*返回状态为200，即为数据获取成功*/
//       cb_json = JSON.parse(request.responseText);
//       happy(cb_json)
//     }
//   }
//
// }
// const class_button_json = GetButtonjson()
// var cd_Json
// function happy(cd_json){
//   //console.log(cd_json)
//   cd_Json =  cd_json
// }
// console.log(cd_Json)



/**
 * @param {string} name if it is robot or user
 * @param {string} img the robot img or user img
 * @param {string} side location of dialogue right or left
 * @param {string} text the value of input
 */


function appendMessage(name, img, side, text, btnGroup) {
  //Simple solution for small apps
    let buttonHtml = generateBtnGroup(btnGroup)
    console.log(buttonHtml)

    const msgHTML =
        ` <div class="msg ${side}-msg">
          <div class="msg-img" style="background-image: url(${img})"></div>
          <div class="msg-bubble">
            <div class="msg-info">
              <div class="msg-info-name">${name}</div>
              <div class="msg-info-time">${formatDate(new Date())}</div>
            </div>
            <div class="msg-text">${text}</div>`+ buttonHtml+ `</div></div>`;

  //'beforeend': Just inside the element, after its last child.
  msgerChat.insertAdjacentHTML("beforeend", msgHTML);
  msgerChat.scrollTop += 500;
  if(buttonHtml != " "){
    const btn_group = document.getElementsByClassName("btn btn-success");
    console.log(btn_group)
    for (var i = 0 ; i < btn_group.length; i++) {
       btn_group[i].addEventListener('click',showNext,false)
    }
  }
}
function showNext(e){
  var msgText = " "
  var btnGroup = []
  var nextques = ""
  var pattern = e.target.innerHTML
  console.log(pattern)
  input.push(pattern)
  console.log(input_question.length)
  for (var i = 0 ; i < input_question.length; i++) {
      console.log(input_question[i].patterns)
    if(input_question[i].patterns.indexOf(pattern) != -1){
      nextques = input_question[i].nextques
      console.log(nextques)
       }
  }
  if(nextques == "none"){
    var input_cpoy = input
    input = []
    getinput(input_cpoy)
    appendMessage(BOT_NAME, NURSE_IMG, "left", "Thank you! you answered all questions, we are calculating recurrence",btnGroup);
    return
  }
  for (var i = 0 ; i < input_question.length; i++) {
    if (input_question[i].tag == nextques) {
      let index = Math.floor((Math.random()*input_question[i].responses.length))
      msgText = input_question[i].responses[index]
      btnGroup = input_question[i].patterns
      console.log("hello")
      console.log(msgText)
      console.log(btnGroup)
    }
  }
  appendMessage(BOT_NAME, NURSE_IMG, "left", msgText,btnGroup);

}

function getinput(input_copy){
  $.get("/getInput", { msg: input_copy.toString() }).done(function (data) {
  console.log(data)
})
}




function generateBtnGroup(btn_group){
  let buttonHtml = ""
  let btn_array = Object.values(btn_group)
  // console.log( btn_array )
  if (btn_array.length != 0){
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
function RecordInformation(){
  alert("hello")
}


function botResponse(rawText) {
  // Bot Response
  $.get("/get", { msg: rawText }).done(function (data) {
    console.log(rawText);
    console.log(data);
    const msgText = data["response"];
    const btnGroup = data["button_group"]
    appendMessage(BOT_NAME, NURSE_IMG, "left", msgText,btnGroup);
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
window.οnlοad = appendMessage(BOT_NAME, NURSE_IMG, "left", firstMsg, btnGroup);



// ****************************************************************************
const start_button = document.getElementById("start_button");
start_button.onclick = startButton;
const start_img = document.getElementById("start_img");


var final_transcript = '';
var recognizing = false;
var ignore_onend;
var start_timestamp;
if (!('webkitSpeechRecognition' in window)) {
  upgrade();
} else {
  start_button.style.display = 'inline-block';
  var recognition = new webkitSpeechRecognition();
  recognition.continuous = true;
  recognition.interimResults = true;

  recognition.onstart = function() {
    recognizing = true;
    // alert('info_speak_now');
    start_img.src = 'static/img/mic-animate.gif';
  };

  recognition.onerror = function(event) {
    if (event.error == 'no-speech') {
      start_img.src = 'static/img/mic.gif';
      alert('info_no_speech');
      ignore_onend = true;
    }
    if (event.error == 'audio-capture') {
      start_img.src = 'static/img/mic.gif';
      alert('info_no_microphone');
      ignore_onend = true;
    }
    if (event.error == 'not-allowed') {
      if (event.timeStamp - start_timestamp < 100) {
        alert('info_blocked');
      } else {
        alert('info_denied');
      }
      ignore_onend = true;
    }
  };

  recognition.onend = function() {
    recognizing = false;
    if (ignore_onend) {
      return;
    }
    start_img.src = 'static/img/mic.gif';
    if (!final_transcript) {
      // alert('info_start');
      return;
    }
  };

  recognition.onresult = function(event) {
    var interim_transcript = '';
    for (var i = event.resultIndex; i < event.results.length; ++i) {
      if (event.results[i].isFinal) {
        final_transcript += event.results[i][0].transcript;
      } else {
        interim_transcript += event.results[i][0].transcript;
      }
    }
    final_transcript = capitalize(final_transcript);
    msgerInput.value =linebreak(final_transcript);

  };
}

function upgrade() {
  start_button.style.visibility = 'hidden';
  alert('info_upgrade');
}

var two_line = /\n\n/g;
var one_line = /\n/g;
function linebreak(s) {
  return s.replace(two_line, '<p></p>').replace(one_line, '<br>');
}

var first_char = /\S/;
function capitalize(s) {
  return s.replace(first_char, function(m) { return m.toUpperCase(); });
}


function startButton(event) {
  if (recognizing) {
    recognition.stop();
    return;
  }
  final_transcript = '';
  recognition.lang = 'en-US';
  recognition.start();
  ignore_onend = false;
  start_img.src = 'static/img/mic-slash.gif';
  start_timestamp = event.timeStamp;
}

// ===========================================================================







