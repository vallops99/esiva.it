'use strict';

let registrationTime = 0;

function showTimes(init = false) {
  if (init) {
    $('.dog-life-time-passed').html('00' + ':' + '00');
    return;
  }
  registrationTime += 1;
  let seconds = normalizeTime(registrationTime % 60);
  let minutes = normalizeTime(parseInt(registrationTime / 60));
  $('.dog-life-time-passed').html(minutes + ":" + seconds);
}

function normalizeTime(val) {
  var valString = val + "";
  if (valString.length < 2) {
    return "0" + valString;
  } else {
    return valString;
  }
}

function checkAudioAvailability() {
  if (typeof MediaRecorder === 'undefined') {
    $('.dog-life-mic svg').addClass('audio-not-supported');
    $('.dog-life-error').html('Il tuo browser non supporta la registrazione audio, perfavore carica il file manualmente').removeClass('d-none');

    return false;
  }

  return true;
}

function resetAudio() {
  $('.dog-life-time-passed').html('');
  $('.dog-life-audio #audio-source').attr('src', '');
  $('.dog-life-audio').addClass('d-none');
  $('.dog-life-cancel').addClass('d-none');
  $('.dog-life-send').addClass('d-none');
  $('.dog-life-error').addClass('d-none');
  $('.dog-life-mic svg').css('fill', 'black');
  return true;
}

async function initAudioRecorder() {

  let isRegStarted = false;
  let mediaRecorder = null;
  let intervalId;
  let isResetted = resetAudio();

  $('.dog-life-mic svg').on('click', function(e) {
    e.preventDefault();

    // revert bool as registration status just changed
    isRegStarted = !isRegStarted;

    if (isRegStarted) {
      navigator.mediaDevices.getUserMedia({ audio: true })
      .then(function(stream) {
        if (!isResetted) {
          isResetted = resetAudio();
        }

        isResetted = !isResetted;

        mediaRecorder = new MediaRecorder(stream);

        $(e.target).css('fill', 'red');
        showTimes(true);
        intervalId = setInterval(showTimes, 1000);

        mediaRecorder.start();

        const audioChunks = [];
        mediaRecorder.addEventListener("dataavailable", event => {
          audioChunks.push(event.data);

          if (mediaRecorder.state === "inactive") {
            const audioBlob = new Blob(audioChunks, {
              type: 'audio/webm; codecs=opus',
            });
            const audioUrl = URL.createObjectURL(audioBlob);

            const eventToListen = ((window.isTouchDevice) ? 'touchend' : 'click');

            const audio = new Audio(audioUrl);

            $('#audio-source').attr('src', audioUrl);
            $('#audio-source-recovery').attr('src', audioUrl);
            $('#dog-audio')[0].load();
            $('.dog-life-audio').removeClass('d-none');

            $('.dog-life-cancel').removeClass('d-none');
            $('.dog-life-send').removeClass('d-none');

            $('.dog-life-cancel').on('click', function(e) {
              e.preventDefault();

              audio.pause();
              isResetted = resetAudio();
            });

            $('.dog-life-send').on('click', function(e) {
              e.preventDefault();

              const audioForm = new FormData();
              audioForm.append('file', audioBlob, 'eugenio-audio.mp3');

              $.ajax({
                url: '/api/store-audio',
                type: 'POST',
                headers: {
                  'X-CSRFToken': getCookie('csrftoken')
                },
                data: audioForm,
                processData: false,
                contentType: false,

                success: function() {
                  isResetted = resetAudio();
                  $('#audioResponseModal').modal('show');
                },
                failure: function() {
                  isResetted = resetAudio();
                }
              });
            });
          }
        });
      });

    } else {
      mediaRecorder.stop();

      clearInterval(intervalId);
      $(e.target).css('fill', 'black');
      registrationTime = 0;
    }
  });
}

function checkFileUpload() {
  $('.dog-life-input-file').on('input', function(e) {
    if (e.target.value) {
      $('.dog-life-send-uploaded').prop('disabled', false);
    } else {
      $('.dog-life-send-uploaded').prop('disabled', true);
    }
  });
}

(function() {
  if (window.openModalResponse === 'True') {
    $('#audioResponseModal').modal('show');
  }
  // const isAudioAvailable = checkAudioAvailability();

  // if (isAudioAvailable) {
  initAudioRecorder();
  // }

  checkFileUpload();
})();
