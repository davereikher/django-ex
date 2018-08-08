function valAliasRange() {
	var quantity  = document.getElementById("Quantity").value;
	var itemfirst = document.getElementById("inSEQFROM").value;
	var itemlast  = document.getElementById("inSEQTO").value;
   var alias     = document.getElementById("inSEQOTHERID").value;
   if (alias == "") {
   	if (itemfirst == "" && itemlast == "") {
         var conf = confirm("WARNING: No ALIAS Range selected!");
			return conf;
      } else {
         alert("ERROR: Please select a valid Other ID (EQ ALIAS)!");
         return false;
      }   	
   }	
	var range = parseInt(itemlast) - parseInt(itemfirst) + 1;
	if (range != parseInt(quantity)) {
	   alert("ERROR: Please select a valid ALIAS range!");
	   return false;
	} else {
      return true;
	}
}
function valSeqFrom() {
	var quantity = document.getElementById("Quantity").value;	
	var itemfirst = document.getElementById("inSEQFROM").value; 
	var itemlast = parseInt(itemfirst) + parseInt(quantity) - 1;
	document.getElementById("inSEQTO").value = itemlast;
	return;
}
function valSeqTo() {
	var quantity = document.getElementById("Quantity").value;	
	var itemlast = document.getElementById("inSEQTO").value;   
	var itemfirst = parseInt(itemlast) - parseInt(quantity) + 1;
	document.getElementById("inSEQFROM").value = itemfirst;
	return;
}
function valSeqNoMax() {
	var quantity = document.getElementById("Quantity").value;	
   var digits   = document.getElementById("inSEQDIGITS").value;
   if (digits == 3) {
      inFrom = document.getElementById("inSEQFROM");
      inFrom.setAttribute("max",999 - parseInt(quantity)); // set a new value;
      inTo = document.getElementById("inSEQTO");         	
      inTo.setAttribute("max",999); // set a new value;
   } else {
      inFrom = document.getElementById("inSEQFROM");
      inFrom.setAttribute("max",9999 - parseInt(quantity)); // set a new value;
      inTo = document.getElementById("inSEQTO");         	
      inTo.setAttribute("max",9999); // set a new value;
   }	
	return;
}
function setSeqFieldsColor() {
	document.getElementById("inSEQOTHERID").style.color="#333333";
	document.getElementById("inSEQFROM").style.color="#333333";
	document.getElementById("inSEQTO").style.color="#333333";
	document.getElementById("inSEQDIGITS").style.color="#333333";			 
	return;
}