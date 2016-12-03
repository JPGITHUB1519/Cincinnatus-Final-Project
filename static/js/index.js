function post_by_category_ajax(category_id)
{
	/* ajax request to get the post by category to use on change select */
	$.ajax
		({
		type : "POST",
		url : "/post_categorizer",
		contentType : "application/json",
		datatype : "json",
		// send json to the server
		data : JSON.stringify({"category_id" : category_id})
	})
	.done(function(json)
	{
		// console.log(json["data"]);
		//render data in ther server
		$("#post").remove();
		/* updating data */
		var blog_header = '<div class="row" id="blog-header"></div>';
		var blog_data = '<div class="row" id="blog-data"></div>';
		var blog_content = '<div class="row" id="blog-content"></div>';
		var end_div = '</div>';
		var date_content = "<div class='col-md-1 date text-center visible-only-large'><p>%data%</p></div>";
		var subject_content = "<div class='col-md-10'><h1 class='text-beatiful-red font-lobster'>%data%</h1></div>";
		var username_content = '<div class="col-sm-6"><p class="font-pacifico text-semi-large text-center-only-small" >Written By %data%</p></div>';
		var category_content = '<div class="col-sm-6"><p class="text-semi-large text-beatiful-blue text-center-only-small">Category : <span class="text-black">%data%</span></p>';
		var content_content = '<div class="col-md-12"><p>%data%</p></div>';
		var noresult = '<div class="row"><div class="col-md-12 error-text text-center"><h1>There are not Post with this category</h1></div></div>'; 
		$(".container").append("<div id='post'></div>");
		if(json["data"].length > 0)
		{
			for(var i = 0; i < json["data"].length; i++)
			{
			$("#post").append(blog_header);
			$("#post").append(blog_data);
			$("#post").append(blog_content);
			$("#blog-header").append(date_content.replace("%data%", json["data"][i]["date"]));
			$("#blog-header").append(subject_content.replace("%data%", json["data"][i]["subject"]));
			$("#blog-data").append(username_content.replace("%data%", json["data"][i]["username"]));
			$("#blog-data").append(category_content.replace("%data%", json["data"][i]["category"]));
			$("#blog-content").append(content_content.replace("%data%", json["data"][i]["content"]));
			}
		}
		else
		{
			$("#post").append(noresult);
		}
	})
	.fail(function(xhr, textStatus)
	{
		console.log(textStatus);
	});
}

function like_ajax(post_id)
{
	console.log(post_id)
	$.ajax(
	{
		type : "POST",
		url : "/post_sensation",
		contentType : "application/json",
		datatype : "json",
		// data sent to the server
		data : JSON.stringify({"post_id" : post_id, "action_type" : "like"})

	})
	.done(function(response)
	{
		if(response["status"] == "ok")
		{
			$("#likes_counter").text(response["likes"])
		}
		// quit focus
		like_link = "#like_caller_" + response["post_id"];
		$(like_link).blur();
		console.log(response);
	})
	.fail(function(textStatus)
	{
		console.log(textStatus);
	});
}


// dislikes stuffs
function dislike_ajax(post_id)
{
	console.log(post_id)
	$.ajax(
	{
		type : "POST",
		url : "/post_sensation",
		contentType : "application/json",
		datatype : "json",
		// data sent to the server
		data : JSON.stringify({"post_id" : post_id, "action_type" : "dislike"})

	})
	.done(function(response)
	{
		if(response["status"] == "ok")
		{
			$("#dislikes_counter").text(response["dislikes"]);
			// quit focus on link
			var dislike_link = "#dislike_caller_" + response["post_id"];
			console.log(dislike_link);
			$(dislike_link).blur();
		}
		console.log(response);
	})
	.fail(function(textStatus)
	{
		console.log(textStatus);
	});
}

$(document).ready()
{
	$("#category_chooser").change(function()
	{
		var category_id = $(this).find("option:selected").val();
		post_by_category_ajax(category_id);
	});

	// $("#like_caller").click(function()
	// {
	// 	var post_id = $(this).val();
	// 	like_ajax(post_id);
	// });
}