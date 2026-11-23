function table2html(tableData) {
    // build the DOM with .text() so values are never parsed as HTML
    var $table = $("<table>").addClass("scrolling-wrapper-flexbox");
    for (let row of tableData) {
        var $tr = $("<tr>").appendTo($table);
        for (let value of row) {
            $("<td>").text(value).toggleClass("blank", value == "[BLANK]")
                .appendTo($tr);
        }
    }
    return $table;
}

function getCurrentTableData() {
    var data = [];
    $("td").each(function(index) {
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
