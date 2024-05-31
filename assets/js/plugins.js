// place any jQuery/helper plugins in here, instead of separate, slower script files.
$(() => {
  const input = document.getElementById('search-input');
  if (!input) return;

  window.toggleClearButton = () => {
    const button = document.getElementById('clear-button');
    if (input?.value) {
      button?.classList?.remove('d-none');
    } else {
      button?.classList?.add('d-none');
    }
  };

  window.clearSearch = () => {
    const button = document.getElementById('clear-button');
    input.value = '';
    button?.classList?.add('d-none');
  };

  // Call the function once when the page loads to set the initial button visibility
  window.toggleClearButton();
});
