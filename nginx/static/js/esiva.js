'use strict';

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function setCookie(cname, cvalue, exdays) {
  const d = new Date();
  d.setTime(d.getTime() + (exdays*24*60*60*1000));
  let expires = "expires="+ d.toUTCString();
  document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function openModal() {
  const responseModal = $('#formResponseModal');
  const infoIcon = $('.board-page-info-container');

  if (infoIcon.length) {
    if (!getCookie('board-info-opened')) {
      $('#boardInfo').modal('show');
      setCookie('board-info-opened', true, 1);
    }

    infoIcon.on('click', function() {
      $('#boardInfo').modal('show');
    });
  }

  if (responseModal.length) {
    responseModal.modal('show');
  }
}

(function() {
  openModal();
})();
