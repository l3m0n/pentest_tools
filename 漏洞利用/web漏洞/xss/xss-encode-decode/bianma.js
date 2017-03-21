		var encodeObj = document.getElementById("encode");
		//定义变量 encodeObj 获取到 左边要加密的文本域
		var decodeObj = document.getElementById("decode");
		//定义变量 decodeObj 获取到 右边解密后的文本域
		var dianji = document.getElementsByTagName("button");
		//获得常规变异是否勾选
		var hexchanggui = document.getElementById("htmlbianyi");
		//获得非常规变异是否勾选
		var hexnochanggui = document.getElementById("hex90");
		//获得是否要去掉html编码的分号
		var fenhao = document.getElementById("htmlfenhao");
		//获得是否要对&#进行url编码
		var twoURL = document.getElementById("twoURL");

		//定义变量 dianji 等于整个网页中的所有按钮对象
			for(var i =0;i<dianji.length;i++)   //dianji 是个数组 遍历数组
			{
				dianji[i].onclick=function()   //如果按钮中的某个按钮被点击  将执行一个匿名函数
				{
				var type= this.getAttribute("leixing");   //定义一个变量 type 获得当前被点击按钮的 leixing 属性！
				if(type=="jiami")						//如果leixing属性的值 等于 jiami 
					{
							jiami(this.name);			//那么便调用加密函数 传参 当前按钮的name属性的值 function jiami(name)
					}
				if(type=="jiemi")						//如果leixing属性的值 等于 jiemi
					{
						jiemi(this.name)				//那么便调用解密函数 传参 当前按钮的name属性的值 function jiemi(name)
					}
				}
			}
	
		function jiami(s)   //加密函数  定义一个变量  s 接受传入进来的值
		{
			//把传入的值 赋给变量 encode
			var encode = s;
			//if选择的url编码 则进入url编码 代码块
			if(encode=="url")
			{
				try
				{
					decodeObj.value = encodeURIComponent(encodeObj.value);
				}
				catch(e)
				{
					alert(e);
				}
			}

			//如果选择的html实体编码十进制
			if(encode=="html10")
			{
				try
				{

					var jieguo = "";
					if(fenhao.checked)
					{
						for(var i=0;i<encodeObj.value.length;i++)
						{
							jieguo +="&#"+encodeObj.value.charCodeAt(i);
						}
					}
					else
					{
						for(var i=0;i<encodeObj.value.length;i++)
						{
							jieguo +="&#"+encodeObj.value.charCodeAt(i)+";";
						}
					}

					//检查常规变异是否勾选
					if(hexchanggui.checked){
						//如果勾选 那么便加七个0
						//如果勾选对&#编码
						if(twoURL.checked)
						{
						var erciURL = jieguo.replace(/&#/g,"%26%230000000");
						decodeObj.value=erciURL;
						}
						else
						{
						var changgui = jieguo.replace(/&#/g,"&#0000000");
						decodeObj.value=changgui;
						}
					}

					//检查非常规变异是否勾选
					else if(hexnochanggui.checked)
					{
						//如果勾选则加10个0
						if(twoURL.checked)
						{
						var erciURL1 = jieguo.replace(/&#/g,"%26%230000000000");
						decodeObj.value=erciURL1;
						}
						else
						{
						var nochanggui = jieguo.replace(/&#/g,"&#0000000000");
						decodeObj.value=nochanggui;
						}
					}

					else
					{
						if(twoURL.checked)
						{
							decodeObj.value= jieguo.replace(/&#/g,"%26%23");
						}
						else
						{
							decodeObj.value=jieguo;
						}
					}
				}
				catch(e)
				{
					alert(e);
				}
				
			}

			//如果选择的html实体编码十六进制
			if(encode=="html16")
			{
				try{
					var jieguo = "";
					if(fenhao.checked)
					{
						for(var i=0;i<encodeObj.value.length;i++)
						{
							jieguo +="&#x"+encodeObj.value.charCodeAt(i).toString(16);
						}
					}
					else
					{
						for(var i=0;i<encodeObj.value.length;i++)
						{
							jieguo +="&#x"+encodeObj.value.charCodeAt(i).toString(16)+";";
						}
					}

					//检查常规变异是否勾选
					if(hexchanggui.checked){
						//如果勾选 那么便加七个0
						if(twoURL.checked)
						{
							decodeObj.value = jieguo.replace(/&#x/g,"%26%23x0000000");
							
						}
						else
						{
							var changgui = jieguo.replace(/&#x/g,"&#x0000000");
							decodeObj.value=changgui;
						}
					}

					//检查非常规变异是否勾选
					else if(hexnochanggui.checked)
					{
						//如果勾选则加10个0
						if(twoURL.checked)
						{
							decodeObj.value = jieguo.replace(/&#x/g,"%26%23x0000000000");
						}
						else
						{
							decodeObj.value = jieguo.replace(/&#x/g,"%26%23x0000000000");
						}
					}

					else
					{
						if(twoURL.checked)
						{
							decodeObj.value=jieguo.replace(/&#x/g,"%26%23x");
						}
						else
						{
							decodeObj.value=jieguo;
						}
					}

					}
				catch(e)
				{
					alert(e);
				}

			}

			//如果选择的编码是js unicode编码
			if(encode=="jsunicode")
			{
			try{	
				var jieguo = "";
				for(var i=0;i<encodeObj.value.length;i++)
				{
					jieguo +="\\u00"+encodeObj.value.charCodeAt(i).toString(16);
				}
				decodeObj.value=jieguo;
				}
				catch(e)
				{
					alert(e);
				}
				

			}

			//如果选择的是js16进制编码
			if(encode=="js16")
			{
				try{
				var jieguo = "";

				for(var i=0;i<encodeObj.value.length;i++)
				{
					jieguo +="\\x"+encodeObj.value.charCodeAt(i).toString(16);
				}
				if(hexchanggui.checked)
				{
						//如果勾选 那么便加七个0
						var changgui = jieguo.replace(/\\x/g,"\\x0000000");
						decodeObj.value=changgui;
				}

					//检查非常规变异是否勾选
					else if(hexnochanggui.checked)
					{
						//如果勾选则加10个0
						var nochanggui = jieguo.replace(/\\x/g,"\\x0000000000");
						decodeObj.value=nochanggui;

					}

					else
					{
						decodeObj.value=jieguo;
					}

				}
				catch(e){

					alert(e);
				}

			}

			//如果选择的是js8进制编码
			if(encode=="js8")
			{
				try{
				var jieguo = "";
				for(var i=0;i<encodeObj.value.length;i++)
				{
					jieguo +="\\"+encodeObj.value.charCodeAt(i).toString(8);
				}
				decodeObj.value=jieguo;
				}
				catch(e)
				{
					alert(e);
				}

			}
			//如果选择的是base64编码
			if(encode=="base64")
			{	
				
				try{
					decodeObj.value=btoa(encodeObj.value);
				}
				catch(e)
				{
					alert(e.message);
				}
			}

			//如果选择的是 String.charCodeAt 编码
			if(encode=="String")
			{
				try
				{
					var Stringen = encodeObj.value;  //定义一个变量 获取要加密的内容
					var Stringde = new Array();		//创建一个新的数组  接受加密后的内容
					for(var i=0;i<Stringen.length;i++) 
					{
						Stringde[i]=Stringen.charCodeAt(i)  //数组中的 第当前循环值的下标的值 等于 要加密的当前下标的值  加密
					}
					decodeObj.value="String.fromCharCode("+Stringde+")";

				}	

				catch(e)
				{
					alert(e.message);
				}
			}

		}
		//以上是加密函数
		//以下是解密函数
		
		function jiemi(s)
		{
			//创建一个变量接受传过来的解码方式
			var decode = s;
			//如果解码方式等于URL
			if(decode=="url")
			{
				try{
				decodeObj.value=decodeURIComponent(encodeObj.value);
				}
				catch(e)
				{
					alert(e);
				}
			}

			//如果解码方式是html实体编码十进制
			if(decode=="html10")
			{
				try{
				var jieguo ="";
				var jieguoary= decodeObj.value.split("&#");
				for(var i=1;i<jieguoary.length;i++)
				{
					jieguo+=String.fromCharCode(parseInt(jieguoary[i].replace(';','')));
				}
				decodeObj.value=jieguo;
				}
				catch(e)
				{
					alert(e);
				}
			}

			//如果解码方式是html实体编码十六进制
			if(decode=="html16")
			{
				try{
				var jieguo ="";
				var jieguoary= encodeObj.value.split("&#x");
				for(var i=1;i<jieguoary.length;i++)
				{
					jieguo+=String.fromCharCode(parseInt(jieguoary[i],16));
				}
				decodeObj.value=jieguo;
				}
				catch(e)
				{
					alert(e);
				}
			}

			//如果解码方式是js unicode编码
			if(decode=="jsunicode")
			{
				try{
				var jieguo ="";
				var jieguoary= encodeObj.value.split("\\u00");
				for(var i=1;i<jieguoary.length;i++)
				{
					jieguo+=String.fromCharCode(parseInt(jieguoary[i],16));
				}
				decodeObj.value=jieguo;
				}
				catch(e)
				{
					alert(e)
				};
			}

			//如果解码方式是js16进制编码
			if(decode=="js16")
			{
				try{
				var jieguo ="";
				var jieguoary= encodeObj.value.split("\\x");
				for(var i=1;i<jieguoary.length;i++)
				{
					jieguo+=String.fromCharCode(parseInt(jieguoary[i],16));
				}
				decodeObj.value=jieguo;
				}
				catch(e)
				{
					alert(e);
				}
			}

			//如果解码方式是js8进制编码
			if(decode=="js8")
			{
				try{
					var jieguo ="";
					var jieguoary= encodeObj.value.split("\\");
					for(var i=1;i<jieguoary.length;i++)
						{
							jieguo+=String.fromCharCode(parseInt(jieguoary[i],8));
						}
					decodeObj.value=jieguo;
					}
				catch(e)
				{
					alert("e");
				}
			}

			

			//如果解码方式是base64编码
			if(decode=="base64")
			{
				try
				{
					decodeObj.value=atob(encodeObj.value);
				}
				catch(e)
				{
					alert("e");
				}
			}

			//如果解码方式是String.fromCharCode
			if(decode=="String")
			{

				try
				{	
					var temp = encodeObj.value.split(",");
					for(var i=0;i<temp.length;i++)
					{
						decodeObj.value+=String.fromCharCode(temp[i])
					}


				}

				catch(e)
				{

					alert("e");
				}

			}
		}			

