jQuery(document).ready(function () {
"use strict";
  // PageTopヘッダ分ずらす
  var headMargin = 20 ;

	var nowURL = window.location.href ;
		// スクロール速度
  var sSpeed = 500;

  // ページ内リンクのスクロール
  var sAnchors = jQuery("a[href*='#']") ;
  sAnchors.each( function() {
    var sThat = jQuery(this) ;
    var sHref = sThat.attr("href") ;
      // もしhref属性の先頭が#ならページ内リンク
    if (sHref.match(/^#/)) {
      sThat.click( function() {
      var sTarget = $((sHref === "#" ||  sHref === "#wrapper") ? 'html' : sHref );
      var sPosition = sTarget.offset().top;
      var sPositionShift = sPosition - headMargin ;
      jQuery('body,html').animate({scrollTop:sPositionShift}, sSpeed, 'swing' );
      return false;
      });
      // #で始まらないが同一ページを差すリンクのとき
    } else {
    var nDest = nowURL.split("#");
    var nDestPage = nDest[0];
    var sDest = sHref.split("#");
    var sDestPage = sDest[0];
      if(nDestPage === sDestPage ){
				sThat.click( function() {
					var sTargetTxt = sDest[1];
          var sTarget = $((sTargetTxt === "" || sTargetTxt === "wrapper") ? 'html' : '#'+sTargetTxt );
          var sPosition = sTarget.offset().top;
          var sPositionShift = sPosition - headMargin ;
          jQuery('body,html').animate({scrollTop:sPositionShift}, sSpeed, 'swing' );
          return false;
        });
      }
		}
  });

	// 別ページ・外部ページから来たときのページ内リンクのスクロール
	if(nowURL.match(/#/)) {
		var sDest = nowURL.split("#");
		var sTarget = sDest[1];
		var sPosition = $("#"+sTarget).offset().top;
		var sPositionShift = sPosition - headMargin ;
		jQuery('body,html').animate({scrollTop:sPositionShift }, sSpeed, 'swing' );
	}

});