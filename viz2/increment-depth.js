function incrementValue()
{
    var value = parseInt(document.getElementById('inc').value, 10);
    value = isNaN(value) ? 0 : value;
    value++;
    document.getElementById('inc').value = value;

    var parent = document.getElementById("svg");
    removeAllChildNodes(parent)
    parent.remove();
    setupTree();
}