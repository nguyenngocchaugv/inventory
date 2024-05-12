$(() => {
  // Delete tool confirmation
  let deleteUrl;

  $('#tools-delete-btn').on('click', (event) => {
    deleteUrl = $(event.currentTarget).data('url');
  });

  $('#tools-on-confirm-delete-btn').on('click', (event) => {
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

  $('#tool-discard-changes-btn').on('click', (event) => {
    discardUrl = $(event.currentTarget).data('url');
  });

  $('#tool-on-discard-changes-btn').on('click', (event) => {
    event.preventDefault();
    if (!discardUrl) {
      return;
    }

    window.location.href = discardUrl;
  });
});
