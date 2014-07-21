from django.contrib import admin

from stories.models import Story



# Creating a class that inherits from the ModelAdmin class
class StoryAdmin(admin.ModelAdmin):
	# Modify the list display to inlcude all the fields we want.
	list_display = ('lower_case_title', 'domain', 'moderator', 'created_at', 'updated_at')
	# Create a filter based on created_at and updated_at
	list_filter = ('created_at', 'updated_at')
	# Create a search field that searches on the title attribute
	search_fields = ('title', 'moderator__username', 'moderator__first_name', 'moderator__last_name' )

	# Define the fields and their order that we want to see in the admin.
	#fields = ('title', 'url', 'created_at', 'updated_at',)

	fieldsets = [
		('Story', {
			'fields': ('title', 'url', 'points')
		}),
		('Moderator', {
			'classes': ('collapse',),
			'fields' : ('moderator',)
		}),
		('Change History', {
			'classes': ('collapse',),
			'fields': ('created_at', 'updated_at')
		})
	]

	# Create some read-only fields to display the fields that are not editable
	readonly_fields = ('created_at', 'updated_at',)

	# Create a method to return lower case titles
	def lower_case_title(self, obj):
		# Return the result of the object in lower case
		return obj.title.lower()
	# Adjust the column header so that it returns the title
	lower_case_title.short_description = 'title'

admin.site.register(Story, StoryAdmin)

