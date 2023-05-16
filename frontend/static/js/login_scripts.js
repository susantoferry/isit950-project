 /*================================
    login form
    ==================================*/

    $('.fm-grp input').on('focus', function() {
        $(this).parent('.fm-grp').addClass('focused');
    });
    $('.fm-grp input').on('focusout', function() {
        if ($(this).val().length === 0) {
            $(this).parent('.fm-grp').removeClass('focused');
        }
    });

