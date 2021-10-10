$(document).ready(function () {
	sel_all_chbx = document.getElementById("check-all");
	sel_all_chbx.onclick = function(event) {
	  checkboxes = document.getElementsByClassName('b-form-checkbox');
	  for(var i=0, n=checkboxes.length;i<n;i++) {
	    checkboxes[i].checked = sel_all_chbx.checked;
  		}
	}
})