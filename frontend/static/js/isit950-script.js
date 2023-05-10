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

let arrow = document.querySelectorAll(".arrow");

for (var i = 0; i < arrow.length; i++) {
    arrow[i].addEventListener("click", (e) => {
        let arrowParent = e.target.parentElement.parentElement;//selecting main parent of arrow
        arrowParent.classList.toggle("showMenu");
    });
}

// document.getElementById("comment-text").addEventListener("focus", function () {
//     $(".comment-form").addClass("comment-onfocus");
// });

// document.getElementById("comment-text").addEventListener("focusout", function () {
//     $(".comment-form").removeClass("comment-onfocus");
// });


function checkPostValue() {
    postValue = document.getElementById('comment-text').value;
    if (postValue == "") {
        document.getElementById("postBtn").disabled = true;
    } else {
        document.getElementById("postBtn").disabled = false;
    }
}

$('#postBtn123').click(function () {
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
});

window.onload = function () {
    window.onpopstate = function (event) {
        const urlParams = new URLSearchParams(window.location.search);
        const paramVal = urlParams.get('name');
        if (paramVal != '' && paramVal != null) {
            showDetail(paramVal);
            const newClass = document.querySelector('.task-detail-container');
            newClass.style.setProperty('transition', 'none');
        }
    };
};

