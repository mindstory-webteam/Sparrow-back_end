function initTrustbook() {
    "use strict";
    //   Background image ------------------
    var a = $(".bg");
    a.each(function (a) {
        if ($(this).attr("data-bg")) $(this).css("background-image", "url(" + $(this).data("bg") + ")");
    });
    //   Isotope------------------
    function nrg() {
        if ($(".gallery-items").length) {
            var a = $(".gallery-items").isotope({
                singleMode: true,
                columnWidth: ".grid-sizer, .grid-sizer-second, .grid-sizer-three",
                itemSelector: ".gallery-item, .gallery-item-second, .gallery-item-three",
                singleMode: true,
                transformsEnabled: true,
                transitionDuration: "900ms"
            });
            a.imagesLoaded(function () {
                a.isotope("layout");
            });
            $(".gallery-filters").on("click  ", "a.gallery-filter", function (b) {
                b.preventDefault();
                var c = $(this).attr("data-filter"),
                    d = $(this).text();
                a.isotope({
                    filter: c
                });
                $(".gallery-filters a").removeClass("gallery-filter-active");
                $(this).addClass("gallery-filter-active");
            });

            $(".gallery-items").isotope("on", "layoutComplete", function (a, b) {
                var b = a.length;
                $(".num-album").html(b);
            });
            var b = $(".gallery-item").length;
            $(".all-album , .num-album").html(b);
        }
    }
    nrg();
    function postGrid() {
        if ($(".post-items").length) {
            var $grid2 = $(".post-items").isotope({
                singleMode: true,
                columnWidth: ".grid-sizer, .grid-sizer-second, .grid-sizer-three",
                itemSelector: ".post-item",
            });
            $grid2.imagesLoaded(function () {
                $grid2.isotope("layout");
            });
        }
    }
    postGrid();
    function csselem() {
        $(".anim-fw").css({
            height: $(".fw-carousel_hight").outerHeight(true)
        });
        $(".fs-slider-item").css({
            height: $(".fs-slider").outerHeight(true)
        });
        $(".first-slide_wrap").css({
            height: $(".fw-carousel_hight").outerHeight(true)
        });
        $(".height-emulator").css({
            height: $(".main-footer").outerHeight(true)
        });
    }
    csselem();
    //   sliders ------------------
    if ($(".fs-slider").length > 0) {
        var mouseContr2 = $(".fs-slider").data("mousecontrol2");
        var j32 = new Swiper(".fs-slider .swiper-container", {
            preloadImages: false,
            loop: true,
            grabCursor: true,
            speed: 1500,
            spaceBetween: 0,
            effect: "slide",
            mousewheel: mouseContr2,
            parallax: true,
            pagination: {
                el: '.hero-slider-wrap_pagination',
                clickable: true,
            },
            navigation: {
                nextEl: '.hs-button-next',
                prevEl: '.hs-button-prev',
            },
            autoplay: {
                delay:3500,
                disableOnInteraction: false
            }
        });
        var totalSlides = $(".fs-slider .swiper-slide:not(.swiper-slide-duplicate) .bg").length,
            ssnd = $('.fs-slider .swiper-container .swiper-wrapper .swiper-slide:not(.swiper-slide-duplicate)');
        $('.total').html('0' + totalSlides);
        var nxSlide = ssnd.eq(j32.realIndex).next();
        $('.hs_btn_next .hs_btn_wrap_preview .bg').css("background-image", "url(" + nxSlide.find('.bg').attr("data-bg") + ")");
        j32.on('slideChange', function () {
            var csli = j32.realIndex + 1,
                curnum = $('.current');
            curnum.html('0' + csli);
            var nxSlide = ssnd.eq(j32.realIndex).next();
            $('.hs_btn_next .hs_btn_wrap_preview .bg').css("background-image", "url(" + nxSlide.find('.bg').attr("data-bg") + ")");
        });
        j32.on("slideChangeTransitionStart", function () {
            $(".slide-progress").css({
                width: 0,
                transition: "width 0s"
            });
        });
        j32.on("slideChangeTransitionEnd", function () {

            $(".slide-progress").css({
                width: "100%",
                transition: "width 2000ms"
            });
        });
        var totalSlides2 = $(".fs-slider .swiper-slide:not(.swiper-slide-duplicate)").length;
        $('.total_c').html("0" + totalSlides2);
        j32.on('slideChange', function () {
            var csli2 = j32.realIndex + 1,
                curnum2 = $('.current_c'),
                curnumanm2 = $('.hc_counter .current_c');
            curnum2.html("0" + csli2);
        });
        var autobtn = $(".play-pause_slider");
        function autoEnd() {
            autobtn.removeClass("auto_actslider");
            j32.autoplay.stop();
			autobtn.find("span").text("play")
        }
        function autoStart() {
            autobtn.addClass("auto_actslider");
            j32.autoplay.start();
			autobtn.find("span").text("pause")
        }
        autobtn.on("click", function () {
            if (autobtn.hasClass("auto_actslider")) autoEnd();
            else autoStart();
            return false;
        });			
    }
    if ($(".half-carousel-wrap").length > 0) {
        var halfCarousel = new Swiper(".half-carousel .swiper-container", {
            preloadImages: true,
            loop: true,
            centeredSlides: false,
            freeMode: false,
            slidesPerView: 2,
            spaceBetween: 10,
            grabCursor: true,
            mousewheel: false,
            parallax: true,
            speed: 1400,
            navigation: {
                nextEl: '.hcw-cont-next',
                prevEl: '.hcw-cont-prev',
            },
            pagination: {
                el: '.half-carusel_pagination',
                clickable: true,
            },
            breakpoints: {
                768: {
                    slidesPerView: 2,
                },
                640: {
                    slidesPerView: 1,
                },
            }
        });
        var totalSlides3 = $(".half-carousel .swiper-slide:not(.swiper-slide-duplicate)").length;
        $('.total_c2').html("0" + totalSlides3);
        halfCarousel.on('slideChange', function () {
            var csli3 = halfCarousel.realIndex + 1,
                curnum3 = $('.current_c2'),
                curnumanm3 = $('.hc_counter2 .current_c2');
            curnum3.html("0" + csli3);
        });
    }
    if ($(".testimonilas-carousel").length > 0) {
        var ms1 = new Swiper(".testimonilas-carousel .swiper-container", {
            loop: true,
            grabCursor: true,
            autoHeight: false,
            centeredSlides: true,
            slidesPerView: 3,
            spaceBetween: 20,
            speed: 1400,
            navigation: {
                nextEl: '.tc-button-next',
                prevEl: '.tc-button-prev',
            },
            pagination: {
                el: '.tcs-pagination_init',
                clickable: true,
            },
            breakpoints: {
                1064: {
                    slidesPerView: 2,
                    spaceBetween: 10,
                },
                768: {
                    slidesPerView: 1,
                    spaceBetween: 0,
                    autoHeight: true,
                },
            }
        });
        var totalSlides2 = $(".testimonilas-carousel  .swiper-slide:not(.swiper-slide-duplicate)").length;
        $('.ts_total').html('0' + totalSlides2);
        ms1.on('slideChange', function () {
            var csli2 = ms1.realIndex + 1,
                curnum2 = $('.ts_current');
            curnum2.html('0' + csli2);
        });
    }
    if ($(".single-slider").length > 0) {
        var j2 = new Swiper(".single-slider .swiper-container", {
            preloadImages: false,
            slidesPerView: 1,
            spaceBetween: 0,
            loop: true,
            autoHeight: true,
            grabCursor: true,
            mousewheel: false,
            pagination: {
                el: '.ss-slider-pagination',
                clickable: true,
            },
            navigation: {
                nextEl: '.ss-slider-button-next',
                prevEl: '.ss-slider-button-prev',
            },
        });
    }
    if ($(".fw-carousel ").length > 0) {
        var ec = new Swiper(".fw-carousel  .swiper-container", {
            preloadImages: true,
            loop: true,
            centeredSlides: false,
            freeMode: false,
            slidesPerView: "auto",
            spaceBetween: 10,
            grabCursor: true,
            mousewheel: false,
            speed: 1400,
            navigation: {
                nextEl: '.hcw-cont-next',
                prevEl: '.hcw-cont-prev',
            },
            pagination: {
                el: '.half-carusel_pagination',
                clickable: true,
            },
            breakpoints: {

            }
        });
        var totalSlides3 = $(".fw-carousel .swiper-slide:not(.swiper-slide-duplicate)").length;
        $('.total_c2').html("0" + totalSlides3);
        ec.on('slideChange', function () {
            var csli3 = ec.realIndex + 1,
                curnum3 = $('.current_c2'),
                curnumanm3 = $('.hc_counter2 .current_c2');
            curnum3.html("0" + csli3);
        });
        $(".fw-carousel.thumb-contr .swiper-slide:not(.swiper-slide-duplicate) img").each(function () {
            var ccasdc = $(this).attr("src");
            $("<div class='thumb-img'><img src='" + ccasdc + "'></div>").appendTo(".thumbnail-wrap");
        });
        $(".thumb-img").on('click', function () {
            ec.slideTo($(this).index(), 500);
            hideThumbnails();
        });
    }
    var thumbcont = $(".thumbnail-container"),
        thumbItrm = $(".thumb-img"),
        stbtn = $(".show_thumbnails");
    function showThumbnails() {
        thumbcont.addClass("visthum");
        stbtn.removeClass("unvisthum");
        setTimeout(function () {
            $(".thumb-img").addClass("visthumbnails");
        }, 1000);
    }
    function hideThumbnails() {
        $(".thumb-img").removeClass("visthumbnails");
        thumbcont.removeClass("visthum");
        stbtn.addClass("unvisthum");
    }
    stbtn.on("click", function (ec) {
        ec.preventDefault();
        if ($(this).hasClass("unvisthum")) showThumbnails();
        else hideThumbnails();
    });
    if ($(".clients-carousel").length > 0) {
        var ms2 = new Swiper(".clients-carousel .swiper-container", {
            loop: true,
            grabCursor: true,
            autoHeight: false,
            centeredSlides: false,
            slidesPerView: 4,
            spaceBetween: 0,
            speed: 1400,
            mousewheel: false,
            navigation: {
                nextEl: '.cc-next',
                prevEl: '.cc-prev',
            },
            breakpoints: {
                1064: {
                    slidesPerView: 3,
                    spaceBetween: 10,
                },
                768: {
                    slidesPerView: 2,
                    spaceBetween: 0,
                },
                640: {
                    slidesPerView: 1,
                    spaceBetween: 0,
                }
            }
        });
    }
 	
    if ($(".hero-carousel ").length > 0) {
        const totalSlides3 = $(".hero-carousel .swiper-slide").length;
        const heroCarusel = new Swiper(".hero-carousel .swiper-container", {
            preloadImages: false,
            loop: true,
            centeredSlides: true,
            freeMode: false,
            slidesPerView: 3,
            spaceBetween: 10,
            grabCursor: true,
            mousewheel: false,
            parallax: true,
            speed: 1400,
            effect: "slide",
            init: true,
            autoplay: {
                delay: 33332500,
                disableOnInteraction: false
            },
            pagination: {
                el: '.fcwc-pagination',
                clickable: true,
            },
            navigation: {
                nextEl: '.carousel-btn_control-next',
                prevEl: '.carousel-btn_control-prev',
            },
            breakpoints: {
                1268: {
                    slidesPerView: 2
                },
                768: {
                    slidesPerView: 1,
                    centeredSlides: false,
                },
            }
        });
    }	
    //   sliders ------------------
    if ($(".slider-fw").length > 0) {
        $(".slider-fw.thumb-contr .swiper-slide .bg").each(function () {
            var ccasdc3 = $(this).attr("data-bg");
            $("<div class='thumb-img'><img src='" + ccasdc3 + "'></div>").appendTo(".thumbnail-wrap");
        });
        $(".thumb-img").on('click', function () {
            if ($(window).width() > 768) {
                j32.slideTo($(this).index(), 500);
                hideThumbnails();
            }
        });
        var j32 = new Swiper(".slider-fw .swiper-container", {
            preloadImages: false,
            loop: true,
            grabCursor: true,
            slidesPerView: "auto",
            centeredSlides: true,
            speed: 1400,
            spaceBetween: 0,
            effect: "slide",
            mousewheel: false,
            parallax: true,
            pagination: {
                el: '.hc-pag',
                clickable: true,
            },
            autoplay: {
                delay:  3500,
                disableOnInteraction: false
            },
            navigation: {
                nextEl: '.fs-button-next',
                prevEl: '.fs-button-prev',
            }
        });
        var totalSlides = $(".slider-fw  .swiper-slide:not(.swiper-slide-duplicate) .bg").length;
        $('.total_c2').html('0' + totalSlides);
        j32.on('slideChange', function () {
            var csli = j32.realIndex + 1,
                curnum = $('.current_c2');
            curnum.html('0' + csli);
        });

        j32.on("slideChangeTransitionStart", function () {
            $(".slide-progress").css({
                width: 0,
                transition: "width 0s"
            });
        });
        j32.on("slideChangeTransitionEnd", function () {

            $(".slide-progress").css({
                width: "100%",
                transition: "width 2000ms"
            });
        });
        var autobtn = $(".play-pause_slider");
        function autoEnd() {
            autobtn.removeClass("auto_actslider");
            j32.autoplay.stop();
			autobtn.find("span").text("play")
        }
        function autoStart() {
            autobtn.addClass("auto_actslider");
            j32.autoplay.start();
			autobtn.find("span").text("pause")
        }
        autobtn.on("click", function () {
            if (autobtn.hasClass("auto_actslider")) autoEnd();
            else autoStart();
            return false;
        });		
    }	
    if ($(".slideshow-container_wrap").length > 0) {
        var ms1 = new Swiper(".slideshow-container_wrap .swiper-container", {
            preloadImages: false,
            loop: true,
            speed: 1400,
            spaceBetween: 0,
            effect: "fade",
            init: false,
            autoplay: {
                delay: 2500,
                disableOnInteraction: false
            },
            pagination: {
                el: '.fcwc-pagination',
                clickable: true,
            },
        });
        setTimeout(function () {
            ms1.init();
        }, 200);
    }
    $(".accordian__item").on("click", function () {
        $(this)
            .addClass("active")
            .siblings()
            .removeClass("active");
    });
    //   lightGallery------------------
    $(".image-popup , .single-popup-image").lightGallery({
        selector: "this",
        cssEasing: "cubic-bezier(0.25, 0, 0.25, 1)",
        download: false,
        counter: false
    });
    $(".lightgallery").lightGallery({
        selector: ".lightgallery a.popup-image , .lightgallery  a.popgal",
        cssEasing: "cubic-bezier(0.25, 0, 0.25, 1)",
        download: false,
        loop: false,
        counter: false
    });
    $('#html5-videos , .inithtml5video').lightGallery({
        selector: 'this',
        counter: false,
        download: false,
        zoom: false
    });
    var vid_src = $(".popup_video").data("videolink");
    $(".lg-video-object").find("source").attr("src", vid_src);
    //   appear------------------
    $(".stats").appear(function () {
        $(".num").countTo();
    });
    $(".piechart-holder").appear(function () {
        $(this).find(".chart").each(function () {
            var cbc = $(".piechart-holder").attr("data-skcolor");
            $(".chart").easyPieChart({
                barColor: cbc,
                trackColor: "#333",
                scaleColor: false,
                size: "150",
                lineWidth: "45",
                lineCap: "butt",
                animate: 3500,
                onStep: function (a, b, c) {
                    $(this.el).find(".percent").text(Math.round(c));
                }
            });
        });
    });
    var scwrp = $(".header-search-wrap"),
        swlink = $(".show_search-btn");
    function showSearch() {
        scwrp.addClass("vis-search").removeClass("novis_sarch")
        swlink.addClass("scwllink2");
    }
    function hideSearch() {
        scwrp.removeClass("vis-search").addClass("novis_sarch");
        swlink.removeClass("scwllink2");
    }
    swlink.on("click", function () {
        if (scwrp.hasClass("novis_sarch")) showSearch();
        else hideSearch();
    });
    $(".team-info-btn").on("click", function () {
        $(this).parent(".team-photo").find(".team-details").toggleClass("team-det_vis")
        $(this).toggleClass("team-info-btn_cl");
    });
    // Share   ------------------
    $(".sfcs").on("click", function () {
        $(this).toggleClass("vis-buts h");
        $(".fixed-scroll-column-share-container").slideToggle(400);
    });
    $(".share-container").share({
        networks: ['facebook', 'pinterest', 'tumblr', 'twitter', 'linkedin']
    });
	
    var shrcn = $(".share-holder"),
        clsh = $(".share-container a");

    function showShare() {
        shrcn.addClass("visshare").removeClass("isShare");
        setTimeout(function () {
            clsh.each(function (a) {
                var b = $(this);
                setTimeout(function () {
                    b.addClass("vissharea")
                }, 50 * a);
            });
        }, 300);
        $(".showshare").addClass("vis-shar");
    }
    function hideShare() {
        clsh.removeClass("vissharea")
        setTimeout(function () {
            shrcn.removeClass("visshare").addClass("isShare");
        }, 300);
        $(".showshare").removeClass("vis-shar");
    }
    $(".showshare").on("click", function () {
        if ($(".share-holder").hasClass("isShare")) showShare();
        else hideShare();
    });	
    $(".lang-action li a").on('click', function (e) {
        e.preventDefault();
        var thdatlantext = $(this).data("lantext");
        $(".lang-action li a").removeClass("current-lan");
        $(this).addClass("current-lan");
        $(".show-lang span strong").text(thdatlantext);
    });
    //   scrollToFixed ------------------
 
    $(".init-fix-column").scrollToFixed({
        minWidth: 1068,
        marginTop: 110,
        removeOffsets: true,
        limit: function () {
            var a = $(".limit-box").offset().top - $(".init-fix-column").outerHeight(true);
            return a;
        }
    });
    $(".fix-bar-init").scrollToFixed({
        minWidth: 1064,
        zIndex: 112,
        marginTop: 110,
        removeOffsets: true,
        limit: function () {
            const a = $(".limit-box").offset().top - $(".fix-bar-init").outerHeight(true) + 70;
            return a;
        }
    });
    if ($(".fixed-bar").outerHeight(true) < $(".post-container").outerHeight(true)) {
        $(".fixed-bar").addClass("fixbar-action");
        $(".fixbar-action").scrollToFixed({
            minWidth: 1064,
            marginTop: function () {
                var a = $(window).height() - $(".fixed-bar").outerHeight(true) - 120;
                if (a >= 0) return 20;
                return a;
            },
            removeOffsets: true,
            limit: function () {
                var a = $(".limit-box").offset().top - $(".fixed-bar").outerHeight() + 30;
                return a;
            }
        });
    } else $(".fixed-bar").removeClass("fixbar-action");
    //   Video------------------	
    if ($(".video-holder-wrap").length > 0) {
        function videoint() {
            var w = $(".background-vimeo").data("vim"),
                bvc = $(".background-vimeo"),
                bvmc = $(".media-container"),
                bvfc = $(".background-vimeo iframe "),
                vch = $(".video-container");
            bvc.append('<iframe src="//player.vimeo.com/video/' + w + '?background=1"  frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen ></iframe>');
            $(".video-holder").height(bvmc.height());
            if ($(window).width() > 1024) {
                if ($(".video-holder").length > 0)
                    if (bvmc.height() / 9 * 16 > bvmc.width()) {
                        bvfc.height(bvmc.height()).width(bvmc.height() / 9 * 16);
                        bvfc.css({
                            "margin-left": -1 * $("iframe").width() / 2 + "px",
                            top: "-75px",
                            "margin-top": "0px"
                        });
                    } else {
                        bvfc.width($(window).width()).height($(window).width() / 16 * 9);
                        bvfc.css({
                            "margin-left": -1 * $("iframe").width() / 2 + "px",
                            "margin-top": -1 * $("iframe").height() / 2 + "px",
                            top: "50%"
                        });
                    }
            } else if ($(window).width() < 760) {
                $(".video-holder").height(bvmc.height());
                bvfc.height(bvmc.height());
            } else {
                $(".video-holder").height(bvmc.height());
                bvfc.height(bvmc.height());
            }
            vch.css("width", $(window).width() + "px");
            vch.css("height", Number(720 / 1280 * $(window).width()) + "px");
            if (vch.height() < $(window).height()) {
                vch.css("height", $(window).height() + "px");
                vch.css("width", Number(1280 / 720 * $(window).height()) + "px");
            }
        }
        videoint();
    }
    $(".custom-scroll-link").on("click", function () {
        var a = 70;
        if (location.pathname.replace(/^\//, "") == this.pathname.replace(/^\//, "") || location.hostname == this.hostname) {
            var b = $(this.hash);
            b = b.length ? b : $("[name=" + this.hash.slice(1) + "]");
            if (b.length) {
                $("html,body").animate({
                    scrollTop: b.offset().top - a
                }, {
                    queue: false,
                    duration: 1200,
                    easing: "easeInOutExpo"
                });
                return false;
            }
        }
    });
    $(".to-top").on("click", function (a) {
        a.preventDefault();
        $("html, body").animate({
            scrollTop: 0
        }, 800);
        return false;
    });
    //   accordion ------------------
    $(".accordion a.toggle").on("click", function (a) {
        a.preventDefault();
        $(".accordion a.toggle").removeClass("act-accordion");
        $(this).addClass("act-accordion");
        if ($(this).next('div.accordion-inner').is(':visible')) {
            $(this).next('div.accordion-inner').slideUp();
        } else {
            $(".accordion a.toggle").next('div.accordion-inner').slideUp();
            $(this).next('div.accordion-inner').slideToggle();
        }
    });
    var progressBar = $(".js-progress-bar");
    var $window = $(window);
    $window.on("scroll", function () {
        var a = $(document).height();
        var b = $window.height();
        var c = $window.scrollTop();
        var d = c / (a - b) * 100;
        progressBar.css("stroke-dashoffset", 100 - (d));
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
    $(".act-cf").on("click", function (ec) {
        ec.preventDefault();
        showConInfo();
    });
    $(".close-cf , .contact-form-overlay").on("click", function (e) {
        e.preventDefault();
        hideConInfo();
        $("#message").slideUp(200);
        $(".custom-form").find("input[type=text], textarea").val("");
    });
    //   Contact form------------------
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
    //   mailchimp------------------
    $("#subscribe").ajaxChimp({
        language: "eng",
        url: "https://gmail.us1.list-manage.com/subscribe/post?u=1fe818378d5c129b210719d80&amp;id=a2792f681b"
    });
    $.ajaxChimp.translations.eng = {
        submit: "Submitting...",
        0: ' We will be in touch soon!',
        1: ' You must enter a valid e-mail address.',
        2: ' E-mail address is not valid.',
        3: ' E-mail address is not valid.',
        4: ' E-mail address is not valid.',
        5: ' E-mail address is not valid.'
    };
    $("<div class='mob-nav-overlay fs-wrapper'></div>").appendTo("#main");
	 $("#menu-init").menu();
    // Mob Menu------------------
    $(".nav-button-wrap").on("click", function () {
        $(".main-header").toggleClass("vismobmenu");
		$(".mob-nav-overlay").fadeToggle(200);
		$(this).toggleClass("nbw_tb");
    });
    $(".mob-nav-overlay").on("click", function () {
        $(".main-header").removeClass("vismobmenu");
		   $(".nav-button-wrap").removeClass("nbw_tb");
        $(this).fadeOut(200);
    });
	$(".header-search_btn").on("click", function () {
         $(".header-search-wrap").toggleClass("vis-searvvh_wrap");
    });
    $(".sliding-menu li a.nav").parent("li").addClass("submen-dec");
    var $window = $(window);
    $window.on("resize", function () {
        csselem();
    });
    function initscrollnav() {
        //   scrollnav  ------------------
        $(".scroll-init").singlePageNav({
            filter: ":not(.external)",
            updateHash: false,
            offset: 150,
            threshold: 120,
            speed: 1200,
            currentClass: "actscr-link"
        });		
    }
    initscrollnav();
    //   duplicate ------------------	
    $.fn.duplicate = function (a, b) {
        const c = [];
        for (var d = 0; d < a; d++) $.merge(c, this.clone(b).get());
        return this.pushStack(c);
    };
    $("<span class='arrow_dec_dot'></span>").duplicate(9).appendTo(".arrow_dec");
    $("<div class='pl-row'><span class='pl-row-anim'></span></div>").duplicate(25).appendTo(".ds_dec-grid");
    $("<div class='cfid'><span class='cfid-anim'></span></div>").duplicate(9).appendTo(".cf-inner_dec");
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
    function randomItem2() {
        $(".cfid").each(function () {
            for (var i = 0; i < 7; i++) {
                var length2 = $(".cfid-anim").length;
                var random2 = Math.floor(Math.random() * 8);
                $(this).find(".cfid-anim").eq(random2).addClass("cfid-anim-dec-vis");
            }
        });
    }
    randomItem2();
    //   Parallax ------------------
    var b = new Scrollax();
    b.reload();
    b.init();
}
$.fn.duplicate = function (a, b) {
    const c = [];
    for (var d = 0; d < a; d++) $.merge(c, this.clone(b).get());
    return this.pushStack(c);
};
 $(".logo-holder img").clone().appendTo(".top-header-logo");
	 
		
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
    $(".loader-wrap").delay(2500).fadeOut(1)
}
firstload();
$('head').append('<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0">');
document.addEventListener('gesturestart', function (e) {
    e.preventDefault();
});
//   Init All ------------------
$(document).ready(function () {
    initTrustbook();
});