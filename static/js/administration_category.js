function insert_category(category_name)
{
	$.ajax(
	{
		type : "POST",
		url : "/administration/category",
		contentType : "application/json",
		datatype : "json",
		data : JSON.stringify({"category_name" : category_name, "action" : "insert"})
	})
	.done(function(response)
	{
		console.log(response)
		// verifying errors
		if (response["status"] == "error")
		{
			if (("error_exits" in response))
			{
				$("#error_exits").text(response["error_exits"]);
				$("#error_empty").text("");
			}
			if (("error_empty" in response))
			{
				$("#error_empty").text(response["error_empty"]);
				$("#error_exits").text("");
			}
		}	
		else
		{
			var category_key = response["category_entity"]["category_key"];
			var string_html = "<tr id='data_%category_key%' value='%category_key%'><td id='data_name_%category_key%'>%category_name%</td><td>%category_date%</td><td><a id='updater_%category_key%' class='updater' data-target='#update_category_modal' data-key-value='%category_key%'>Update</a></td><td><a id='deleter_%category_key%' href = javascript:delete_category('%category_key%'); value = '%category_key%'>Delete</a></td></tr>";
			var category_name = response["category_entity"]["category_name"];
			var category_date = response["category_entity"]["category_date"];
			string_html = string_html.replace("%category_name%", category_name);
			string_html = string_html.replace("%category_date%", category_date);
			// replace all
			string_html = string_html.replace(/%category_key%/g, category_key);
			$("#table_data").prepend(string_html);
			$("#category_name").val("");
			// delete error
			$("#error_exits").text("");
			$("#error_empty").text("");
		}

	})
	.fail(function(textStatus)
	{
		console.log(textStatus);
	});
}

function delete_category(category_key)
{
	$.ajax(
	{
		type : "POST",
		url : "/administration/category",
		contentType : "application/json",
		datatype : "json",
		data : JSON.stringify({"category_key" : category_key, "action" : "delete"})
	})
	.done(function(response)
	{
		console.log(response);
		if(response["status"] == "ok")
		{
			var data_element = "#data_" + response["category_key"];
			var caller_element = "#deleter_" + response["category_key"];
			console.log(caller_element);
			$(data_element).remove();
			// console.log(caller_element);
			$(caller_element).blur();
		}
	})
	.fail(function(textStatus)
	{
		console.log(textStatus);
	});
	
}

function update_category(category_key, category_new_value)
{
	$.ajax(
	{
		type : "POST",
		url : "/administration/category",
		contentType : "application/json",
		datatype : "json",
		data : JSON.stringify({"category_new_value" : category_new_value,
							   "category_key" : category_key, 
							   "action" : "update"
								})
	})
	.done(function(response)
	{
		console.log(response);
		if("error" in response)
		{
			$("#update_error").text(response["error"]);
		}
		else
		{
			var row_name_name = "#data_name_" + category_key;
			$('#update_category_modal').modal('hide');
			$("#update_error").text("");
			$(row_name_name).text(response["category_entity"]["category_name"]);
		}
	})
	.fail(function(textStatus)
	{
		console.log(textStatus);
	});
	
}

$(document).ready(function()
{
	$("#save").click(function(e)
	{
		e.preventDefault();
		category_name = $("#category_name").val();
		insert_category(category_name);
	});

	// $(".updater").click(function(e)
	// {
	// 	// open modal
	// 	$("#update_category_modal").modal();
	// 	alert("hey")
	// 	var category_key = $(this).data("key-value");
	// 	var data_name_name = "#data_name_" + category_key;
	// 	console.log(data_name_name);
	// 	var row_val = $(data_name_name).text();
	// 	$("#new_category_name").val(row_val);
	// 	$("#old_category_name").text(" " + row_val);
	// 	$("#new_category_name").data("category-key", category_key);
	// 	// clean any error when click
	// 	$("#update_error").text("");

	// });

	/* When the document is already loaded and we wanna make a event future new objects we have
		to use a delegate like this */

	// Click for Future Links 
	$(document).on("click", '.updater', function (e) 
	{
		// open modal
		$("#update_category_modal").modal();
		var category_key = $(this).data("key-value");
		var data_name_name = "#data_name_" + category_key;
		console.log(data_name_name);
		var row_val = $(data_name_name).text();
		$("#new_category_name").val(row_val);
		$("#old_category_name").text(" " + row_val);
		$("#new_category_name").data("category-key", category_key);
		// clean any error when click
		$("#update_error").text("");
	});


	$("#update_button").click(function(e)
	{
		e.preventDefault();
		var category_key = $("#new_category_name").data("category-key");
		var category_new_value = $("#new_category_name").val();
		update_category(category_key, category_new_value);

	});

	$("#close_updater_modal").click(function(e)
	{
		$("#new_category_name").val("");
		$("#old_category_name").text("");

	});
	
});