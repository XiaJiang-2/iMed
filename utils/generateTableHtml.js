function csvToArray(str, delimiter = ",") {
  // slice from start of text to the first \n index
  // use split to create an array from string by delimiter
  const headers = str.slice(0, str.indexOf("\n")).split(delimiter);

  // slice from \n index + 1 to the end of the text
  // use split to create an array of each csv value row
  const rows = str.slice(str.indexOf("\n") + 1).split("\n");

  // Map the rows
  // split values from each row into an array
  // use headers.reduce to create an object
  // object properties derived from headers:values
  // the object passed as an element of the array
  const arr = rows.map(function (row) {
    const values = row.split(delimiter);
    const el = headers.reduce(function (object, header, index) {
      object[header] = values[index];
      return object;
    }, {});
    return el;
  });

  // return the array
  return arr;
}
function gerateTableHtml(dataset) {
    var array = csvToArray(dataset, delimiter = ",")
    const tablehead = Object.keys(array[0]);
    for(var  i= 0; i< tablehead.length; i++) {
        tableHTML+= '<th>' + tablehead[i] + '</th>'
    }
    tableHTML += '</tr></thead>'

    for(var row = 0; row< array.length; row++) {
       tableHTML+= '<tbody><tr>'
        value_list = Object.values(array[row])
            for(var col= 0; col< value_list.length; col++) {
                tableHTML+= '<td>' + value_list[col] + '</td>'
            }
       tableHTML+= '</tr></tbody>'
    }

}
