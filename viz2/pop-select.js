fetch("../shared/clusters.json")
.then(res => res.json())
.then(data => {
    var ele = document.getElementById('search-select3');

    for (var i = 0; i < data.length; i++) {
        ele.innerHTML = ele.innerHTML +
        '<div class="item">'+
        '<span class="text">'+data[i]["complex"]+'</span>'+
        '<span class="description">'+data[i]["size"]+'</span>'
        +'</div>';
    }
});

$(document).ready(function(){
    $('#search-select').dropdown()
}); 