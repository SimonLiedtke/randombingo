function table2html(tableData) {
    // build the DOM with .text() so values are never parsed as HTML
    var $table = $("<table>").addClass("scrolling-wrapper-flexbox");
    for (let row of tableData) {
        var $tr = $("<tr>").appendTo($table);
        for (let value of row) {
            // null marks a padding cell without a value
            $("<td>").text(value === null ? "" : value)
                .toggleClass("blank", value === null).appendTo($tr);
        }
    }
    return $table;
}

function getCurrentTableData() {
    var data = [];
    // padding cells (.blank) carry no value, so don't send them back
    $("td:not(.blank)").each(function(index) {
        data.push($(this).text());
    })
    return data;
}

function refreshTable(newTable) {
    // remove <table> if it exists
    $("table").remove();
    // create new table after main div
    table2html(newTable).appendTo("#main");
}
