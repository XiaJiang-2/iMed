
// Icons made by Freepik from www.flaticon.com
const BOT_IMG = "static/img/robot.svg";
const NURSE_IMG = "static/img/nurse.svg"
const PERSON_IMG = "static/img/woman.svg";
const BOT_NAME = "iMedBot";
const PERSON_NAME = "You";

// get the element for html

const msgerForm = get(".msger-inputarea");
const msgerInput = get(".msger-input");
const msgerChat = get(".msger-chat");


msgerForm.addEventListener("submit", event => {
  event.preventDefault();
  const msgText = msgerInput.value;
  if (!msgText) return;
  appendMessage(PERSON_NAME, PERSON_IMG, "right", msgText);
  msgerInput.value = "";
  botResponse(msgText);
});

/**
 * @param {string} name if it is robot or user
 * @param {string} img the robot img or user img
 * @param {string} side location of dialogue right or left
 * @param {string} text the value of input
 */
function appendMessage(name, img, side, text) {
  //Simple solution for small apps
  const msgHTML = `
        <div class="msg ${side}-msg">
          <div class="msg-img" style="background-image: url(${img})"></div>
          <div class="msg-bubble">
            <div class="msg-info">
              <div class="msg-info-name">${name}</div>
              <div class="msg-info-time">${formatDate(new Date())}</div>
            </div>
            <div class="msg-text">${text}</div>
          </div>
        </div>`;
  //'beforeend': Just inside the element, after its last child.
  msgerChat.insertAdjacentHTML("beforeend", msgHTML);
  msgerChat.scrollTop += 500;
}


function botResponse(rawText) {
  // Bot Response
  $.get("/get", { msg: rawText }).done(function (data) {
    console.log(rawText);
    console.log(data);
    const msgText = data;
    appendMessage(BOT_NAME, NURSE_IMG, "left", msgText);
  });
}

// Utils
function get(selector, root = document) {
  return root.querySelector(selector);
}



// function transfervoice(){
//   const start_img = document.getElementById("start_img");
//   var recognition = new webkitSpeechRecognition();
//   if (recognizing) {
//     console.log("recog")
//     recognition.stop();
//   }
//   var recognizing = false;
//   var ignore_onend = false;
//   var lang = 'en-US'
//   var final_transcript = '';
//
//   recognition.lang = lang;
//   recognition.continuous = true;//if allowed continue listen
//   recognition.interimResults = true;
//   recognition.start();
//
//   recognition.onstart = function() {
//     recognizing = true;
//     start_img.src = 'static/img/mic-animate.gif';
//   };
//     recognition.onerror = function(event) {
//       if (event.error == 'no-speech') {
//         alert("No speech was detected. You may need to adjust your microphone settings")
//         ignore_onend = true;
//       }
//       if (event.error == 'audio-capture') {
//         alert("audio-capture")
//         ignore_onend = true;
//       }
//       if (event.error == 'not-allowed') {
//         alert("Permission to use microphone was denied.");
//         ignore_onend = true;
//       }
//     };
//     recognition.onend = function() {
//       recognizing = false;
//       if (ignore_onend) {
//         return;
//       }
//       start_img.src = 'static/img/mic.gif';
//     };
//
//     recognition.onresult = function(event) {
//     var interim_transcript = '';
//     for (var i = event.resultIndex; i < event.results.length; ++i) {
//       if (event.results[i].isFinal) {
//         final_transcript += event.results[i][0].transcript;
//       } else {
//         interim_transcript += event.results[i][0].transcript;
//       }
//     }
//     console.log(final_transcript)
//     final_transcript = capitalize(final_transcript);
//     msgerInput.value =linebreak(final_transcript);
//   };
//
//
// }
//
//   var two_line = /\n\n/g;
//   var one_line = /\n/g;
//   function linebreak(s) {
//   return s.replace(two_line, '<p></p>').replace(one_line, '<br>');
// }
//   var first_char = /\S/;
//   function capitalize(s) {
//   return s.replace(first_char, function(m) { return m.toUpperCase(); });
// }

function formatDate(date) {
  const h = "0" + date.getHours();
  const m = "0" + date.getMinutes();
  return `${h.slice(-2)}:${m.slice(-2)}`;
}
firstMsg = "Hi, welcome to iMedBot! Go ahead and send me a message. 😄"

window.οnlοad = appendMessage(BOT_NAME, NURSE_IMG, "left", firstMsg);



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





