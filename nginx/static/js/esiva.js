function openModal() {
  const modal = $('#formResponseModal');

  if (modal.length) {
    modal.modal('show');
  }
}

(function() {
  openModal();
})();
