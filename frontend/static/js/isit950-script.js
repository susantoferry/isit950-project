document.getElementById("comment-text").addEventListener("focus", function () {
    $(".comment-form").addClass("comment-onfocus"); 
});

document.getElementById("comment-text").addEventListener("focusout", function () {
    $(".comment-form").removeClass("comment-onfocus");
});


function checkPostValue(){
    postValue = document.getElementById('comment-text').value;
    if (postValue == "") {
        document.getElementById("postBtn").disabled = true;
    } else {
        document.getElementById("postBtn").disabled = false;
    }
}
