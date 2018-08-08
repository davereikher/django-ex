function setDivUnits(preID,curI,count,quantity){
	var curID  = preID + (curI+1).toString();
	var curVal = parseInt(document.getElementById(curID).value);
   var goodUnitID  = "good"+curID;
   var goodUnitVal = parseInt(document.getElementById(goodUnitID).value);
   if (goodUnitVal > 0) {   	
   	document.getElementById(goodUnitID).value = (0).toString();
   	document.getElementById(goodUnitID).onchange();
   }
	var sumVal = 0; 
   for (i = 0; i < count; i++) {
	   var id = preID + (i+1).toString();
	   var inpVal = parseInt(document.getElementById(id).value);
	   sumVal = sumVal + inpVal;
   }
   if (sumVal > quantity) {
   	var exVal = sumVal - quantity;
	   document.getElementById(curID).value = (curVal - exVal).toString();   	
	   document.getElementById("dividedUnits").value = quantity.toString();   	
	   document.getElementById("hiddenLeftUnits").value = (0).toString();
      document.getElementsByClassName("leftU")[0].classList.add("fullysplit");      
      document.getElementsByClassName("leftU")[0].innerHTML = "There are no more Units left in Batch!";
   	return;   	
   }	
	document.getElementById("dividedUnits").value = sumVal.toString();	
   if (sumVal < quantity) {
   	var leftVal = quantity - sumVal;
   	document.getElementsByClassName("leftU")[0].classList.remove("fullysplit");
   	if (leftVal == 1) {
	      document.getElementsByClassName("leftU")[0].innerHTML = "There is still 1 Unit left in Batch!";   		
   	} else {	
	      document.getElementsByClassName("leftU")[0].innerHTML = "There are still "+leftVal+" Units left in Batch!";
	   }
   } else if(sumVal == quantity) {
	   document.getElementById("hiddenLeftUnits").value = (0).toString();   	
      document.getElementsByClassName("leftU")[0].classList.add("fullysplit");
      document.getElementsByClassName("leftU")[0].innerHTML = "There are no more Units left in Batch!";
   }
   return;   	
}
function setDivGoodUnits(preID1,preID2,curI,count,goodquantity) {
	var curID1  = preID1 + (curI+1).toString();
	var curID2  = preID2 + (curI+1).toString();	
	var curVal1 = parseInt(document.getElementById(curID1).value);
	var curVal2 = parseInt(document.getElementById(curID2).value);
	var sumVal = 0;
   if (curVal1 < curVal2) {
   	curVal2 = curVal1;
	   document.getElementById(curID2).value = (curVal2).toString();   	
   }					 
   for (i = 0; i < count; i++) {
	   var id = preID2 + (i+1).toString();
	   var inpVal = parseInt(document.getElementById(id).value);
	   sumVal = sumVal + inpVal;
   }
	document.getElementById("dividedGoodUnits").value = sumVal.toString();
   if (sumVal > goodquantity) {
   	var exVal = sumVal - goodquantity;
	   document.getElementById(curID2).value = (curVal2 - exVal).toString();   	
	   document.getElementById("dividedGoodUnits").value = goodquantity.toString();   	
	   document.getElementById("hiddenLeftGoodUnits").value = (0).toString();
      document.getElementsByClassName("leftGoodU")[0].classList.add("fullysplit");      
      document.getElementsByClassName("leftGoodU")[0].innerHTML = "There are no more Good Units to subdivide!";
   	return;   	
   }	   
   if (sumVal < goodquantity) {
   	var leftVal = goodquantity - sumVal;
   	document.getElementsByClassName("leftGoodU")[0].classList.remove("fullysplit");
   	if (leftVal == 1) {
	      document.getElementsByClassName("leftGoodU")[0].innerHTML = "There is still 1 Good Unit to subdivide!";   		
   	} else {	
	      document.getElementsByClassName("leftGoodU")[0].innerHTML = "There are still "+leftVal+" Good Units to subdivide!";
	   }
   } else if(sumVal == goodquantity) {
	   document.getElementById("hiddenLeftGoodUnits").value = (0).toString();   	
      document.getElementsByClassName("leftGoodU")[0].classList.add("fullysplit");
      document.getElementsByClassName("leftGoodU")[0].innerHTML = "There are no more Good Units to subdivide!";
   }
	return;
}
function iffullysplitup() {	
	var units     = document.getElementById("hiddenLeftUnits").value;
	var goodunits = document.getElementById("hiddenLeftGoodUnits").value;
	if(units == 0 && goodunits == 0){		
		return true;		
	} else {
		alert("Units in Batch or Good Units not yet fully split up!");
		return false; 
	}
}