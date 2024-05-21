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

  // A set to store the IDs of the tools that have been added
  const addedTools = new Set();

  // Handle the "Add Item" button
  $('#addInvoiceItem').on('click', () => {
    $.ajax({
      url: '/sell-invoices/get-invoice-item-form', // The URL of the route that returns a new form
      method: 'GET',
      success(data) {
        // Append the new form to the table
        $('#invoiceItemsBody').append(data);

        // Get the select dropdown in the newly added row
        const select = $('#invoiceItemsBody').find('select:last');

        // Remove the options for the tools that have been added
        select.children().each(function selectOption() {
          if (addedTools.has($(this).val())) {
            $(this).remove();
          }
        });

        // Number the rows
        $('#invoiceItemsBody tr').each((index, row) => {
          $(row).find('td:first-child').text(index + 1);
        });
      },
    });
  });

  // Handle the "Remove" buttons
  $('#invoiceItemsBody').on('click', '.remove-sell-invoice-item-btn', function removeRow() {
    // Remove the parent table row of the button
    $(this).parents('tr').remove();

    // Remove the tool from the set of added tools
    addedTools.delete($(this).parents('tr').find('select').val());
  });

  // Handle the change event of the tool dropdowns
  $('#invoiceItemsBody').on('change', 'select', function selectToolDropdownChange() {
    // Remove the previous value from the set of added tools
    addedTools.delete($(this).data('previous'));

    // Add the new value to the set of added tools
    addedTools.add($(this).val());

    // Update the previous value
    $(this).data('previous', $(this).val());
  });
});
