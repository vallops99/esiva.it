let registrationTime = 0;

function showTimes() {
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

(function() {
  let isRegStarted = false;
  let intervalId;
  let mediaRecorder;
  let audio = null;

  $('.dog-life-mic svg').on('click', function(e) {
    e.preventDefault();

    // revert bool as registration status just changed
    isRegStarted = !isRegStarted;

    if (isRegStarted) {
      navigator.mediaDevices.getUserMedia({ audio: true })
      .then(stream => {
        mediaRecorder = new MediaRecorder(stream);

        if (!audio) {
          $('.dog-life-time-passed').html('');
          $('.dog-life-cancel').addClass('d-none');
          $('.dog-life-play').addClass('d-none');
          $('.dog-life-pause').addClass('d-none');
          $('.dog-life-send').addClass('d-none');
          audio = null;
          audioUrl = null;
          audioBlob = null;
        }

        $(e.target).css('fill', 'red');
        intervalId = setInterval(showTimes, 1000);

        mediaRecorder.start();

        const audioChunks = [];
        mediaRecorder.addEventListener("dataavailable", event => {
          audioChunks.push(event.data);
        });

        mediaRecorder.addEventListener("stop", () => {
          const audioBlob = new Blob(audioChunks);
          const audioUrl = URL.createObjectURL(audioBlob);

          audio = new Audio(audioUrl);

          $('.dog-life-cancel').removeClass('d-none');
          $('.dog-life-send').removeClass('d-none');
          $('.dog-life-play').removeClass('d-none')
            .on('click', function(e) {
              $(this).addClass('d-none');
              $('.dog-life-pause').removeClass('d-none');

              audio.play();

              audio.addEventListener('ended', () => {
                $(this).removeClass('d-none');
                $('.dog-life-pause').addClass('d-none');
              });
            });

            $('.dog-life-pause').on('click', function(e) {
              audio.pause();

              $(this).addClass('d-none');
              $('.dog-life-play').removeClass('d-none');
            });

            $('.dog-life-cancel').on('click', function(e) {
              audio.pause();
              $(this).addClass('d-none');
              $('.dog-life-send').addClass('d-none');
              $('.dog-life-play').addClass('d-none');
              $('.dog-life-pause').addClass('d-none');
              $('.dog-life-time-passed').html('');
              audio = null;
              audioUrl = null;
              audioBlob = null;
              mediaRecorder = null;
            });

            $('.dog-life-send').on('click', function() {
              $.post("/api/store-audio", {
                  audio: mediaRecorder.forceDownload(audioBlob, 'output.wav')
              });

              $('.dog-life-play').addClass('d-none');
              $('.dog-life-pause').addClass('d-none');
              $('.dog-life-cancel').addClas('d-none');
              $('.dog-life-send').addClass('d-none');
              $('.dog-life-time-passed').html('');
              audio = null;
              audioUrl = null;
              audioBlob = null;
              mediaRecorder = null;
            });
        });
      });

    } else {
      mediaRecorder.stop();

      $(e.target).css('fill', 'black');
      clearInterval(intervalId);
      registrationTime = 0;
    }
  });
})();
