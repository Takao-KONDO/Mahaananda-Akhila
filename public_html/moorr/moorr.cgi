#!/usr/local/bin/perl5
#+------------------------------------------------------+
#|Åymoorr 1.11Åz                                        |
#|Copyright : ñ≥óøëfçﬁâÆ MooÅ@Å`ñ≥óøëfçﬁÅ`              |
#|URL       : http://common1.biz/                       |
#+------------------------------------------------------+
#|Å¶íçà”éñçÄ                                            |
#|ÇPÅDÇ±ÇÃÉXÉNÉäÉvÉgÇÕÉtÉäÅ[ëfçﬁÇ≈Ç∑ÅB                  |
#|ÇQÅDÇ±ÇÃÉXÉNÉäÉvÉgÇégópÇµÇΩÇ±Ç∆Ç…ÇÊÇ¡Çƒê∂Ç∂ÇÈ        |
#|    Ç¢Ç©Ç»ÇÈëπäQÇ…ëŒÇµÇƒçÏé“ÇÕàÍêÿÇÃê”îCÇïâÇ¢Ç‹ÇπÇÒÅB|
#+------------------------------------------------------+
#use strict;
use CGI;
our$qu = new CGI;
#+------------------------------------------------------+
our$order = $qu->param('order');
#+------------------------------------------------------+
our$ThisCgi      = 'moorr.cgi';
our$ThisCgiName  = 'moorr';
our$AdminCgi     = 'admin.cgi';
our$AdminCgiName = 'moorrä«óù';
our$BasicData    = 'data_basic.cgi';
our$LogData      = 'data_log.cgi';
our$MooRRJs      = 'moorr.js';
our$MooRRJs2     = 'moorr2.js';
#+------------------------------------------------------+
our$MooSiteUrl   = 'http://common1.biz/';
our$MooSiteName  = 'moo';
#+------------------------------------------------------+
use XML::FeedPP;
#+------------------------------------------------------+
#change_start
our@RssUrl      = ('http://naadeszvara.namaste.jp/feed/');
our@TabooTit    = ('PR');
our@TabooLin    = ('');
our@TabooDes    = ('');
our$MakeDire    = '.';
our$MakeUrl     = '';
our$TermMinutes = '30';
our$Max         = '20';
our$NewMark     = 'New';
our$NewHours    = '72';
our$STitleByte  = '0';
our$TitleByte   = '100';
our$DescByte    = '200';
our$Layout1     = '<div style="width:520px;_width:500px;height:120px;padding:10px;margin:0px;border:solid 1px #aaaaaa;overflow-y:auto;"><><table><><tr><td style="font-weight:bolder;" colspan="2">What\'s newÅI</td></tr>';
our$Layout2     = '<tr><><td><!--date--></td><><td><a href="<!--link-->" target="_blank"><!--title--></a></td><></tr>';
our$Layout3     = '</table></div>';
our$MojiCode    = '2';
our$MaxType     = '1';
our$MoPerScore  = '20';
our$TimeOutSeconds = '15'||3;
#change_end
$Layout1 =~s/<>//g;
$Layout1 =~s/'/\\'/g;
$Layout2 =~s/<>//g;
$Layout2 =~s/'/\\'/g;
$Layout3 =~s/<>//g;
$Layout3 =~s/'/\\'/g;
$NewMark =~s/'/\\'/g;
our$LastDateNum = 20130318002738;
our$MobileAgent = 'DoCoMo|KDDI|DDIPOKET|UP.Browser|J-PHONE|Vodafone|SoftBank';
our$DocomoAgent = 'DoCoMo';
#+------------------------------------------------------+
if($ENV{'HTTP_USER_AGENT'} =~/$MobileAgent/){#ågë—
	&mobile;
}else{
	if($order eq 'get'){
		print "Content-type:text/html\n\n";
		&rss_read;
	}else{
		&pc;
	}
}
#else{
#	print "Content-type:text/html\n\n";
#	&rss_read;
#}
exit;
#+------------------------------------------------------+
sub rss_read{
	$order = $_[0] if(!$order);
	my%Mon = ('Jan'=>1,'Feb'=>2,'Mar'=>3,'Apr'=>4,'May'=>5,'Jun'=>6,'Jul'=>7,'Aug'=>8,'Sep'=>9,'Oct'=>10,'Nov'=>11,'Dec'=>12);
	my@get_rss;
	my$get_flag = 0;
	if($order eq 'get'){
		my$error_mes;
		foreach my$url(@RssUrl){
			my$feed;
			eval{
				local $SIG{ALRM} = sub {die "timeout"};
				alarm $TimeOutSeconds;
				$feed = XML::FeedPP->new($url);
			};
			alarm 0;
			$error_mes .= "$@";
			next if($@);
			my$stitle = $feed->title();
			my$slink  = $feed->link();
			foreach my$item($feed->get_item()){
				my$title = $item->title();
				my$link  = $item->link();
				my$date  = $item->pubDate();
				my$des   = $item->description();
				if($date =~/^(\d\d\d\d)-(\d\d)-(\d\d)T(\d\d):(\d\d):(\d\d)(.*?)$/){
					$date =~s/^(\d\d\d\d)-(\d\d)-(\d\d)T(\d\d):(\d\d):(\d\d)(.*?)$/$1$2$3$4$5$6/;
				}elsif($date =~/^(\d\d\d\d)-(\d\d)-(\d\d)T(\d\d):(\d\d)(.*?)$/){
					$date =~s/^(\d\d\d\d)-(\d\d)-(\d\d)T(\d\d):(\d\d)(.*?)$/$1$2$3$4$5/;
				}elsif($date =~/^(\d\d\d\d)-(\d\d)-(\d\d) (\d\d):(\d\d):(\d\d)(.*?)$/){
					$date =~s/^(\d\d\d\d)-(\d\d)-(\d\d) (\d\d):(\d\d):(\d\d)(.*?)$/$1$2$3$4$5$6/;
				}
				push @get_rss,"$date<>$title<>$link<>$des<>$stitle<>$slink<>$url<>\n";
			}
		}
		if($error_mes){
			print "document.write('error<br />$error_mes');\n";
			$get_flag = 1;
		}
	}else{
		open(DAT,"<$LogData");
		@get_rss=<DAT>;
		close(DAT);
	}
	#
	my$taboo_tit  = &taboouens(@TabooTit);
	my$taboo_lin  = &taboolins(@TabooLin);
	my$taboo_des  = &taboouens(@TabooDes);
	#
	my@get_rsss = sort{(split(/<>/,$b))[0]<=>(split(/<>/,$a))[0]}@get_rss;
	my$add_js;
	my$co = 0;
	my%count;
	my@rss;
	foreach my$rss(@get_rsss){
		my($date,$title,$link,$des,$stitle,$slink,$url) = split(/<>/,$rss);
		next if($MaxType == 2 && $count{$url} >= $Max);
		#
		my$e_title  = &en($title);
		my$e_des    = &en($des);
		next if($e_title  =~/$taboo_tit/ig);
		next if($link     =~/$taboo_lin/ig);
		next if($e_des    =~/$taboo_des/ig);
		$date = sprintf("%04d/%02d/%02d %02d:%02d:%02d",
			substr($date,0,4),
			substr($date,4,2),
			substr($date,6,2),
			substr($date,8,2),
			substr($date,10,2),
			substr($date,12,2)
		);
		$stitle = &text_byte_shape(&utf_dec($stitle),$STitleByte);
		$title  = &text_byte_shape(&utf_dec($title) ,$TitleByte);
		$des    = &text_byte_shape(&utf_dec($des)   ,$DescByte);
		
		$stitle =~s/\'/\\'/g;
		$title  =~s/\'/\\'/g;
		$des    =~s/\'/\\'/g;
		
		push @rss,"$date<>$title<>$link<>$des<>$stitle<>$slink<>\n";
		$add_js .= "['$date','$title','$link','$des ','$stitle','$slink'],";
		#
		$count{$url}++;
		$co++;
		last if($MaxType != 2 && $co >= $Max);
	}
	$add_js =~s/\,$//g;
	#
	if($order eq 'get' && $get_flag == 0 && scalar @rss > 0){#
		open(DAT,">$LogData");
		print DAT @rss;
		close(DAT);
		my($se,$mi,$ho,$da,$mo,$ye,$we) = localtime(time);
		my$last_date_num = sprintf("%04d%02d%02d%02d%02d%02d",$ye+1900,$mo+1,$da,$ho,$mi,$se);
		&make_js($last_date_num,$add_js);
	}
}
#+------------------------------------------------------+
sub mobile{
	if($ENV{'HTTP_USER_AGENT'} =~/$DocomoAgent/){#Docomo
		print "Content-Type: application/xhtml+xml\n\n";
		print <<"HTM";
<?xml version="1.0" encoding="Shift_JIS"?>
<!DOCTYPE html PUBLIC "-//i-mode group (ja)//DTD XHTML i-XHTML(Locale/Ver.=ja/2.0) 1.0//EN" "i-xhtml_4ja_10.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="ja" xml:lang="ja">
<head>
<meta http-equiv="content-type" content="application/xhtml+xml; charset=Shift_JIS" />
<title>$title</title>
<style type="text/css">
<![CDATA[
a:link{color:$MainColor;}
a:focus{color:#ffffff;background-color:$MainColor;}
a:visited{color:$MainColor;}
]]>
</style>
</head>
<body>
HTM
	}else{
		print "Content-type: text/html\n\n";
		print <<"HTM";
<?xml version="1.0" encoding="Shift_JIS"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="ja" xml:lang="ja">
<head>
<meta http-equiv="content-type" content="text/html; charset=shift_jis" />
<title>$title</title>
<meta http-equiv="Content-Style-Type" content="text/css" />
<meta http-equiv="Content-Script-Type" content="text/javascript" />
<style type="text/css">
a:link{color:$MainColor;}
a:focus{color:$MainColor;}
a:visited{color:$MainColor;}
</style>
</head>
<body>
HTM
	}
	
	open(DAT,"<$LogData");
	my@rss=<DAT>;
	close(DAT);
	
	my$Page = $qu->param('page');
	my$pa = int(@rss/$MoPerScore)+1;
	  $pa = int(@rss/$MoPerScore) if(@rss % $MoPerScore == 0);
	my$p_op;
	for(my$p=1;$p<=$pa;$p++){
		my$sel = ' selected="selected"' if($Page == $p);
		$p_op .= "<option value=\"$p\"$sel>$p</option>";
	}
	my$this_cgi_url = &this_cgi_url;
	
	my@Week = ('ì˙','åé','âŒ','êÖ','ñÿ','ã‡','ìy');
	print "<div style=\"text-align:center;\">What's newÅI</div><hr />";
	print "<span style=\"font-size:small;\">";
	print "<ul>";
	for(my$r=$Page*$MoPerScore-$MoPerScore;$r<$Page*$MoPerScore;$r++){
		my($date,$title,$link,$des,$stitle,$slink) = split(/<>/,$rss[$r]);
		last if(!$date);
		my$yea = substr($date,0,4);
		my$mon = substr($date,5,2);
		my$day = substr($date,8,2);
		my$hou = substr($date,11,2);
		my$sec = substr($date,17,2);
		my$ymd = substr($date,0,10);
		my$hm  = substr($date,11,5);
		&leap($yea);
		my$we = &what_week($yea,$mon,$day);
		print "<li>";
		#print "<img src=\"$NewMark\" \/>";
		print "<a href=\"$link\">$title</a><br />";
		print "$des Åc<br />" if($des);
		print "<div style=\"text-align:right;\">$ymd\($Week[$we]\)$hm</div>";
		print "</li>";
	}
	print "</ul>";
	print "</span>";
	print "<hr />";
	if($pa > 1){
		print "<div style=\"text-align:center;\"><form action=\"$this_cgi_url\" method=\"post\">";
		print "<select name=\"page\">$p_op</select>";
		print "<input type=\"submit\" value=\"GO\" />";
		print "</form></div><hr />";
	}
	print "<div style=\"text-align:center;\"><span style=\"font-size:small;\"><a href=\"$MooSiteUrl\">$ThisCgiName by $MooSiteName</a></span></div>";
	print $view;
	
	&this_cgi_rewrite;
}
#+------------------------------------------------------+
sub pc{
	my@Week = ('ì˙','åé','âŒ','êÖ','ñÿ','ã‡','ìy');
	my$PcLayout1 = <<"HTM";
<table style="text-align:left;">
<tr><td style="font-weight:bolder;text-align:center;" colspan="3">What's newÅI</td></tr>
HTM
	my$PcLayout2 = <<"HTM";
<tr>
<td style="font-size:12px;line-height:150%;"><!--date(year/month/day(week) hour:minute:second)--></td>
<td style="font-size:12px;line-height:150%;"><!--new--></td>
<td style="font-size:12px;line-height:150%;"><a href="<!--link-->" target="_blank"><!--title--></a></td>
</tr>
HTM
	my$PcLayout3 = <<"HTM";
</table>
HTM
	
	open(DAT,"<$LogData");
	my@rss=<DAT>;
	close(DAT);
	my($se,$mi,$ho,$da,$mo,$ye,$we) = localtime(time);
	my$n_date_num = sprintf("%04d%02d%02d%02d%02d%02d",$ye+1900,$mo+1,$da,$ho,$mi,$se);
	my$pt = $n_date_num - ($NewHours*10000);
	my$view;
	for(my$r=0;$r<@rss;$r++){
		my($date,$title,$link,$des,$stitle,$slink) = split(/<>/,$rss[$r]);
		my$yea = substr($date,0,4);
		my$mon = substr($date,5,2);
		my$day = substr($date,8,2);
		my$hou = substr($date,11,2);
		my$min = substr($date,14,2);
		my$sec = substr($date,17,2);
		my$ymd = substr($date,0,10);
		my$hm  = substr($date,11,5);
		&leap($yea);
		my$we = &what_week($yea,$mon,$day);
		
		my$lay = $PcLayout2;
		my$date_format = $2 if($lay =~/(.*)<!--date\((.*?)\)-->(.*)/);
		if($lay =~/(.*)<!--date\((.*?)\)-->(.*)/){
			$date_format = $2;
			$date_format =~s/year/$yea/g;
			$date_format =~s/month/$mon/g;
			$date_format =~s/day/$day/g;
			$date_format =~s/week/$Week[$we]/g;
			$date_format =~s/hour/$hou/g;
			$date_format =~s/minute/$min/g;
			$date_format =~s/second/$sec/g;
			$lay =~s/<!--date\((.*?)\)-->/$date_format/g;
		}elsif($lay =~/<!--date-->/){
			$lay =~s/<!--date-->/$ymd\($Week[$we]\)$hm/g;
		}
		$lay =~s/<!--site_title-->/$stitle/g;
		$lay =~s/<!--site_link-->/$slink/g;
		$lay =~s/<!--title-->/$title/g;
		$lay =~s/<!--link-->/$link/g;
		$lay =~s/<!--description-->/$des/g;
		$date =~s/\/| |://g;
		$lay =~s/<!--new-->/<img src="$NewMark" \/>/g if($date > $pt);
		$view .= $lay;
	}
	print <<"HTM";
Content-type: text/html\n\n
<?xml version="1.0" encoding="Shift_JIS"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="ja" xml:lang="ja">
<head>
<meta http-equiv="content-type" content="text/html; charset=shift_jis" />
<title>çXêVèÓïÒ</title>
<meta http-equiv="Content-Style-Type" content="text/css" />
<style type="text/css"><!--
--></style>
</head>
<body>
<center>
$PcLayout1
$view
$PcLayout3
<div style="margin:50px 0px 0px 0px;font-size:11px;"><a href="$MooSiteUrl">$ThisCgiName by $MooSiteName</a></div>
</center>
</body>
</html>
HTM
	&this_cgi_rewrite;
}
#+------------------------------------------------------+
sub this_cgi_rewrite{
	my($se,$mi,$ho,$da,$mo,$ye,$we) = localtime(time);
	my$date_num = sprintf("%04d%02d%02d%02d%02d%02d",$ye+1900,$mo+1,$da,$ho,$mi,$se);
	if($date_num > $LastDateNum+($TermMinutes*60)){
		open(DAT,"+<$ThisCgi");
		flock(DAT,2);
		my@Cgi=<DAT>;
		truncate(DAT,0);
		seek(DAT,0,0);
		my$cgi = join '',@Cgi;
		$cgi =~s/our\$LastDateNum \= (\d{14})\;/our\$LastDateNum \= $date_num\;/ms;
		print DAT $cgi;
		close(DAT);
		&rss_read('get');
	}
}
#+------------------------------------------------------+
sub what_week{
	my($yea,$mon,$day) = @_;
	if($mon < 3){
		$mon += 12;
		$yea --;
	}
	my$wn = ($yea + int($yea / 4) - int($yea / 100) + int($yea / 400) + int((13 * $mon + 8) / 5) + $day) % 7;
	return $wn;
}
#+------------------------------------------------------+
sub leap{
	my($yea) = @_;
	my$leap = 28;
	if(($yea % 4 == 0 && $yea % 100 != 0) || $yea % 400 == 0){
	    $leap = 29;
	}
	$Days[1] = $leap;
}
#+------------------------------------------------------+
sub make_js{
	my($last_date_num,$add_js) = @_;
	my$this_cgi_url = &this_cgi_url;
	my$this_url;
	if($ENV{'SERVER_PORT'} == 443){
		$this_url = 'https://'.$ENV{'HTTP_HOST'}.$ENV{'SCRIPT_NAME'};
	}else{
		$this_url = "http://".$ENV{'HTTP_HOST'}.$ENV{'SCRIPT_NAME'};
	}
	$this_url =~s/$ThisCgi$//g;
	$this_url = "$MakeUrl/" if($MakeUrl);
	#
	my$js = <<"EOM";
/*
+------------------------------------------------------+
|ÅymoorrÅz                                             |
|Copyright : ñ≥óøëfçﬁâÆ MooÅ@Å`ñ≥óøëfçﬁÅ`              |
|URL       : http://common1.biz/                       |
+------------------------------------------------------+
|Å¶íçà”éñçÄ                                            |
|ÇPÅDÇ±ÇÃÉXÉNÉäÉvÉgÇÕÉtÉäÅ[ëfçﬁÇ≈Ç∑ÅB                  |
|ÇQÅDÇ±ÇÃÉXÉNÉäÉvÉgÇégópÇµÇΩÇ±Ç∆Ç…ÇÊÇ¡Çƒê∂Ç∂ÇÈ        |
|    Ç¢Ç©Ç»ÇÈëπäQÇ…ëŒÇµÇƒçÏé“ÇÕàÍêÿÇÃê”îCÇïâÇ¢Ç‹ÇπÇÒÅB|
+------------------------------------------------------+
*/
var now = new Date();
var num = Math.floor(now.getTime()/1000);
document.write('<script type="text/javascript" src="$this_url$MooRRJs2?'+Math.floor(now.getTime()/1000)+'"></script>');
EOM
	if($MojiCode != 1){
		my$code;
		if(eval "use Encode;\${Encode::VERSION}"){
			   if($MojiCode == 2){$code = 'utf8';}
			elsif($MojiCode == 3){$code = 'euc-jp';}
			$code = 'utf8';
			eval "Encode::from_to(\$js,'shiftjis','$code');";
		}elsif(eval "use Jcode;\${Jcode::VERSION}"){
			   if($MojiCode == 2){$code = 'utf8';}
			elsif($MojiCode == 3){$code = 'euc';}
			$code = 'utf8';
			eval "\$js = Jcode->new(\$js,'sjis')->$code();";
		}
	}
	open(DAT,">$MakeDire/$MooRRJs");
	print DAT $js;
	close(DAT);
	#
	my$js = <<"EOM";
/*
+------------------------------------------------------+
|ÅymoorrÅz                                             |
|Copyright : ñ≥óøëfçﬁâÆ MooÅ@Å`ñ≥óøëfçﬁÅ`              |
|URL       : http://common1.biz/                       |
+------------------------------------------------------+
|Å¶íçà”éñçÄ                                            |
|ÇPÅDÇ±ÇÃÉXÉNÉäÉvÉgÇÕÉtÉäÅ[ëfçﬁÇ≈Ç∑ÅB                  |
|ÇQÅDÇ±ÇÃÉXÉNÉäÉvÉgÇégópÇµÇΩÇ±Ç∆Ç…ÇÊÇ¡Çƒê∂Ç∂ÇÈ        |
|    Ç¢Ç©Ç»ÇÈëπäQÇ…ëŒÇµÇƒçÏé“ÇÕàÍêÿÇÃê”îCÇïâÇ¢Ç‹ÇπÇÒÅB|
+------------------------------------------------------+
*/
//----------------------------------------------------//
var rss  = new Array($add_js);
var term = $TermMinutes;
var lay1 = new String('$Layout1');
var lay2 = new String('$Layout2');
var lay3 = new String('$Layout3');
var Week = new Array('ì˙','åé','âŒ','êÖ','ñÿ','ã‡','ìy');

var last_date = new String('$last_date_num');
var last_yea = last_date.slice(0,4);
var last_mon = last_date.slice(4,6);
var last_day = last_date.slice(6,8);
var last_hou = last_date.slice(8,10);
var last_min = last_date.slice(10,12);
var last_sec = last_date.slice(12,14);

var last_time = new Date();
last_time.setFullYear(last_yea);
last_time.setMonth(last_mon-1);
last_time.setDate(last_day);
last_time.setHours(last_hou);
last_time.setMinutes(last_min);
last_time.setSeconds(last_sec);
var last_num = last_time.getTime();

var no_time = new Date();
var no_num = no_time.getTime();

var view = new String();
if(lay1){view += lay1;}
for(var r=0;r<rss.length;r++){
	//
	var this_time = new Date();
	this_time.setFullYear(rss[r][0].slice(0,4));
	this_time.setMonth(rss[r][0].slice(5,7)-1);
	this_time.setDate(rss[r][0].slice(8,10));
	this_time.setHours(rss[r][0].slice(11,13));
	this_time.setMinutes(rss[r][0].slice(14,16));
	this_time.setSeconds(rss[r][0].slice(17,19));
	var this_num = this_time.getTime();
	var we = this_time.getDay();
	//
	var kiji = new String(lay2);
	
	if(kiji.search(/<!--date\\((.*?)\\)-->/) >= 0){
		var date_format = kiji.replace(/(.*)<!--date\\((.*?)\\)-->(.*)/,'\$2');
		date_format = date_format.replace(/year/g,rss[r][0].slice(0,4));
		date_format = date_format.replace(/month/g,rss[r][0].slice(5,7));
		date_format = date_format.replace(/day/g,rss[r][0].slice(8,10));
		date_format = date_format.replace(/week/g,Week[we]);
		date_format = date_format.replace(/hour/g,rss[r][0].slice(11,13));
		date_format = date_format.replace(/minute/g,rss[r][0].slice(14,16));
		date_format = date_format.replace(/second/g,rss[r][0].slice(17,19));
		kiji = kiji.replace(/<!--date\\((.*?)\\)-->/g,date_format);
	}else if(kiji.search(/<!--date-->/) >= 0){
		kiji = kiji.replace(/<!--date-->/g,rss[r][0].slice(0,10)+'('+Week[we]+') '+rss[r][0].slice(11,16));
	}
	
	if(this_num > no_num-($NewHours*60*60*1000)){
		kiji = kiji.replace(/<!--new-->/g,'<img src="$NewMark" />');
	}
	kiji = kiji.replace(/<!--site_title-->/g,rss[r][4]);
	kiji = kiji.replace(/<!--site_link-->/g,rss[r][5]);
	kiji = kiji.replace(/<!--title-->/g,rss[r][1]);
	kiji = kiji.replace(/<!--link-->/g,rss[r][2]);
	kiji = kiji.replace(/<!--description-->/g,rss[r][3]);
	view += kiji;
}
if(lay3){view += lay3;}
document.write(view);


if(no_num > last_num+(term*60*1000)){
	document.write('<script type="text/javascript" src="$this_cgi_url?order=get"></script>');
}
//----------------------------------------------------//
EOM
	if($MojiCode != 1){
		my$code;
		if(eval "use Encode;\${Encode::VERSION}"){
			   if($MojiCode == 2){$code = 'utf8';}
			elsif($MojiCode == 3){$code = 'euc-jp';}
			eval "Encode::from_to(\$js,'shiftjis','$code');";
		}elsif(eval "use Jcode;\${Jcode::VERSION}"){
			   if($MojiCode == 2){$code = 'utf8';}
			elsif($MojiCode == 3){$code = 'euc';}
			eval "\$js = Jcode->new(\$js,'sjis')->$code();";
		}
	}
	open(DAT,">$MakeDire/$MooRRJs2");
	print DAT $js;
	close(DAT);
}
#+------------------------------------------------------+
sub this_cgi_url{
	my$this_cgi_url;
	if($ENV{'SERVER_PORT'} == 443){
		$this_cgi_url = 'https://'.$ENV{'HTTP_HOST'}.$ENV{'SCRIPT_NAME'};
	}else{
		$this_cgi_url = "http://".$ENV{'HTTP_HOST'}.$ENV{'SCRIPT_NAME'};
	}
	return $this_cgi_url;
}
#+------------------------------------------------------+
sub utf_dec{
	my($str) = @_;
	$str =~s/%([0-9A-Fa-f][0-9A-Fa-f])/%$1/g;
	$str =~tr/+/ /;
	$str =~s/\xe3\x80\x9c/\xef\xbd\x9e/gi;
	$str =~s/\xe2\x80\x96/\xe2\x88\xa5/gi;
	$str =~s/\xe2\x88\x92/\xef\xbc\x8d/gi;
	$str =~s/\xc2\xa2/\xef\xbf\xa0/gi;
	$str =~s/\xc2\xa3/\xef\xbf\xa1/gi;
	$str =~s/\xc2\xac/\xef\xbf\xa2/gi;
	if(eval "use Encode;\${Encode::VERSION}"){
		eval "Encode::from_to(\$str,'utf8','cp932');";
	}elsif(eval "use Jcode;\${Jcode::VERSION}"){
		eval "\$str = Jcode->new(\$str,'utf8')->cp932();";
	}
	return $str;
}
#+------------------------------------------------------+
sub taboouens{
	my$tabooen;
	foreach my$taboo(@_){
		if(eval "use Encode;\${Encode::VERSION}"){
			eval "Encode::from_to(\$taboo,'cp932','utf8');";
		}elsif(eval "use Jcode;\${Jcode::VERSION}"){
			eval "\$taboo = Jcode->new(\$taboo,'sjis')->utf8();";
		}
		$taboo =~s/([^\w ])/'%'.unpack('H2',$1)/eg;
		$taboo =~tr/ /+/;
		$tabooen .= "$taboo|";
	}
	$tabooen =~s/\|$//g;
	return $tabooen;
}
#+------------------------------------------------------+
sub taboolins{
	my$taboos;
	foreach my$taboo(@_){
		$taboos .= "$taboo|";
	}
	$taboos =~s/\|$//g;
	return $taboos;
}
#+------------------------------------------------------+
sub en{
	my($str) = @_;
	$str =~s/([^\w ])/'%'.unpack('H2',$1)/eg;
	$str =~tr/ /+/;
	return $str;
}
#+------------------------------------------------------+
sub text_byte_shape{
	my($str,$byte) = @_;
	$str =~s/<(.*?)>|\r\n|\r|\n//g;
	my$wo = substr($str,$byte-2,2);
	if(eval "use Encode;\${Encode::VERSION}"){#
		eval "Encode::from_to(\$wo,'cp932','euc-jp');";
	}elsif(eval "use Jcode;\${Jcode::VERSION}"){
		eval "\$wo = Jcode->new(\$wo,'sjis')->euc();";
	}
	my$val;
	if($wo =~/[\xA1-\xFE][\xA1-\xFE]$/){
		$val = substr($str,0,$byte);
	}else{
		$val = substr($str,0,$byte-1);
	}
	return $val;
}
#+------------------------------------------------------+
