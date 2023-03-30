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

// $( "#btn-bookmark" ).click(function() {
//     alert( "Handler for .click() called." );
// });

function bookmark(getButton, taskId) {
    alert(taskId);
    
    // const token = document.getElementByName("csrfmiddlewaretoken")[0].value;

    fetch(`/api/bookmark/${taskId}`, {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
            "X-CSRFToken": token,
            "Content-Type": 'application/json'
        }
    })
    .then(response => response.json())
    .then(result => {
        if (getButton.classList.contains("fa-heart")) {
            document.getElementById("bookmarkImg").src = "../static/images/reply.png";
    
        } else {
            document.getElementById("bookmarkImg").src = "../static/images/saved.png";
        }
    })
}

function getTaskDetail(id) {
    
    fetch(`/api/task/${id}`, {
        method: 'GET',
    })
    .then(response => response.json())
    .then(data => {
        
    })

}