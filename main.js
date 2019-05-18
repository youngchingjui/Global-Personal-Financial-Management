window.onload = function() {
    $("#balance").text("10,230")
    $("#add_account_btn").click(add_account)
}

function add_account() {
    console.log("Adding account")

    // Add another row of inputs
    var copy = $("#accounts_form").clone()
    var id_num = getHighestIDNumber()
    copy.attr('id', 'accounts_form'+(id_num+1))
    $("#accounts_block").append(copy)
}

function getHighestIDNumber() {
    var a = $(".form_row")
    var b = [];
    for (i = 0; i<a.length; i++) {
        b.push(a[i].id)

    var c = []
    for (j in b) {

        // Gets the number at the end of the id name and adds it to c, and converts to Number
        c.push(Number(j.split("form_row")[1]))
    }

    // Return the highest number from that list
    return Math.max(...c)
}