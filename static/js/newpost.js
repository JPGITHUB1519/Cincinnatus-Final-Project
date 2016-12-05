$(document).ready(function()
{
	// function to ask if the user will put a new category
	// it show/hide the new category input
	function ask_category()
	{
		if($("#category").val() == "other")
		{
			$("#new_category").removeClass("invisible");
			$("#new_category").addClass("visible");
		}
		else
		{
			$("#new_category_text").val("");
			$("#new_category").addClass("invisible");
			$("#new_category").removeClass("visible");
			// putting a null value when hiding
			
		}
	}
	// ask on load
	ask_category()
	// show/hide new category
	$("#category").change(function(){
	    ask_category()
	});

	$("#btn-submit-post").click(function()
	{
		var data_html = CKEDITOR.instances.content.getData();
		$("#post_content").val(data);
	});
});
