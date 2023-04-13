const Toast = Swal.mixin({
    toast: true,
    position: 'bottom-end',
    showConfirmButton: false,
    timer: 3000,
    timerProgressBar: true,
    didOpen: (toast) => {
        toast.addEventListener('mouseenter', Swal.stopTimer)
        toast.addEventListener('mouseleave', Swal.resumeTimer)
    }
})

document.getElementById("comment-text").addEventListener("focus", function () {
    $(".comment-form").addClass("comment-onfocus");
});

document.getElementById("comment-text").addEventListener("focusout", function () {
    $(".comment-form").removeClass("comment-onfocus");
});


function checkPostValue() {
    postValue = document.getElementById('comment-text').value;
    if (postValue == "") {
        document.getElementById("postBtn").disabled = true;
    } else {
        document.getElementById("postBtn").disabled = false;
    }
}

$('#postBtn').click(function () {
    var urlArr = document.URL.split('/');
    var taskId = window.location.href.split("-").pop()

    const token = document.getElementsByName("csrfmiddlewaretoken")[0].value;

    fetch(`/api/question/${taskId}`, {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
            "X-CSRFToken": token,
            "Content-Type": 'application/json'
        },
        body: JSON.stringify({
            user: 1,
            task: taskId,
            question: document.querySelector('#comment-text').value
        })
    })
    .then(response => response.json())
    .then(result => {
        Swal.fire({
            icon: 'success',
            title: 'Success',
            text: 'Your comment has been posted',
        }).then((result) => {
            location.reload();
        })
    })
})


function accept_offer() {
    const token = document.getElementsByName("csrfmiddlewaretoken")[0].value;
    // const fname = document.querySelector('#first_name').value;

    Swal.fire({
        icon: 'success',
        title: 'Thank you',
        text: 'We have got your enquiry'
    }).then((result) => {
        location.reload();
    })

    // fetch('/api/accept-offer/', {
    //     method: "POST",
    //     credentials: 'same-origin',
    //     headers: {
    //         "X-CSRFToken": token,
    //         "Content-Type": 'application/json'
    //     },
    //     body: JSON.stringify({fname, lname, email, phone, msg})
    // })
    // .then(response => response.json())
    // .then(res => {
    //     if (res.error) {
    //         alert("Cannot save");
    //     } else {
    //         Swal.fire({
    //             icon: 'success',
    //             title: 'Thank you',
    //             text: 'We have got your enquiry'
    //         }).then((result) => {
    //             location.reload();
    //         })
    //     }
    // })
    // .catch(err => {
    //     alert(err)
    // })
}

// $('.task-left-card').click(function () {
//     var taskId = $(this).attr('data-id');

//     // location.href = "/tasks/" + taskId;
//     $("#mydiv").load("#mydiv");
//     console.log("a")
// })

// document.addEventListener("DOMContentLoaded", function() {
//     document.querySelectorAll('.task-left-card').forEach(a => {
//         a.onclick = function(e) {
//             e.preventDefault()
//             // console.log(this.dataset.taskId);

//             fetch(`/tasks/${this.dataset.taskId}`)
//             .then(response => response.text())
//             .then(res => {
//                 const obj = JSON.parse(res)
//                 console.log(obj.taskDetail.id)
//                 // history.pushState(null, '', `/tasks/${this.dataset.taskId}`)
                
//             });
            
            
//         }
//     })
// });

// $( "#btn-bookmark" ).click(function() {
//     alert( "Handler for .click() called." );
// });

function bookmark(getButton, taskId) {

    const token = document.getElementsByName("csrfmiddlewaretoken")[0].value;

    alert(id)
    // fetch(`/api/bookmark/${taskId}`, {
    //     method: 'POST',
    //     credentials: 'same-origin',
    //     headers: {
    //         "X-CSRFToken": token,
    //         "Content-Type": 'application/json'
    //     }
    // })
    // .then(response => response.json())
    // .then(result => {
    //     if (getButton.classList.contains("fa-heart")) {
    //         document.getElementById("bookmarkImg").src = "../static/images/reply.png";

    //     } else {
    //         document.getElementById("bookmarkImg").src = "../static/images/saved.png";
    //     }
    // })
}

// function getTaskDetail() {

//     fetch(`/api/task/${id}`, {
//         method: 'GET',
//     })
//         .then(response => response.json())
//         .then(data => {

//         })

// }