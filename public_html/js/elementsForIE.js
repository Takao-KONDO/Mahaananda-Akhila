// JavaScript Document
/*
*
* 古いInternet Explorerのために、彼らの知らないHTML5要素を作るコード
*
*/
(function() {
	var els = ['section','article','hgroup','header','footer','nav','aside','figure','mark','time','ruby','rt','rp'];
	for (var i=0; i<els.length; i++) {
		document.createElement(els[i]);
	}
})();