$(document).ready(function () {

    const urlParams = new URLSearchParams(window.location.search);
    const paramVal = urlParams.get('name');
    if (paramVal != '' && paramVal != null) {
        showDetail(paramVal);
        const newClass = document.querySelector('.task-detail-container');
        newClass.style.setProperty('transition', 'none');
    }

    window.addEventListener('resize', function (event) {
        if ($(".search-overlay").hasClass("active-input")) {
            $(".search-overlay").removeClass("active-input")
        }
    }, true);

    $(".btn-search-nav").click(function () {
        if (screen.width < 646)
            $(".search-overlay").addClass("active-input");
    });

    $(".btn-input-close").click(function () {
        $(".search-overlay").removeClass("active-input");
    });

    // $('.search-input').change(function() {
    //     var searchKeyword = $(this).val();

    //     fetch(`/task/task_state/?search_keyword=${searchKeyword}`)
    //     .then(response => response.json())
    //     .then(result => {
    //         console.log(result)
    //     });
    // });

    $('.task-bookmark').click(function (event) {
        event.stopPropagation();
        var taskId = $(this).attr('data-id');

        const token = document.getElementsByName("csrfmiddlewaretoken")[0].value;
        
        fetch(`/api/watchlist`, {
            method: 'POST',
            credentials: 'same-origin',
            headers: {
                "X-CSRFToken": token,
                "Content-Type": 'application/json'
            },
            body: JSON.stringify({
                user: Cookies.get('usid'),
                task: taskId
            })
        })
            .then(response => response.json())
            .then(result => {
                if ($(this).find('i').hasClass('unbookmark')) {
                    $(this).find('i').removeClass("fa-regular unbookmark")
                    $(this).find('i').addClass("fa bookmarked")
                    toastr.success('Bookmarked the task');
                } else {
                    $(this).find('i').removeClass("bookmarked")
                    $(this).find('i').addClass("fa-regular unbookmark")
                    toastr.info('The task has been removed from your bookmark.');
                }
            })
    })

    $('.task-bookmark123').click(function (event) {


        var taskId = $(this).attr('data-task-id');
        showDetail(taskId)

    })

    $('.task-bookmark-mytask').click(function (event) {


        var taskId = $(this).attr('data-task-id');
        showmyTaskDetail(taskId)

    })

    $('.return-map').click(function (event) {
        if (!$(".task-detail-wrapper").hasClass("task-blank") && !$(".task-detail-container").hasClass("no-selected")) {
            $(".task-detail-wrapper").addClass("task-blank")
            $(".task-detail-container").addClass("no-selected")
        }
        history.pushState(null, null, `/tasks`)
        document.title = 'ISIT950 Group Project';
    })

    $('#offer-btn').click(function ($e) {
        taskPrice = parseFloat(document.getElementById("task-price").innerHTML).toFixed(0)

        offerPrice = taskPrice;
        adminFee = (taskPrice * 10) / 100;
        document.getElementById('offer-price').value = offerPrice
        document.getElementById('admin-fee').innerHTML = adminFee;
        document.getElementById('total-earn').innerHTML = offerPrice - adminFee;
    })

    $('#offer-price').keyup(function ($e) {
        if ($('#offer-price').val() > 0) {
            $amount = $e.target.value;
            $adminFee = ($amount * 10) / 100;
            $totalEarn = $amount - $adminFee;
            $('#admin-fee').text($adminFee)
            $('#total-earn').text($totalEarn)
        }
    });

    $('.comm-btn').click(function ($event) {
        const token = document.getElementsByName("csrfmiddlewaretoken")[0].value;
        const price = document.querySelector('#offer-price').value;
        const offerDesc = document.querySelector('#offer-desc').value;
        const adminFee = -Math.abs(Number(document.querySelector('#admin-fee').innerText));
        const totalEarn = document.querySelector('#total-earn').innerText;
        const urlParams = new URLSearchParams(window.location.search);
        const task = urlParams.get('name')

        fetch(`/api/offer`, {
            method: "POST",
            credentials: 'same-origin',
            headers: {
                "X-CSRFToken": token,
                "Content-Type": 'application/json'
            },
            body: JSON.stringify({
                'price': price,
                'description': offerDesc,
                'admin_fee': adminFee,
                'total_price': totalEarn,
                'task': task,
                'user': Cookies.get('usid')
            })
        })
            .then(response => response.json())
            .then(res => {
                console.log(res.status)
                if (res.status == 200) {
                    $('#offerModal').modal('toggle');
                    Swal.fire({
                        icon: 'success',
                        title: 'Success',
                        text: 'Your offer has been saved successfully'
                    }).then((result) => {
                        location.reload();
                    })
                    // success_mail();
                    // location.reload();
                } else {
                    alert("Cannot save");
                }
            })
            .catch(err => {
                alert(err)
            })
    })

    const creditCardInput = document.getElementById('cardNo');

    creditCardInput.addEventListener("input", (event) => {
        // Remove all non-digits from the input
        const input = event.target.value.replace(/\D/g, '');

        // Add a space after every 4 digits
        const formattedInput = input.replace(/(\d{4})/g, '$1 ').trim();

        // Set the formatted value back to the input
        event.target.value = formattedInput;
    });

    const expiryDateInput = document.getElementById("expiryDate");

    // Format the input value as an expiry date
    expiryDateInput.addEventListener("input", (event) => {
        // Remove all non-digits from the input
        const input = event.target.value.replace(/\D/g, '');

        // Add a slash after the second digit
        const formattedInput = input.replace(/^(\d{2})(\d{0,4})$/, '$1/$2').trim();

        // Set the formatted value back to the input
        event.target.value = formattedInput;
    });


    $('.cc-func').click(function ($event) {
        const token = document.getElementsByName("csrfmiddlewaretoken")[0].value;
        var cardNo = document.getElementById('cardNo').value;
        var expiryDate = document.getElementById("expiryDate").value;
        const cvc = document.getElementById("cvc").value;
        cardNo = cardNo.replace(/\D/g, '');
        expiryDate = expiryDate.replace(/\D/g, '');

        if (cardNo.length === 16 && checkExpiryCCMonth(expiryDate) === true && cvc.length === 3) {
            fetch(`/api/paymentInformation/${Cookies.get('usid')}`, {
                method: 'POST',
                credentials: 'same-origin',
                headers: {
                    "X-CSRFToken": token,
                    "Content-Type": 'application/json'
                },
                body: JSON.stringify({
                    'credit_card': cardNo, 
                    'expiry_date': expiryDate, 
                    'cvv': cvc
                })
            })
            .then(response => response.json())
            .then(res => {
                console.log(res)
                if (res.status == 200) {
                    $('#paymentMethodModal').modal('toggle');
                    Swal.fire({
                        icon: 'success',
                        title: 'Success',
                        text: 'Your payment has been saved'
                    }).then((result) => {
                        location.reload();
                    })
                } else {
                    alert("Cannot save");
                }
            })
            .catch(err => {
                alert(err)
            })
        } else {
            console.log(false)
        }

        
    })

    // $('#pending-offer').click(function() {
    //     var condition = $(this).data('condition');
    //     $.ajax({
    //       url: '/my-task/',
    //       data: {
    //         condition: condition
    //       },
    //       dataType: 'json',
    //       success: function(data) {
    //         // Code to update the HTML with the filtered data
    //       }
    //     });
    //   });

});

