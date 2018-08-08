function setSQL(content){
	document.getElementById("hiddenSQL").value = content;
	//alert(content);
}

function handleComment() {
    var comtext = prompt("Please enter your comment", "new comment");
    if (comtext != null) {    	
        var comtype = document.getElementById("comtypbutton").value;
        document.getElementById("hiddenCOMTYPE").value = comtype;        
        document.getElementById("hiddenCOMTEXT").value = comtext;
        document.getElementById("loadEQ").click();
    }
}

function handleMTFofExistingDocs() {
    var promptMTF = prompt("Please enter MTF - Number (20MN X XXXX # ####) of existing Document(s)", "");
    if (promptMTF != null) {
        var MTF = promptMTF.replace(/\s+/g,"");
        if (MTF != "") {    	  
           document.getElementById("hiddenDOCMTF").value = MTF;
           document.getElementById("loadEQ").click();
        }
    }
}

function disp_prompt(){
	var MTF = prompt("Where do you want to attach your Equipment? Please enter the MTF ID of the parent equipment!","")
	var SUB = prompt("Please enter the Sub Batch ID of the parent, if applicable.","")
	var POS = prompt("Please enter the position in which the child should be put, if applicable (like top/bottom...).","")
	if (MTF != null && MTF!=""){
		//if (SUB != null && SUB != ""){
			document.getElementById("hiddenPARMTF").value = MTF;
			document.getElementById("hiddenPARSUB").value = SUB;
			document.getElementById("hiddenPARPOS").value = POS;
			document.getElementById("loadEQ").click();
		//}
	}
}
 
function disp_prompt2(){
	var MTF = prompt("Which Equipment do you want to attach to this parent? Please enter the MTF ID of the child equipment!","")
	var SUB = prompt("Please enter the Sub Batch ID of the child, if applicable.","")
	var POS = prompt("Please enter the position in which the child should be put, if applicable (like top/bottom...).","")
	if (MTF != null && MTF!=""){
		//if (SUB != null && SUB != ""){
			document.getElementById("hiddenCHILMTF").value = MTF;
			document.getElementById("hiddenCHILSUB").value = SUB;
			document.getElementById("hiddenCHILPOS").value = POS;
			document.getElementById("loadEQ").click();
		//}
	}
}

function changecolor(id){
    document.getElementById(id).style.color="#000000";	
    document.getElementById(id).style.backgroundColor="#ffbf00"; 
}

function loadtable(var3){
   //alert(var3);
   if (var3 != "partab") {
      document.getElementById("hiddenTAB").value = var3;
   }
   document.getElementById("loadOver").click();
}

function changecolorOver(id){
    document.getElementById(id).style.backgroundColor="#ffbf00"; 
    document.getElementById("loadOver").click();
}

function checkmtftype(pattern) {
	var mtftype = document.getElementById("mtftype").value;
	var pattern = document.getElementById("mtftype").getAttribute("pattern");
	if (mtftype.match(pattern)) {
	   document.formregister.submit();	
	}
	return;
}

function setDocID(id){
	document.getElementById("dlDocID").value = id;	
	document.getElementById("loadEQ").click();
}

