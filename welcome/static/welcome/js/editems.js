function toggleRange() {
	var checkbox   = document.getElementById("chooseRange");
	var startrange = document.getElementById("startRange");	
	var endrange   = document.getElementById("endRange");	
   var disabled   = document.getElementById("disabledPOST");
	var startPlh   = document.getElementById("startPlaceholderPOST");
	var endPlh     = document.getElementById("endPlaceholderPOST");
	if(checkbox.checked == false) {
		endrange.value = ""; endrange.placeholder = ""; endrange.disabled = true; disabled.value = "disabled";
		startrange.placeholder = "single ID"; startPlh.value = "single ID"; endPlh.value = "";
	} else {
	   endrange.placeholder = "end range #"; endrange.disabled = false; disabled.value = "";
	   startrange.placeholder = "single ID / start range #"; startPlh.value = "single ID / start range #"; endPlh.value = "end range #";
	}
}