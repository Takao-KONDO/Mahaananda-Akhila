#!/usr/local/bin/perl5
#+------------------------------------------------------+
#|【moorr 1.11】                                        |
#|Copyright : 無料素材屋 Moo　～無料素材～              |
#|URL       : http://common1.biz/                       |
#+------------------------------------------------------+
#|※注意事項                                            |
#|１．このスクリプトはフリー素材です。                  |
#|２．このスクリプトを使用したことによって生じる        |
#|    いかなる損害に対して作者は一切の責任を負いません。|
#+------------------------------------------------------+
#use strict;
use CGI;
our$qu = new CGI;
#+------------------------------------------------------+
our$order      = $qu->param('order');
our$control    = $qu->param('control');
our$admin_pass = $qu->param('admin_pass');
our$order_word = $qu->param('order_word');
our$mode_num   = $qu->param('mode_num');
#+------------------------------------------------------+
our$ThisCgi      = 'moorr.cgi';
our$ThisCgiName  = 'moorr';
our$AdminCgi     = 'admin.cgi';
our$AdminCgiName = 'moorr管理';
our$BasicData    = 'data_basic.cgi';
our$LogData      = 'data_log.cgi';
our$MooRRJs      = 'moorr.js';
our$MooRRJs2     = 'moorr2.js';
#+------------------------------------------------------+
our$MooSiteUrl   = 'http://common1.biz/';
our$MooSiteName  = 'moo';
#+------------------------------------------------------+
open(DAT,"<$BasicData");
our@Basic=<DAT>;
close(DAT);
chomp @Basic;
our$AdminPass   = $Basic[0];
our$MakeDire    = $Basic[1]||'.';
our$MakeUrl     = $Basic[2];
our$RssUrl      = $Basic[3];
our$TermMinutes = $Basic[4]||60;
our$Max         = $Basic[5]||10;
our$NewMark     = $Basic[6];
our$NewHours    = $Basic[7];
our$STitleByte  = $Basic[8]||0;
our$TitleByte   = $Basic[9]||30;
our$DescByte    = $Basic[10]||0;
our$TabooTitle  = $Basic[11];
our$TabooUrl    = $Basic[12];
our$TabooDesc   = $Basic[13];
our$Layout1     = $Basic[14];
our$Layout2     = $Basic[15];
our$Layout3     = $Basic[16];
our$MojiCode    = $Basic[17]||1;
our$MaxType     = $Basic[18]||1;
our$MoPerScore  = $Basic[19]||10;
our$TimeOutSeconds = $Basic[20]||3;
#+------------------------------------------------------+
our@Week = ('日','月','火','水','木','金','土');
#+------------------------------------------------------+
print "Content-type:text/html\n\n";
#+------------------------------------------------------+
if($order eq 'pass_set_go'){
	print &header;
	&pass_set_go;
	print &footer;
	exit;
}elsif(!$AdminPass){
	print &header;
	&pass_set;
	print &footer;
	exit;
}
#+------------------------------------------------------+
print &header;
my$flag = 0;
if(!$order && &dekey($admin_pass,$AdminPass) == 1){
	$flag = 1;
}elsif($order && $admin_pass eq $AdminPass){
	$flag = 1;
}
if($flag == 1){
	   if($order eq 'control_room')   {&control_room;}
	elsif($order eq 'basic')          {&basic;}
	elsif($order eq 'basic_go')       {&basic_go;}
	elsif($order eq 'depository')     {&depository;}
	elsif($order eq 'depository_go')  {&depository_go;}
	elsif($order eq 'pass_change')    {&pass_change;}
	elsif($order eq 'pass_change_go') {&pass_change_go;}
	elsif($order eq 'make_rr_js')     {&make_rr_js;}
	elsif($order eq 'tag_view')       {&tag_view;}
	else{&control_room;}
}else{
	&gate('パスワードが違います。');
}
print &footer;
exit;
#+------------------------------------------------------+
sub gate{
	my($mes) = @_;
	print <<"HTM";
<center>
<form action="$AdminCgi" method="post">
パスワード<br /><br />
<input type="password" name="admin_pass" size="15" value=""><br /><br />
<input type="submit" value="ログイン">
</form>
</center>
HTM
}
#+------------------------------------------------------+
sub control_room{
	my($mes) = @_;
	my@menu = (
		['TOP','control',0,[['TOP','control_room']]],
		['設定','set_up',0,[['基本設定','basic'],['CGI以外のファイル置き場','depository'],['パスワード変更','pass_change']]],
		['タグ表\示','tag',0,[['タグ表\示','tag_view']]]
	);
	my($menu_form,%sub_menu_form,$tree);
	for(my$m=0;$m<@menu;$m++){
		my$num = 2;
		  $num = 1 if($control eq $menu[$m][1]);
		$menu_form .= "<a href=\"javascript:control_go('$menu[$m][1]','$menu[$m][3][$menu[$m][2]][1]','$menu[$m][3][$menu[$m][2]][0]',$menu[$m][2]);\" class=\"menu$num\">$menu[$m][0]</a>\n";
		$tree .= "<dt>●$menu[$m][0]</dt>\n";
		for(my$s=0;$s<@{$menu[$m][3]};$s++){
			my$num = 2;
			  $num = 1 if($s == $mode_num);
			$sub_menu_form{$menu[$m][1]} .= "<a href=\"javascript:control_go('$menu[$m][1]','$menu[$m][3][$s][1]','$menu[$m][3][$s][0]',$s);\" class=\"smenu$num\">$menu[$m][3][$s][0]</a>";
			$sub_menu_form{$menu[$m][1]} .= " &nbsp;|&nbsp;\n" if($s < @{$menu[$m][3]}-1);
			$tree .= "<dd><a href=\"javascript:control_go('$menu[$m][1]','$menu[$m][3][$s][1]','$menu[$m][3][$s][0]',$s);\">$menu[$m][3][$s][0]</a></dd>\n";
		}
	}
	$sub_menu_form{$control} = '&nbsp;' if(!$sub_menu_form{$control});
	if(!$mes){
		$mes =<<"HTM";
最初に以下のことをして下さい。
<ul>
<li>設定→基本設定</li>
<li>許可URL設定</li>
<li>タグ表\示で表\示されたタグをアクセス解析したいページに貼\り付ける</li>
</ul>
<br />
 &nbsp; &nbsp; <a href="$ThisCgi" target="_blank">$ThisCgi</a> &nbsp;にアクセスする事でPC・携帯の両方で表\示可能\です。<br /><br />
<dl>
$tree
</dl>
HTM
		my$mo;
		eval "use XML::FeedPP;";
		if(eval "!\${XML::FeedPP::VERSION}"){
			$mo .= "<li><b>XML::FeedPP</b>モジュールがインストールされていないサーバーのようです。<br />この問題は<b>XML::FeedPP</b>をインストールする事によって解決されます。</li>";
		}
		eval "use HTTP::Lite;";
		eval "use LWP::UserAgent;";
		if(eval "!\${HTTP::Lite::VERSION}" && eval "!\${LWP::UserAgent::VERSION}"){
			$mo .= "<li><b>HTTP::Lite</b>モジュールか<b>LWP::UserAgent</b>がインストールされていないサーバーのようです。<br />この問題は<b>HTTP::Lite</b>をインストールする事によって解決されます。</li>";
		}
		$mes .= "<ul>$mo</ul>" if($mo);
	}
	#
	print <<"HTM";
<center>
<table class="lay">
<tr>
 <td class="lay1">
  $menu_form
  <a href="$AdminCgi" style="float:right;margin:5px 8px 0px 0px;padding:1px;color:#511964;">ログアウト</a>
  <div id="fo"></div>
 </td>
</tr>
<tr><td class="lay2">
 <div style="float:left;font-weight:bolder;">$AdminCgiName</div>
 <div style="float:right;">
  <a href="$ThisCgi" target="_blank">$ThisCgi</a> &nbsp; 
  <input type="button" value="データ更新" onclick="data_renew();" />
 </div>
</td></tr>
<tr><td class="lay3">$sub_menu_form{$control}</td></tr>
<tr>
 <td class="lay4">
  <div class="lay4">
   $pri
   $mes
  </div>
 </td>
</tr>
</table>
</center>
<script type="text/javascript">
function data_renew(){
	if(confirm('データ更新します。\\nよろしいですか？')){
		var form = new String();
		form += '<form action="$AdminCgi" method="post" name="renew_form" id="renew_form">';
		form += '<input type="hidden" name="control" value="$control" />';
		form += '<input type="hidden" name="order" value="make_rr_js" />';
		form += '<input type="hidden" name="order_word" value="データ更新" />';
		form += '<input type="hidden" name="mode_num" value="$mode_num" />';
		form += '<input type="hidden" name="admin_pass" value="$AdminPass" />';
		form += '</form>';
		document.getElementById('fo').innerHTML = form;
		document.renew_form.submit();
	}
}
function control_go(control,order,order_word,mode_num){
	var form = new String();
	form += '<form action="$AdminCgi" method="post" name="control_form" id="control_form">';
	form += '<input type="hidden" name="control" value="'+control+'" />';
	form += '<input type="hidden" name="order" value="'+order+'" />';
	form += '<input type="hidden" name="order_word" value="'+order_word+'" />';
	form += '<input type="hidden" name="mode_num" value="'+mode_num+'" />';
	form += '<input type="hidden" name="admin_pass" value="$AdminPass" />';
	form += '</form>';
	document.getElementById('fo').innerHTML = form;
	document.control_form.submit();
}
</script>
HTM
}
#+------------------------------------------------------+
sub pass_set{
	my($mes,$set_pass1,$set_pass2) = @_;
	$mes = "<tr><td colspan=\"2\">$mes</td></tr>" if($mes);
	print <<"HTM";
<center>
<br /><br />
<form action="$AdminCgi" method="post" name="basic_form" id="basic_form">
<table>
$mes
<tr><td class="cap" colspan="2">初期パスワード設定</td></tr>
<tr>
<td class="cap">パスワード</td>
<td><input type="password" name="set_pass1" size="20" value="$set_pass1" /></td>
</tr>
<tr>
<td class="cap">パスワード(確認用)</td>
<td><input type="password" name="set_pass2" size="20" value="$set_pass2" /></td>
</tr>
<tr>
<td class="cap"></td>
<td><input type="submit" value="設定" /></td>
</tr>
</table>
<input type="hidden" name="control" value="control" />
<input type="hidden" name="order" value="pass_set_go" />
<input type="hidden" name="order_word" value="初期パスワード設定" />
<input type="hidden" name="mode_num" value="0" />
</form>
</center>
HTM
}
#+------------------------------------------------------+
sub pass_set_go{
	my$set_pass1 = $qu->param('set_pass1');
	my$set_pass2 = $qu->param('set_pass2');
	if(!$set_pass1){
		&pass_set("パスワードが未記入です。<br />",$set_pass1,$set_pass2);
		exit;
	}elsif(!$set_pass2){
		&pass_set("確認用パスワードが未記入です。<br />",$set_pass1,$set_pass2);
		exit;
	}elsif($set_pass1 ne $set_pass2){
		&pass_set("確認用パスワードが一致しませんでした。<br />",$set_pass1,$set_pass2);
		exit;
	}
	$AdminPass = &enkey($set_pass1);
	&basic_rewrite;
	&pass_set_x($set_pass1,$set_pass2);
	&make_index;
	&control_room("$order_word 完了！<br />");
}
#+------------------------------------------------------+
sub pass_set_x{
	my($set_pass1,$set_pass2) = @_;
	my$div = '<div style="width:226px;_width:246px;height:auto;text-align:left;margin:5px;padding:10px;border:solid 1px #511964;background-color:#ffffff;font-size:12px;line-height:150%;">';
	if(open(DAT,"<$BasicData")){
		my@Basic=<DAT>;
		close(DAT);
		chomp @Basic;
		if(!$Basic[0]){
			&pass_set("$div<b>$BasicData</b>に書き込み出来ませんでした。<b>$BasicData</b>のパーミッションの問題かもしれません。<br /><br />ご利用のサーバーの説明を読んで、適宜<b>$BasicData</b>のパーミッションを変更する事で直る可能\性があります。<br /><br />尚、<b>$BasicData</b>のパーミッションを変更して、初期パスワード設定が上手くいき管理画面が正常に表\示されましたら、<b>data_○○○.cgi</b>に当たるファイル全てのパーミッションも<b>$BasicData</b>と同じパーミッションに設定し直して下さい。<br /><br />【パーミッションの問題でないとしたらサーバーの問題の可能\性が高いです。その場合は、「無料素材屋 Moo」では対応できかねますので、質問はご遠慮下さい。】</div>",$set_pass1,$set_pass2);
			exit;
		}
	}else{
		&pass_set("$div何らかの原因で<b>$BasicData</b>にアクセスできない状態です。<b>$BasicData</b>にアクセスできる状態にしてから再度初期パスワード設定をして下さい。<br /><br />【パーミッションとサーバーの問題が考えられます。サーバーの問題の場合、「無料素材屋 Moo」では対応できかねますので、質問はご遠慮下さい。】</div>",$set_pass1,$set_pass2);
		exit;
	}
}
#+------------------------------------------------------+
sub make_index{
	#ディレクトリ内が見えてしまうサーバー用にダミーでindex.htmlを生成
	my$index = <<"HTM";
<?xml version="1.0" encoding="shift_jis"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="ja" xml:lang="ja">
<head>
<meta http-equiv="content-type" content="text/html; charset=shift_jis" />
<title></title>
</head>
<body>
index.html
</body>
</html>
HTM
	open(DAT,">index.html");
	print DAT $index;
	close(DAT);
}
#+------------------------------------------------------+
sub pass_change{
	my($mes,$change_pass1,$change_pass2) = @_;
	my$form =<<"HTM";
$mes
<form action="$AdminCgi" method="post" name="basic_form" id="basic_form">
<table>
<tr><td class="cap" colspan="2">$order_word</td></tr>
<tr>
<td class="cap">パスワード</td>
<td><input type="password" name="change_pass1" size="20" value="$change_pass1" /></td>
</tr>
<tr>
<td class="cap">パスワード(確認用)</td>
<td><input type="password" name="change_pass2" size="20" value="$change_pass2" /></td>
</tr>
<tr>
<td class="cap"></td>
<td><input type="submit" value="変更" /></td>
</tr>
</table>
<input type="hidden" name="control" value="$control" />
<input type="hidden" name="order" value="pass_change_go" />
<input type="hidden" name="order_word" value="$order_word" />
<input type="hidden" name="mode_num" value="$mode_num" />
<input type="hidden" name="admin_pass" value="$AdminPass" />
</form>
HTM
	&control_room($form);
}
#+------------------------------------------------------+
sub pass_change_go{
	my$change_pass1 = $qu->param('change_pass1');
	my$change_pass2 = $qu->param('change_pass2');
	if(!$change_pass1){
		&pass_change("パスワードが未記入です。<br />",$change_pass1,$change_pass2);
		exit;
	}elsif(!$change_pass2){
		&pass_change("確認用パスワードが未記入です。<br />",$change_pass1,$change_pass2);
		exit;
	}elsif($change_pass1 ne $change_pass2){
		&pass_change("確認用パスワードが一致しませんでした。<br />",$change_pass1,$change_pass2);
		exit;
	}
	$AdminPass = &enkey($change_pass1);
	&basic_rewrite;
	&control_room("$order_word 完了！<br />");
}
#+------------------------------------------------------+
sub basic{
	$RssUrl      =~ s/<>/\n/g;
	$TabooSTitle =~ s/<>/\n/g;
	$TabooSUrl   =~ s/<>/\n/g;
	$TabooTitle  =~ s/<>/\n/g;
	$TabooUrl    =~ s/<>/\n/g;
	$TabooDesc   =~ s/<>/\n/g;
	$RssUrl      =~ s/\&amp;/\&/g;
	$TabooSTitle =~ s/\&amp;/\&/g;
	$TabooSUrl   =~ s/\&amp;/\&/g;
	$TabooTitle  =~ s/\&amp;/\&/g;
	$TabooUrl    =~ s/\&amp;/\&/g;
	$TabooDesc   =~ s/\&amp;/\&/g;
	$Layout1 =~s/<>/\n/g;
	$Layout1 =~s/</&lt;/g;
	$Layout1 =~s/>/&gt;/g;
	$Layout2 =~s/<>/\n/g;
	$Layout2 =~s/</&lt;/g;
	$Layout2 =~s/>/&gt;/g;
	$Layout3 =~s/<>/\n/g;
	$Layout3 =~s/</&lt;/g;
	$Layout3 =~s/>/&gt;/g;
	my%che;
	$che{"moji_code$MojiCode"} = ' checked="checked"';
	$che{"max_type$MaxType"} = ' checked="checked"';
	
	my$form =<<"HTM";
<form action="$AdminCgi" method="post" name="basic_form" id="basic_form">
<table>
<tr>
<td class="cap" colspan="2">$order_word</td></tr>
<tr>
<td class="cap">読み込むRSSのURL</td>
<td><textarea name="rss_url" cols="55" rows="7">$RssUrl</textarea><br /><span style="font-size:8pt;color:#666666;">改行で区切って記入</span></td>
</tr>
<tr>
<td class="cap">ログを更新する時間</td>
<td><input type="text" name="term_minutes" size="5" value="$TermMinutes" /> 分</td>
</tr>
<tr>
<td class="cap">表\示件数</td>
<td>
 <input type="text" name="max" size="5" value="$Max" /> 件 &nbsp; &nbsp; [
 <input type="radio" name="max_type" value="1"$che{'max_type1'} /><span style="font-size:8pt;color:#666666;"> 全て合わせて</span> &nbsp;|
 <input type="radio" name="max_type" value="2"$che{'max_type2'} /><span style="font-size:8pt;color:#666666;"> 各RSS毎に</span> &nbsp;]<br />
 <input type="text" name="mo_per_score" size="5" value="$MoPerScore" /> 件 &nbsp; &nbsp; <span style="font-size:8pt;color:#666666;"> 携帯での1ページ当たりの表\示件数</span>
</td>
</tr>
<tr>
<td class="cap">Newマーク</td>
<td><input type="text" name="new_mark" size="10" value="$NewMark" /></td>
</tr>
<tr>
<td class="cap">Newマーク表\示時間</td>
<td><input type="text" name="new_hours" size="5" value="$NewHours" /> 時間</td>
</tr>
<tr>
<td class="cap">各RSSを取得する時のタイムアウト秒数</td>
<td><input type="text" name="time_out_seconds" size="5" value="$TimeOutSeconds" /> 秒</td>
</tr>
<tr>
<td class="cap">表\示ページの文字コード</td>
<td>
<input type="radio" name="moji_code" value="1"$che{'moji_code1'} /> shift_jis<br />
<input type="radio" name="moji_code" value="2"$che{'moji_code2'} /> utf8<br />
<input type="radio" name="moji_code" value="3"$che{'moji_code3'} /> euc-jp<br />
</td>
</tr>
<tr>
<td class="cap">表\示文字数</td>
<td>
<input type="text" name="stitle_byte" size="5" value="$STitleByte" /> byte
<span style="font-size:8pt;color:#666666;">ブログ名・サイト名</span><br />
<input type="text" name="title_byte" size="5" value="$TitleByte" /> byte
<span style="font-size:8pt;color:#666666;">記事タイトル</span><br />
<input type="text" name="desc_byte" size="5" value="$DescByte" /> byte
<span style="font-size:8pt;color:#666666;">記事の説明文</span><br />
<span style="font-size:8pt;color:#666666;">表\示する場合その文字数を記入</span>
</td>
</tr>
<tr>
<td class="cap">禁止設定</td>
<td>
▼記事タイトル<br /><textarea name="taboo_title" cols="30" rows="5">$TabooTitle</textarea><br />
▼記事URL<br /><textarea name="taboo_url" cols="30" rows="5">$TabooUrl</textarea><br />
▼記事の説明(要約)<br /><textarea name="taboo_desc" cols="30" rows="5">$TabooDesc</textarea><br />
<span style="font-size:8pt;color:#666666;">改行で区切って記入</span>
</td>
</tr>
<tr>
<td class="cap">記事上のレイアウト</td>
<td><textarea name="layout1" cols="50" rows="7">$Layout1</textarea></td>
</tr>
<tr>
<td class="cap">各記事のレイアウト</td>
<td>
<textarea name="layout2" cols="50" rows="12">$Layout2</textarea><br />
&lt;!--date--&gt; ･･･ 日時<br />
&lt;!--new--&gt; ･･･ NEWマーク<br />
&lt;!--site_title--&gt; ･･･ ブログ名・サイト名<br />
&lt;!--site_link--&gt; ･･･ ブログ・サイトURL<br />
&lt;!--title--&gt; ･･･ 記事タイトル<br />
&lt;!--link--&gt; ･･･ 記事URL<br />
&lt;!--description--&gt; ･･･ 記事の説明文<br /><br />

▼日時を細かく設定したい時<br />
 <span style="font-size:8pt;color:#666666;line-height:120%;">
  &nbsp; &nbsp; year ･･･ 年<br />
  &nbsp; &nbsp; month ･･･ 月<br />
  &nbsp; &nbsp; day ･･･ 日<br />
  &nbsp; &nbsp; week ･･･ 曜日<br />
  &nbsp; &nbsp; hour ･･･ 時<br />
  &nbsp; &nbsp; minute ･･･ 分<br />
  &nbsp; &nbsp; second ･･･ 秒<br />
  &nbsp; &nbsp; として、<br />
  &nbsp; &nbsp; &lt;!--date(?????)--&gt;<br />
  &nbsp; &nbsp; の?????の中に適宜書きます。<br />
  &nbsp; &nbsp; <b>例</b><br />
  &nbsp; &nbsp; &lt;!--date(year/month/day (week) hour:minute:second)--&gt;
 </span>
</td>
</tr>
<tr>
<td class="cap">記事下のレイアウト</td>
<td><textarea name="layout3" cols="50" rows="7">$Layout3</textarea></td>
</tr>
<tr>
<td colspan="2"><input type="submit" value="設定" /></td></tr>
</table>
<input type="hidden" name="control" value="$control" />
<input type="hidden" name="order" value="basic_go" />
<input type="hidden" name="order_word" value="$order_word" />
<input type="hidden" name="mode_num" value="$mode_num" />
<input type="hidden" name="admin_pass" value="$AdminPass" />
</form>

HTM

	&control_room($form);
}
#+------------------------------------------------------+
sub basic_go{
	our$RssUrl      = &change_tag($qu->param('rss_url'));
	our$TermMinutes = $qu->param('term_minutes');
	our$Max         = $qu->param('max');
	our$NewMark     = $qu->param('new_mark');
	our$NewHours    = $qu->param('new_hours');
	our$STitleByte  = $qu->param('stitle_byte');
	our$TitleByte   = $qu->param('title_byte');
	our$DescByte    = $qu->param('desc_byte');
	our$TabooTitle  = &change_tag($qu->param('taboo_title'));
	our$TabooUrl    = &change_tag($qu->param('taboo_url'));
	our$TabooDesc   = &change_tag($qu->param('taboo_desc'));
	our$Layout1     = &change_tag($qu->param('layout1'));
	our$Layout2     = &change_tag($qu->param('layout2'));
	our$Layout3     = &change_tag($qu->param('layout3'));
	our$MojiCode    = $qu->param('moji_code');
	our$MaxType     = $qu->param('max_type');
	our$MoPerScore  = $qu->param('mo_per_score');
	our$TimeOutSeconds = $qu->param('time_out_seconds')||3;
	#
	&basic_rewrite;
	&control_room("$order_word 完了！<br />$rssUrl");
}
#+------------------------------------------------------+
sub depository{
	my$form =<<"HTM";
<form action="$AdminCgi" method="post" name="basic_form" id="basic_form">
<table>
<tr><td class="cap">$order_word</td></tr>
<tr>
<td>
 ▼このCGIから見た<b>相対パス</b><br />
 <input type="text" name="make_dire" size="60" value="$MakeDire" /><br /><br />
 ▼http://またはhttps://から始まる<b>絶対パス</b><br />
 <input type="text" name="make_url" size="90" value="$MakeUrl" /><br /><br />
 CGIとHTMLのディレクトリが分離しているサーバをご使用の場合、CGI以外のファイル置き場のディレクトリを相対パス・絶対パスそれぞれ指定して下さい。<br />
 この設定を変更した場合、設定した位置に<b>設定したディレクトリ名</b>のディレクトリを作って下さい。<br /><br />
 <span style="color:#880000;">注意</span> 通常CGIとHTMLのディレクトリが分離していないサーバの場合は設定不要です。
</td>
</tr>
<tr>
<td><input type="submit" value="設定" /></td>
</tr>
</table>
<input type="hidden" name="control" value="$control" />
<input type="hidden" name="order" value="depository_go" />
<input type="hidden" name="order_word" value="$order_word" />
<input type="hidden" name="mode_num" value="$mode_num" />
<input type="hidden" name="admin_pass" value="$AdminPass" />
</form>
HTM
	&control_room($form);
}
#+------------------------------------------------------+
sub depository_go{
	our$MakeDire = $qu->param('make_dire')||'.';
	our$MakeUrl  = $qu->param('make_url');
	$MakeDire =~s/\/$//g;
	$MakeUrl =~s/\/$//g;
	#
	&basic_rewrite;
	&control_room("$order_word 完了！<br />");
}
#+------------------------------------------------------+
sub basic_rewrite{
	open(DAT,"+<$BasicData");
	flock(DAT,2);
	my@Basic=<DAT>;
	truncate(DAT,0);
	seek(DAT,0,0);
	print DAT "$AdminPass\n";
	print DAT "$MakeDire\n";
	print DAT "$MakeUrl\n";
	print DAT "$RssUrl\n";
	print DAT "$TermMinutes\n";
	print DAT "$Max\n";
	print DAT "$NewMark\n";
	print DAT "$NewHours\n";
	print DAT "$STitleByte\n";
	print DAT "$TitleByte\n";
	print DAT "$DescByte\n";
	print DAT "$TabooTitle\n";
	print DAT "$TabooUrl\n";
	print DAT "$TabooDesc\n";
	print DAT "$Layout1\n";
	print DAT "$Layout2\n";
	print DAT "$Layout3\n";
	print DAT "$MojiCode\n";
	print DAT "$MaxType\n";
	print DAT "$MoPerScore\n";
	print DAT "$TimeOutSeconds\n";
	close(DAT);
	#
	my$rss_url      = &arr($RssUrl);
	my$taboo_title  = &arr($TabooTitle);
	my$taboo_url    = &arr($TabooUrl);
	my$taboo_desc   = &arr($TabooDesc);
	my$lay1 = $Layout1;
	my$lay2 = $Layout2;
	my$lay3 = $Layout3;
	$lay1 =~s/<>;//g;
	$lay1 =~s/&lt;/</g;
	$lay1 =~s/&gt;/>/g;
	$lay1 =~s/'/\\'/g;
	$lay2 =~s/<>;//g;
	$lay2 =~s/&lt;/</g;
	$lay2 =~s/&gt;/>/g;
	$lay2 =~s/'/\\'/g;
	$lay3 =~s/<>;//g;
	$lay3 =~s/&lt;/</g;
	$lay3 =~s/&gt;/>/g;
	$lay3 =~s/'/\\'/g;
	my$add_cgi =<<"CGI";
our\@RssUrl      = ($rss_url);
our\@TabooTit    = ($taboo_title);
our\@TabooLin    = ($taboo_url);
our\@TabooDes    = ($taboo_desc);
our\$MakeDire    = '$MakeDire';
our\$MakeUrl     = '$MakeUrl';
our\$TermMinutes = '$TermMinutes';
our\$Max         = '$Max';
our\$NewMark     = '$NewMark';
our\$NewHours    = '$NewHours';
our\$STitleByte  = '$STitleByte';
our\$TitleByte   = '$TitleByte';
our\$DescByte    = '$DescByte';
our\$Layout1     = '$lay1';
our\$Layout2     = '$lay2';
our\$Layout3     = '$lay3';
our\$MojiCode    = '$MojiCode';
our\$MaxType     = '$MaxType';
our\$MoPerScore  = '$MoPerScore';
our\$TimeOutSeconds = '$TimeOutSeconds'||3;
CGI
	#
	open(DAT,"+<$ThisCgi");
	flock(DAT,2);
	my@Cgi=<DAT>;
	truncate(DAT,0);
	seek(DAT,0,0);
	my$cgi = join '',@Cgi;
	$cgi =~s/\#change_start(.*?)\#change_end/\#change_start\n$add_cgi\#change_end/msg;
	print DAT $cgi;
	close(DAT);
}
#+------------------------------------------------------+
sub make_rr_js{
	my$mes  = "<script type=\"text/javascript\" src=\"$ThisCgi?order=get\"></script>\n";
	&control_room("$order_word OK！<br />$mes<br />".&tag."<br />");
}
#+------------------------------------------------------+
sub arr{
	my($str) = @_;
	$str =~s/<>/','/g;
	$str =~s/','$//g;
	$str = "'".$str;
	$str = $str."'";
	return $str;
}
#+------------------------------------------------------+
sub change_tag{
	my($str) = @_;
	$str =~ s/</&lt;/g;
	$str =~ s/>/&gt;/g;
	$str =~ s/\r\n|\r|\n/<>/g;
	return $str;
}
#+------------------------------------------------------+
sub change_number{
	my($str) = @_;
	$str =~ s/０/0/g;
	$str =~ s/１/1/g;
	$str =~ s/２/2/g;
	$str =~ s/３/3/g;
	$str =~ s/４/4/g;
	$str =~ s/５/5/g;
	$str =~ s/６/6/g;
	$str =~ s/７/7/g;
	$str =~ s/８/8/g;
	$str =~ s/９/9/g;
	return $str;
}
#+------------------------------------------------------+
sub tag_view{
	&control_room("$order_word<br />".&tag."<br />");
}
#+------------------------------------------------------+
sub tag{
	my$this_url;
	if($ENV{'SERVER_PORT'} == 443){
		$this_url = 'https://'.$ENV{'HTTP_HOST'}.$ENV{'SCRIPT_NAME'};
	}else{
		$this_url = "http://".$ENV{'HTTP_HOST'}.$ENV{'SCRIPT_NAME'};
	}
	$this_url =~s/$AdminCgi$//g;
	$this_url = "$MakeUrl/" if($MakeDire && $MakeUrl);
	my$tag =<<"HTM";
以下のタグを貼\り付けて下さい。
<textarea name="tag" id="tag" cols="60" rows="5">
&lt;script type="text/javascript" src="$this_url$MooRRJs"&gt;&lt;/script&gt;
&lt;noscript&gt;&lt;a href="$MooSiteUrl"&gt;$ThisCgiName by moo&lt;/a&gt;&lt;/noscript&gt;
</textarea><br />
<input type="button" value="選択" onclick="sele('tag');" />
<script type="text/javascript">
function sele(arg){
	document.getElementById(arg).select();
}
</script>
HTM
	return $tag;
}
#+------------------------------------------------------+
sub ymd_op{
	my($yea,$mon,$day) = @_;
	my($op1,$op2,$op3);
	$op1 = $op2 = $op3 = "<option value=\"\"></option>";
	for(my$x=$yea-2;$x<=$yea+2;$x++){
		my$sel = ' selected="selected"' if($x == $yea);
		$op1 .= "<option value=\"$x\"$sel>$x</option>";
	}
	for(my$x=1;$x<=12;$x++){
		my$sel = ' selected="selected"' if($x == $mon);
		$op2 .= "<option value=\"$x\"$sel>$x</option>";
	}
	for(my$x=1;$x<=31;$x++){
		my$sel = ' selected="selected"' if($x == $day);
		$op3 .= "<option value=\"$x\"$sel>$x</option>";
	}
	return ($op1,$op2,$op3);
}
#+------------------------------------------------------+
sub now{
	my($se,$mi,$ho,$da,$mo,$ye,$we) = localtime(time);
	$ye += 1900;
	$mo += 1;
	return ($ye,$mo,$da);
}
#+------------------------------------------------------+
sub enkey{
	my($str) = @_;
	my($se,$mi,$ho,$da,$mo,$ye,$we) = localtime(time);
	my(@token) = ('0'..'9','A'..'Z','a'..'z');
	my$salt  = $token[(time | $$) % scalar(@token)];
	  $salt .= $token[($se+$mi*60+$ho*60*60) % scalar(@token)];
	return crypt($str,$salt);
}
#+------------------------------------------------------+
sub dekey{
	my($passwd1,$passwd2) = @_;#パスワード,暗号化パスワード
	if(crypt($passwd1,$passwd2) eq $passwd2){
		return 1;
	}else{
		return 2;
	}
}
#+------------------------------------------------------+
sub header{
	my$header =<<"HTM";
<?xml version="1.0" encoding="Shift_JIS"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="ja" xml:lang="ja">
<head>
<meta http-equiv="content-type" content="text/html; charset=shift_jis" />
<title>$AdminCgiName</title>
<meta http-equiv="Content-Script-Type" content="text/javascript" />
<meta http-equiv="Content-Style-Type" content="text/css" />
<style type="text/css"><!--
html{overflow:scroll-y;}
body{
 margin:10px 0px 20px 0px;
 background-color:#d7c7eb;
}
table{
 border-collapse:collapse;
 margin:3px 0px 10px 0px;
 background-color:#ffffff;
}
td,td.cap{
 font-size:10pt;
 padding:3px 4px 3px 4px;
 border:solid 1px #511964;
}
td.cap{
 font-weight:bolder;
 background-color:#a06da5;
 color:#ffffff;
}
td.no{
 font-size:10pt;
 padding:0px 5px 0px 5px;
 border:none;
 background-color:transparent;
 color:#000000;
 vertical-align:top;
 font-size:8pt;
 line-height:110%;
}
table.lay{
 width:600px;
 border-collapse:collapse;
 margin:10px;
 padding:0px;
 background-color:transparent;
 border:none;
}
td.lay1,td.lay2,td.lay3,td.lay4{
 font-size:80%;
 border:none;
 vertical-align:top;
 text-align:left;
 line-height:150%;
}
td.lay1{
 padding:10px 5px 0px 0px;
 background-color:transparent;
}
td.lay2,td.lay3,td.lay4{
 background-color:#ffffff;
 border-style:solid;
 border-color:#511964;
}
td.lay2{
 padding:3px 10px;
 border-width:3px 3px 1px 3px;
 background-color:#cdbadb;
 font-size:85%;
 color:#3e084c;
}
td.lay3{
 padding:3px 10px;
 border-width:1px 3px 1px 3px;
 background-color:#e9e0f8;
}
td.lay4{
 padding:0px 0px;
 border-width:1px 3px 3px 3px;
}
div.lay4{
 height:500px;
 _height:520px;
 overflow:auto;
 padding:10px 10px;
}
a:link.menu1,a:visited.menu1,a:hover.menu1,a:link.menu2,a:visited.menu2,a:hover.menu2{
 float:left;
 border-style:solid;
 border-color:#511964;
 border-width:3px 3px 0px 3px;
 margin:3px 3px 0px 3px;
 width:auto;
 padding:3px 6px 1px 6px;
 font-size:10pt;
 text-align:center;
 text-decoration:none;
}
a:link.menu1,a:visited.menu1,a:hover.menu1{
 color:#000000;
 background-color:#ffffff;
}
a:link.menu2,a:visited.menu2,a:hover.menu2{
 color:#ffffff;
 background-color:#a06da5;
}
a:link.smenu1,a:visited.smenu1,a:hover.smenu1,a:link.smenu2,a:visited.smenu2,a:hover.smenu2{
 color:#000000;
}
a:link.smenu1,a:visited.smenu1,a:hover.smenu1{
 font-weight:bolder;
}
ul{
 list-style:square;
 font-size:10pt;
 line-height:160%;
 margin:5px 5px 5px 20px;
 padding:5px 5px;
}
li{
 margin:1px 1px;
 padding:2px 1px;
}
dl{
 list-style:square;
 font-size:10pt;
 line-height:120%;
 margin:5px 5px 5px 20px;
 padding:5px 5px;
}
dt{
 margin:7px 1px 1px 1px;
 padding:1px 1px;
 font-weight:bolder;
}
dd{
 margin:1px 1px 1px 16px;
 padding:1px 1px;
 line-height:110%;
}
textarea{
 overflow-x:none;
 overflow-y:auto;
}
--></style>
</head>
<body>
HTM
	return $header;
}
#+------------------------------------------------------+
sub footer{
	my$footer =<<"HTM";
</body>
</html>
HTM
	return $footer;
}
#+------------------------------------------------------+
