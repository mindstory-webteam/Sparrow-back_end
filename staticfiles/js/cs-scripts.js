 
//   Background image ------------------
var a = $(".bg");
a.each(function () {
    if ($(this).attr("data-bg")) $(this).css("background-image", "url(" + $(this).data("bg") + ")");
});
/**
 Countdown clock with offset
 */
(function($){$.fn.downCount=function(options,callback){var settings=$.extend({date:null,offset:null},options);if(!settings.date){$.error('Date is not defined.')}if(!Date.parse(settings.date)){$.error('Incorrect date format, it should look like this, 12/24/2012 12:00:00.')}var container=this;var currentDate=function(){var date=new Date();var utc=date.getTime()+(date.getTimezoneOffset()*60000);var new_date=new Date(utc+(3600000*settings.offset));return new_date};function countdown(){var target_date=new Date(settings.date),current_date=currentDate();var difference=target_date-current_date;if(difference<0){clearInterval(interval);if(callback&&typeof callback==='function')callback();return}var _second=1000,_minute=_second*60,_hour=_minute*60,_day=_hour*24;var days=Math.floor(difference/_day),hours=Math.floor((difference%_day)/_hour),minutes=Math.floor((difference%_hour)/_minute),seconds=Math.floor((difference%_minute)/_second);days=(String(days).length>=2)?days:'0'+days;hours=(String(hours).length>=2)?hours:'0'+hours;minutes=(String(minutes).length>=2)?minutes:'0'+minutes;seconds=(String(seconds).length>=2)?seconds:'0'+seconds;var ref_days=(days===1)?'day':'days',ref_hours=(hours===1)?'hour':'hours',ref_minutes=(minutes===1)?'minute':'minutes',ref_seconds=(seconds===1)?'second':'seconds';container.find('.days').text(days);container.find('.hours').text(hours);container.find('.minutes').text(minutes);container.find('.seconds').text(seconds);container.find('.days_ref').text(ref_days);container.find('.hours_ref').text(ref_hours);container.find('.minutes_ref').text(ref_minutes);container.find('.seconds_ref').text(ref_seconds)};var interval=setInterval(countdown,1000)}})(jQuery);    
if ($(".counter-widget").length > 0) {
    var countCurrent = $(".counter-widget").attr("data-countDate");
    $(".countdown").downCount({
        date: countCurrent,
        offset: 0
    });
}
$.fn.duplicate = function (a, b) {
    var c = [];
    for (var d = 0; d < a; d++) $.merge(c, this.clone(b).get());
    return this.pushStack(c);
};
$("<span class='arrow_dec_dot'></span>").duplicate(9).appendTo(".arrow_dec");
$('head').append('<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0">');
$("<div class='pl-row'><span class='pl-row-anim'></span></div>").duplicate(25).appendTo(".ds_dec-grid");
function heroAnim() {
    $(".pl-row-anim").removeClass("pl-row-anim-dec-vis");
    randomItem();
    function randomItem() {
        for (var i = 0; i < 8; i++) {
            var length = $(".pl-row-anim").length;
            var random = Math.floor(Math.random() * length);
            $(".pl-row-anim").eq(random).addClass("pl-row-anim-dec-vis");
        }
    }
}
setInterval(function () {
    heroAnim();
}, 2600);
$(".loader-wrap").append('<div class="loader-wrap-container fs-wrapper" data-ran="25"></div>');
$("<div class='lw-dot'><span class='lw-dot-anim'></span></div>").duplicate(25).appendTo(".loader-wrap-container");

function firstload() {
    function a(a) {
        var b = a.length,
            c, d;
        while (b) {
            d = Math.floor(Math.random() * b--);
            c = a[b];
            a[b] = a[d];
            a[d] = c;
        }
        return a;
    }
    setTimeout(function () {
        $(".loader-spin").addClass("novisspin");
        $("#main").addClass("vis-main");
    }, 1300);

    setTimeout(function () {
        var b = $(".lw-dot-anim");
        $(a(b).slice(0, $(".loader-wrap-container").data("ran"))).each(function (a) {
            var b = $(this);
            setTimeout(function () {
                b.addClass("hid-lw-row");
            }, 30 * a);
        });
    }, 1500);
    $(".loader-wrap").delay(2200).fadeOut(1)
}
firstload();
document.addEventListener('gesturestart', function (e) {
    e.preventDefault();
});
//   Contact form------------------
var coninw = $(".contact-form-container-box"),
    coninbtn = $(".contact-form-btn");
function showConInfo() {
    $(".contact-form-wrap").fadeIn(300);
    setTimeout(function () {
        coninw.addClass("vis-coninfwrap");
    }, 500);
    coninbtn.removeClass("isconin-btn_vis");
}
function hideConInfo() {
    coninw.removeClass("vis-coninfwrap");
    coninbtn.addClass("isconin-btn_vis");
    $(".contact-form-wrap").fadeOut(100);
}
coninbtn.on("click", function () {
    if ($(this).hasClass("isconin-btn_vis")) showConInfo();
    else hideConInfo();
});
$(".act-cf").on("click", function () {
    showConInfo();
});
$(".close-cf , .contact-form-overlay").on("click", function (e) {
    e.preventDefault();
    hideConInfo();
    $("#message").slideUp(200);
    $(".custom-form").find("input[type=text], textarea").val("");
});
$(document).on('submit', '#contactform', function () {
    var a = $(this).attr("action");
    $("#message").slideUp(750, function () {
        $("#message").hide();
        $("#submit").attr("disabled", "disabled");
        $.post(a, {
            name: $("#name").val(),
            email: $("#email").val(),
            comments: $("#comments").val()
        }, function (a) {
            document.getElementById("message").innerHTML = a;
            $("#message").slideDown("slow");
            $("#submit").removeAttr("disabled");
            if (null != a.match("success")) $("#contactform").slideDown("slow");
        });
    });
    return false;
});
$(document).on('keyup', '#contactform input, #contactform textarea', function () {
    $("#message").slideUp(1500);
});
$('.out_label').on('focusin', function () {
    $(this).parents(".input-holder").find('label').addClass('active_lab');
});
$('.out_label').on('focusout', function () {
    if (!this.value) {
        $(this).parents(".input-holder").find('label').removeClass('active_lab');
    }
});
