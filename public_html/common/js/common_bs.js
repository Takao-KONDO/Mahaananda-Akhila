// JavaScript Document

$(function(){
    'use strict';
    //カラム同士の高さ調節
//    if($(window).width() >= 992){ //本来992
//        $('.gnav, .contents').autoHeight();
//    }
//    $(window).on("resize orientationchange",function(){
//        if($(window).width() >= 992){ //本来992
//            $('.gnav, .contents').autoHeight();
//        } else {
//            $('.gnav, .contents').removeAttr('style');
//        }
//    });
    
    
    //メニューのトグル
    var toggleBtn = $('#toggleBtn .btnLine');
    var gnavArea = $('#gnavArea');
	var toggleIcon01 = $('#toggleBtn .glyphicon.glyphicon-menu-hamburger');
	var toggleIcon02 = $('#toggleBtn .glyphicon.glyphicon-remove');
    var overFlag = '';
    toggleBtn.on("click", function(){
        gnavArea.toggleClass("show");
		toggleIcon01.toggleClass("hide");
		toggleIcon02.toggleClass("feed");
    });
    $('#gnavArea, #toggleBtn .btnLine').hover(function(){
             overFlag = true;
    }, function(){
             overFlag = false;
    });
	/*
    $('body').click(function() {
        if (overFlag === false && gnavArea.css('display') === 'block' ) {
                //gnavArea.removeClass("show");
        }
    });
	*/
    $(window).on("resize orientationchange", function () {
        if(window.innerWidth >= 992) {
            gnavArea.addClass("show");
			toggleIcon01.addClass("hide");
			toggleIcon02.addClass("feed");
        } else if (window.innerWidth < 992) {
            //gnavArea.removeClass("show");
			//toggleIcon01.removeClass("hide");
			//toggleIcon02.removeClass("feed");
        }
    });
	$(window).on("scroll", function () {
        if(window.innerWidth >= 992) {
            gnavArea.addClass("show");
			toggleIcon01.addClass("hide");
			toggleIcon02.addClass("feed");
        } else if (window.innerWidth < 992) {
            //gnavArea.removeClass("show");
			//toggleIcon01.removeClass("hide");
			//toggleIcon02.removeClass("feed");
        }
    });



    //トップへ戻るボタン

    var topBtn = $('#topagetop');
    topBtn.hide();
    $(window).scroll(function(){
        if ($(this).scrollTop() > 100) {
            topBtn.fadeIn();
        } else {
            topBtn.fadeOut();
        }
    });
    topBtn.click(function(){
        $('body,html').animate({
            scrollTop: 0
        }, 'slow');
        return false;
    });

});

