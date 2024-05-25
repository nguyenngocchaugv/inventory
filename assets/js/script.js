// App initialization code goes here
export function formatThousands(value) {
  if (value === null || value === undefined) {
    return '';
  }
  return value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}
