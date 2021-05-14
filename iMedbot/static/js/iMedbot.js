
// Icons made by Freepik from www.flaticon.com
const BOT_IMG = "static/img/robot.svg";
const PERSON_IMG = "static/img/woman.svg";
const BOT_NAME = "iMedBot";
const PERSON_NAME = "You";

// get the element for html

const msgerForm = get(".msger-inputarea");
const msgerInput = get(".msger-input");
const msgerChat = get(".msger-chat");

const record = document.getElementById("record");
record.onclick = transfervoice;


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
    appendMessage(BOT_NAME, BOT_IMG, "left", msgText);
  });
}

// Utils
function get(selector, root = document) {
  return root.querySelector(selector);
}

// var create_email = false;
// var final_transcript = '';
// var recognizing = false;
// var ignore_onend;

// if (!('webkitSpeechRecognition' in window)) {
//   upgrade();
// } else {
//   start_button.style.display = 'inline-block';
//   var recognition = new webkitSpeechRecognition();
//   recognition.continuous = true;
//   recognition.interimResults = true;
//
// function startButton(event) {
//   if (recognizing) {
//     recognition.stop();
//     return;
//   }
//   final_transcript = '';
//   recognition.lang = 'en-US';
//   recognition.start();
//   ignore_onend = false;
//   final_span.innerHTML = '';
//   interim_span.innerHTML = '';
//   start_img.src = 'mic-slash.gif';
//   showInfo('info_allow');
//   showButtons('none');
//   start_timestamp = event.timeStamp;
// }
//
// function upgrade() {
//   record.innerText = "Start"
//
// }


function transfervoice(){
  if (recognizing) {
    recognition.stop();
    return;
  }
  // record.innerText = "Start"
  var recognizing = false;
  var ignore_onend = false;
  var lang = 'en-US'
  var final_transcript = '';
  var recognition = new webkitSpeechRecognition();
  recognition.lang = lang;
  recognition.continuous = true;//if allowed continue listen
  recognition.interimResults = true;
  recognition.start();

  recognition.onstart = function() {
    recognizing = true;
    record.innerText = "Recording"

    // start_img.src = 'mic-animate.gif';
  };
    recognition.onerror = function(event) {
      if (event.error == 'no-speech') {
        alert("No speech was detected. You may need to adjust your microphone settings")
        ignore_onend = true;
      }
      if (event.error == 'audio-capture') {
        alert("audio-capture")
        ignore_onend = true;
      }
      if (event.error == 'not-allowed') {
        alert("Permission to use microphone was denied.");
        ignore_onend = true;
      }
    };

    recognition.onend = function() {
      recognizing = false;
      record.innerText = "Start"
      if (ignore_onend) {
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
    console.log(final_transcript)
    msgerInput.value = final_transcript;
    // recognition.stop()
    // #interim_span.innerHTML = linebreak(interim_transcript);

  };


}

function formatDate(date) {
  const h = "0" + date.getHours();
  const m = "0" + date.getMinutes();
  return `${h.slice(-2)}:${m.slice(-2)}`;
}
firstMsg = "Hi, welcome to iMedBot! Go ahead and send me a message. 😄"

window.οnlοad = appendMessage(BOT_NAME, BOT_IMG, "left", firstMsg);

