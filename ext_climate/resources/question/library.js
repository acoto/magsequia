/**
 * Created by brandon on 27/06/16.
 */

$(document).ready(function()
{
	// $('#SearchInTable').keyup(function()
	// {
	// 	searchTable($(this).val());
	// });
    //
	// $('#SearchInTable2').keyup(function()
	// {
	// 	searchTable2($(this).val());
	// });
    console.log("hola plugin");


});

function showIFrame(url,windowTitle,buttonCaption)
{

    document.getElementById('modaliframe').src = url;
    document.getElementById("modaltitle").innerHTML = windowTitle;
    document.getElementById("modalmainbutton").innerHTML = buttonCaption;
    document.getElementById("modalmainbutton").style.cssText = "color: transparent; background-color: transparent; border: none;";
    //document.getElementById("modaliframecont").style.cssText = "min-height: 650px;";
    //document.getElementById("modaliframecont").style.cssText = "min-width: 900px;";
    $('#modal1').modal('show');
}

function closeModal() {
    $('#modal1').modal('hide');
}

$('#modal1').on('hidden.bs.modal', function () {
  location.reload();
});

