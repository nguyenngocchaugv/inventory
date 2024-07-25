$(() => {
  // Delete location confirmation
  let deleteUrl;

  $('.locations-delete-btn').on('click', (event) => {
    deleteUrl = $(event.currentTarget).data('url');
  });

  $('#locations-on-confirm-delete-btn').on('click', (event) => {
    event.preventDefault();
    if (!deleteUrl) {
      return;
    }

    const csrfToken = $('meta[name="csrf-token"]').attr('content');
    fetch(deleteUrl, {
      method: 'POST',
      headers: {
        'X-CSRFToken': csrfToken,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        window.location.href = data.redirect_url;
      });
  });

  // Discard changes
  let discardUrl;

  $('#location-discard-changes-btn').on('click', (event) => {
    discardUrl = $(event.currentTarget).data('url');
  });

  $('#location-on-discard-changes-btn').on('click', (event) => {
    event.preventDefault();
    if (!discardUrl) {
      return;
    }

    window.location.href = discardUrl;
  });
});
