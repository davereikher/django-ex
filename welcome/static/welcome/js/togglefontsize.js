function togglefontsize() {
	var ftsize = document.querySelector('input[name="fontsize"]:checked').value;		
   if(ftsize == "100") {
   	document.cookie = "fontsize=100";
   	document.cookie = "checked100=checked";
   	document.cookie = "checked80=";   	   	
      document.getElementById("body_log").setAttribute("style","font-size:100%;")   	
   } else {
   	document.cookie = "fontsize=80";   	   	 
   	document.cookie = "checked100=";
   	document.cookie = "checked80=checked";   	   	
      document.getElementById("body_log").setAttribute("style","font-size:80%;")    
	}
   return;
}