import { formatThousands } from './script';

$(() => {
  // Delete tool confirmation
  let deleteUrl;

  $('.tools-delete-btn').on('click', (event) => {
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
  let rowCount = 0; // The number of rows in the table
  let toolPrices; // A map of tool IDs to prices

  // Handle the "Add Item" button
  $('#addInvoiceItem').on('click', () => {
    $.ajax({
      url: `/sell-invoices/get-invoice-item-form/${rowCount}`, // The URL of the route that returns a new form
      method: 'GET',
      success(data) {
        // Store the tool prices in the toolPrices variable
        toolPrices = data.tool_prices;
        // Append the new form to the table
        $('#invoiceItemsBody').append(data.form_html);

        // Number the rows
        $('#invoiceItemsBody tr').each((index, row) => {
          $(row).find('td:first-child').text(index + 1);
        });
      },
    });

    rowCount += 1;
  });

  // Handle the "Remove" buttons
  $('#invoiceItemsBody').on('click', '.remove-sell-invoice-item-btn', function removeRow() {
    // Remove the parent table row of the button
    $(this).parents('tr').remove();
  });

  // Handle the change event of the tool dropdowns
  $('#invoiceItemsBody').on('change', 'select, .quantity-input', function selectToolDropdownChange() {
    // Get the row that contains the changed element
    const row = $(this).closest('tr');

    // Get the ID of the selected tool
    const toolId = row.find('select').val();

    // Get the price of the selected tool from the toolPrices variable
    const price = parseFloat(toolPrices[`tool_${toolId}`]);
    const priceWithTwoDecimals = price.toFixed(2);

    // Set the price in the tool-price field
    $(this).closest('tr').find('.tool-price').text(priceWithTwoDecimals);

    // Get the quantity
    const quantity = $(this).closest('tr').find('.quantity-input').val();

    // If either the price or the quantity is not defined, set the total price to zero
    if (!price || !quantity) {
      $(this).closest('tr').find('.total-price').text(0);
      return;
    }

    // Calculate the total price
    const totalPrice = price * quantity;

    // Set the text of the total price cell
    $(this).closest('tr').find('.total-price').text(formatThousands(totalPrice));
  });
});