function checkExpiryCCMonth(expiryDate) {
    var result = true;

    const currentDate = new Date();

    const month = parseInt(expiryDate.slice(0, 2), 10);
    const year = parseInt(expiryDate.slice(2), 10)

    if (expiryDate.length === 4 && month >= 1 && month <= 12 && year >= currentDate.getFullYear() % 100) {
        const expiry = new Date(year + 2000, month - 1, 1);
        
        expiry.setMonth(expiry.getMonth() + 2);
        expiry.setDate(expiry.getDate() - 1);
        if (expiry < currentDate) {
            // The expiry date is valid, submit the form
            console.log("Invalid expiry date");
            result = false;
        }
    } else {
        // The expiry date is invalid, prevent the form from submitting
        result = false
        console.log("Invalid expiry date");
    }
    return result
}

function showDetail(taskId) {
    if ($(".task-detail-wrapper").hasClass("task-blank") && $(".task-detail-container").hasClass("no-selected")) {
        $(".task-detail-wrapper").removeClass("task-blank")
        $(".task-detail-container").removeClass("no-selected")
    }

    fetch(`/api/task/${taskId}`)
        .then(response => response.json())
        .then(result => {
            document.querySelector('#task-detail-header').innerHTML = `${result.task_title}`;
            document.querySelector('#task-active-lg').innerHTML = `${result.status}`;
            document.querySelector('#tasker-client').innerHTML = `${result.first_name} ${result.last_name}`;
            document.querySelector('#task-location').innerHTML = `${result.location}`;
            document.querySelector('#task-completed-on').innerHTML = `${result.completed_on}`;
            document.querySelector('#task-price').innerHTML = `${result.price}`;
            document.querySelector('#task-desc').innerHTML = `${result.description}`;
            history.pushState(null, null, `/tasks/?name=${taskId}`)
            document.title = `${taskId} - ISIT950 Group Project`;
        })
}

function showmyTaskDetail(taskId) {
    if ($(".task-detail-container").hasClass("no-selected")) {
        $(".task-detail-container").removeClass("no-selected")
    }

    fetch(`/api/task/${taskId}`)
    .then(response => response.json())
    .then(result => {
        document.querySelector('#task-detail-header').innerHTML = `${result.task_title}`;
        document.querySelector('#task-active-lg').innerHTML = `${result.status}`;
        document.querySelector('#tasker-client').innerHTML = `${result.first_name} ${result.last_name}`;
        document.querySelector('#task-location').innerHTML = `${result.location}`;
        document.querySelector('#task-completed-on').innerHTML = `${result.completed_on}`;
        document.querySelector('#task-price').innerHTML = `${result.price}`;
        document.querySelector('#task-desc').innerHTML = `${result.description}`;
        history.pushState(null, null, `/my-task/?name=${taskId}`)
        document.title = `${taskId} - ISIT950 Group Project`;
    })
}

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