function setID(value2){
	document.getElementById("inEQIDfield").value = value2;
	document.getElementById("loadEQ").click();
}
function compareShippingDates(){
	var datFrom = document.getElementById("dateFrom").value;  
	var datTo   = document.getElementById("dateTo").value;
	if(datFrom > datTo) {
	   alert("Expected return date is before shipping date!");
	   document.getElementById("dateTo").value = "";
	}
	return;
}
function isGroupAlias() {
	var line1 = "NOTE: This group has already an alias/other ID defined. After splitting the group, it must be unique for each newly created item.\n\n";
	var line2 = "There are two possibilities to proceed: Either you define an alias for each item by choosing a new alias with a running number added to it => Select ALIAS Range, or the alias will be deleted (default).\n\n"; 
   var alias = document.getElementById("inEQALIASfield").value;
   if (alias != "") {
	   alert(line1+line2);
	}
	return;
}
function isBatchAlias(alias) {
	var line1 = "NOTE: You assigned an Alias to this batch.\n\n";
	var line2 = "The sub batches need to have unique Alias IDs after splitting. Therefore, the sub batch ID will be appended to the Alias automatically. If you want to change it, go to Display Equipment and change the Aliases of the sub batches after splitting.\n\n"; 
   var line3 = "As an alternative approach, you could also remove the Alias completely. It is not recommended to use them for batches if not strictly necessary (i.e. because the manufacturer already named the items etc.).";
   if (alias != "") {
	   alert(line1+line2+line3);
	}
	return;
}
function compareShippingDates() {
	var dateFrom = document.getElementById("dateFrom").value;
	var dateTo   = document.getElementById("dateTo").value;
	if (dateFrom > dateTo) {
		alert("Please insert a future date!");
		document.getElementById("dateTo").value = "";		
	}
	return;	
}
function validateShipping(fault) {
	var rangeCount = document.getElementById("rangeCountTotal").value;
	var destId = document.getElementById("siteTo").value;
	if (rangeCount == 0) {
	   alert("No Equipment selected!");
      return false;
   } else if (destId == 99) {
      alert("No Destination selected!");
      return false;
   } else if (parseInt(fault) > 0) {
   	alert("You have selected items and/or batches together that have different actual locations!");
   	return false;      
   } else {
   	return true;
   }      
}
function toggleSelectAll() {
	var checkAll   = document.getElementById("checkAll");
   var checkboxes = document.getElementsByClassName("itemId");
   if (checkAll.checked) {
      for (var i in checkboxes){
         checkboxes[i].checked = true;
      }   	
   } else {
      for (var i in checkboxes){
         checkboxes[i].checked = false;
      }   	   	
   }   
	return;
}
function clearShipmentId() {
	document.getElementById("clearShipId").value = "";
	return;
}
function clearLoadEquipment(usersLocation) {
	document.getElementById("siteFromId").value = 99;
	document.getElementById("siteToId").value = usersLocation;	
	return;
}
function checkRecDate(id){
	var send = document.getElementById('lastItem').innerHTML;
	var sendDate = new Date(send);
	var rec  = document.getElementById(id).value;
	var recDate = new Date(rec);
	if (sendDate.valueOf() >= recDate.valueOf()) {
	   alert("Please enter a receiving date, which is after the sending date!");
	   return false;
	} else {
		return true;
	}
}
function checkDest() {
	var fromID = document.getElementById("siteFrom").value;
	var toID   = document.getElementById("siteTo").value;
	if (toID == fromID) {	   		
		alert("You cannot ship equipment inside the same location. " +
		      "If you want to change the status of this selection only, " +
		      "please use the Multi-Edit-Tool, if you have access.");
      document.getElementById("siteTo").value = 99;		
	}
   return;	
}
function trimInpStr(id,field) {
	if(id == "typeId") {
		var inpField = document.getElementById(id).value;
		if(inpField == "mtf") {
	      var byId = field;
		} else {
			return;
	   }
	
	} else {
      var byId = id;
   }   			
	var inpStr = document.getElementById(byId).value;
	document.getElementById(byId).value = inpStr.replace(/\s/g,""); 	
	return;
}
function valShipId() {
   var shipId = document.getElementById("inViewShipId").value;
   if	(shipId != "") {
   	return true;
   } else {
   	alert("Please enter shipment-ID!");
   	return false;
   }
}
function clearAttDisabled() {
	document.getElementById("stat").disabled = false;
	document.getElementById("loc").disabled = false;
	document.getElementById("roomDesc").disabled = false;		
	return;
}
function valRange(typeId) {
   var idType     = document.getElementById(typeId).value;
   var startRange = document.getElementById("startRange").value;
   var endRange   = document.getElementById("endRange").value;          	
   if (idType == "mtf" && endRange != "" && (startRange.substr(0,9) != endRange.substr(0,9))) {
   	alert("Different Equipment Types within one range are not allowed!");
   	return false;
   } else if (idType == "alias" && endRange != "") {
   	var lnStart = startRange.length;
      var lnEnd   = endRange.length;   	
   	if (lnStart != lnEnd) {
   		alert("These aliases do not match and the range could not be built. Please make sure that you enter valid ranges!");
   	   return false;
   	} else if (endRange > 0) {
   		for (i = lnStart; i >= 0; i--) {
   		   var charStart = startRange.substr(i,1);
   		   var charEnd   = endRange.substr(i,1);
   		   if (charStart != charEnd) {
               isDigitS =  /^\d+$/.test(charStart);
               isDigitE =  /^\d+$/.test(charEnd);
               if(!isDigitS || !isDigitE){
   		         alert("These aliases do not match and the range could not be built. Please make sure that you enter valid ranges!");               	
               	return false;
               }
   		   }   		   
   		}
   	}		
   }
   return true;   
}