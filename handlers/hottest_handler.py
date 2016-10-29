from basic_handler import *

class HottestPost(Handler):
	def get(self):
		"""
			Statics Algorithm

			1- get a dic with all the numbers of thing
			2- getting the hootest from the dic
			3- getting a list with the dic of the hootest ordered
		"""
		# getting the numbers of all post comment
		post_numdata_comments =  numdata_comments_all_post()
		# getting the hottest comment
		hottest_posts = hottest_dic(post_numdata_comments, 5)
		# getting all the numbers of comments by the category
		# ordering
		# data structure of this behavior
		#  idpost				number of comments,   postentity
		# [('5710932114145280', [6, <models.blog_model.Blog object at 0x04428110>])
		hottest_posts = sort_dictionary_desc(hottest_posts)
		hottest_category = count_comments_by_category(post_numdata_comments)
		hottest_category = hottest_dic(hottest_category, 5)
		hottest_category = sort_dictionary_desc(hottest_category)
		logging.error(hottest_category)
		
		self.render("hottest.html", hottest_posts = hottest_posts, hottest_category = hottest_category)
