function main(workbook: ExcelScript.Workbook) {
  // Get the active cell and worksheet.
  let selectedCell = workbook.getActiveCell();
  let selectedSheet = workbook.getActiveWorksheet();
  let selectedRange = workbook.getSelectedRange();
  let values = selectedRange.getValues()

  // Modify each row by combining columns 0 and 1, then include columns 11 to 17
  // Note: Adjusting for zero-based indexing, so columns 11 to 17 are actually indexes 10 to 17 in code
  let csvContent = values.map(row => {
    // Combine the first two columns (0 and 1)
    let combinedFirstTwo = `${row[0]}${row[1]}`;
    // Extract the desired range from each row (columns 11 to 17)
    let selectedColumns = row.slice(10, 18);
    // Prepend the combined columns to the selected range and join with commas for CSV format
    return [combinedFirstTwo, ...selectedColumns].join(",");
  }).join("\n");

  // Log the CSV content
  console.log(csvContent);